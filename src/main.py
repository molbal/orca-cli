#!/usr/bin/env python3
"""
Main entry point for the ORCA application.
"""
import typer
from rich import print

from src.ui import export_tag_gguf
from ui import prompt_model_action, prompt_model_selector
from registry import search_models

app = typer.Typer(no_args_is_help=True)



@app.command()
def search(query: str = typer.Argument("")):
    """
    Searches the Ollama Registry for a model.

    Args:
        query: Name to search for
    """
    if query == "":
        query = typer.prompt("What shall I search Ollama Registry for?")

    models = search_models(query)
    selected_model = prompt_model_selector(models)
    if selected_model == "<- exit" or selected_model == "":
        return
    else:
        prompt_model_action(selected_model)

@app.command()
def download(model_name, tag, filename, directory):
    """
    Downloads a model from Ollama Registry to the specified location. For example the following command
    downloads llama3.2:1b as model.gguf to the current working directory.:
    `orca-cli llama3.2 1b model.gguf .`
    """
    export_tag_gguf(model_name, tag, filename, directory)


if __name__ == "__main__":
    app()