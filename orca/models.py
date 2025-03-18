"""
Functions for handling Ollama model operations.
"""
import subprocess


def pull_model(selected_model):
    """
    Pull a model from Ollama registry to local installation.

    Args:
        selected_model: Name of the model to pull
    """
    from rich import print
    print(f"Pulling [bold green]{selected_model}[/bold green] to local Ollama installation.")
    subprocess.run(f'ollama pull {selected_model}', stdout=subprocess.PIPE)