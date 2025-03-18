import requests
import sys

from rich.progress import Progress, SpinnerColumn, TextColumn, track


def download_model(model, tag, output_filename):

    # According to the default mask in the Go code, we use:
    #   host: registry.ollama.ai
    #   namespace: library
    host = "registry.ollama.ai"
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
            print(f"Error fetching manifest: {r.status_code} - {r.text}")
            sys.exit(1)

        manifest = r.json()

        # The manifest is expected to have a "layers" field.
        layers = manifest.get("layers")
        if not layers or len(layers) == 0:
            print("No layers found in manifest.")
            sys.exit(1)

        # For simplicity, we assume the first layer is our GGUF model file.
        layer = layers[0]
        digest = layer.get("digest")
        if not digest:
            print("Layer does not contain a digest.")
            sys.exit(1)

        # Construct the URL to fetch the blob based on the digest.
        blob_url = f"https://{host}/v2/{namespace}/{model}/blobs/{digest}"

        r = requests.get(blob_url, stream=True)
        total_size = int(r.headers.get("Content-Length", 0))
        print(f"The selected model is ~{round(total_size/1024/1024)} MB")
        if r.status_code != 200:
            print(f"Error downloading blob: {r.status_code} - {r.text}")
            sys.exit(1)
    
    # Save the file using the model name with a .gguf extension.
    with open(output_filename, "wb") as f, Progress() as progress:
        task = progress.add_task("Downloading", total=total_size)

        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                progress.update(task, advance=len(chunk))
    return True
