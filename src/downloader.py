import inquirer
import requests
import sys
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn, track

def adapter_download_confirmation():
    print("[bold blue]Information: [/bold blue] The selected model contains a base model + an adapter.")
    questions = [
        inquirer.Confirm("continue",
                         message="This will add a -base and an -adapter postfix to the filename."
                                 " Please confirm you want to continue.",
                         default=True)
    ]

    answers = inquirer.prompt(questions)
    if answers is None:
        return
    return answers["continue"]


def download_model(model, tag, output_filename):
    host = "registry.ollama.ai"
    if "/" in model:
        namespace = model.split('/')[0]
        model = model.split('/')[-1]
    else:
        namespace = "library"

    # Construct the URL to fetch the manifest.
    manifest_url = f"https://{host}/v2/{namespace}/{model}/manifests/{tag}"

    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
    ) as progress:
        progress.add_task(description="Reading Ollama Registry...", total=None)

        r = requests.get(manifest_url)
        if r.status_code != 200:
            print("Error connecting to Ollama Registry.")
            return False

        manifest = r.json()

        # Check if the manifest has layers
        layers = manifest.get("layers")
        if not layers or len(layers) == 0:
            print("The Ollama Registry manifest does not have a 'layers' field.")
            return False

        # Check if there's an adapter layer
        has_adapter = any(layer.get("mediaType") == "application/vnd.ollama.image.adapter" for layer in layers)

    if has_adapter:
        if adapter_download_confirmation():
            return download_model_with_adapter(host, namespace, model, layers, output_filename)
        else:
            print("User cancelled download.")
            return False
    else:
        return download_model_without_adapter(host, namespace, model, layers, output_filename)


def download_model_without_adapter(host, namespace, model, layers, output_filename):
    # Find the model layer (typically the first one with the right mediaType)
    model_layer = next((layer for layer in layers if layer.get("mediaType") == "application/vnd.ollama.image.model"),
                       None)

    if not model_layer:
        print("No model layer found in the manifest.")
        return False

    digest = model_layer.get("digest")
    if not digest:
        print("The model layer does not have a 'digest' field.")
        return False

    # Construct the URL to fetch the blob based on the digest.
    blob_url = f"https://{host}/v2/{namespace}/{model}/blobs/{digest}"

    r = requests.get(blob_url, stream=True)
    total_size = int(r.headers.get("Content-Length", 0))
    print(f"The selected model is ~{round(total_size / 1024 / 1024)} MB")
    if r.status_code != 200:
        print("Error connecting to Ollama Registry.")
        return False

    # Save the file using the provided output filename
    with open(output_filename, "wb") as f, Progress() as progress:
        task = progress.add_task("Downloading", total=total_size)

        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                progress.update(task, advance=len(chunk))

    return True


def download_model_with_adapter(host, namespace, model, layers, output_filename):
    # Find the model layer
    model_layer = next((layer for layer in layers if layer.get("mediaType") == "application/vnd.ollama.image.model"),
                       None)

    # Find the adapter layer
    adapter_layer = next(
        (layer for layer in layers if layer.get("mediaType") == "application/vnd.ollama.image.adapter"), None)

    if not model_layer:
        print("No model layer found in the manifest.")
        return False

    if not adapter_layer:
        print("No adapter layer found in the manifest.")
        return False

    # Get the model digest
    model_digest = model_layer.get("digest")
    if not model_digest:
        print("The model layer does not have a 'digest' field.")
        return False

    # Get the adapter digest
    adapter_digest = adapter_layer.get("digest")
    if not adapter_digest:
        print("The adapter layer does not have a 'digest' field.")
        return False

    # Create filenames for the model and adapter
    model_filename = output_filename.replace(".gguf", "-base.gguf")
    adapter_filename = output_filename.replace(".gguf", "-adapter.gguf")


    # Download the model
    model_blob_url = f"https://{host}/v2/{namespace}/{model}/blobs/{model_digest}"
    r_model = requests.get(model_blob_url, stream=True)
    model_size = int(r_model.headers.get("Content-Length", 0))
    print(f"The base model is ~{round(model_size / 1024 / 1024)} MB")
    if r_model.status_code != 200:
        print("Error connecting to Ollama Registry for the model.")
        return False

    # Save the model file
    print(f"Downloading base model to {model_filename}")
    with open(model_filename, "wb") as f, Progress() as progress:
        task = progress.add_task("Downloading base model", total=model_size)
        for chunk in r_model.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                progress.update(task, advance=len(chunk))

    # Download the adapter
    adapter_blob_url = f"https://{host}/v2/{namespace}/{model}/blobs/{adapter_digest}"
    r_adapter = requests.get(adapter_blob_url, stream=True)
    adapter_size = int(r_adapter.headers.get("Content-Length", 0))
    print(f"The adapter is ~{round(adapter_size / 1024 / 1024)} MB")
    if r_adapter.status_code != 200:
        print("Error connecting to Ollama Registry for the adapter.")
        return False

    # Save the adapter file
    print(f"Downloading adapter to {adapter_filename}")
    with open(adapter_filename, "wb") as f, Progress() as progress:
        task = progress.add_task("Downloading adapter", total=adapter_size)
        for chunk in r_adapter.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                progress.update(task, advance=len(chunk))

    print(f"Downloaded base model to [bold]{model_filename}[/bold] and adapter to [bold]{adapter_filename}[/bold]")
    return True