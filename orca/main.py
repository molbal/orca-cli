#!/usr/bin/env python3
"""
Main entry point for the ORCA application.
"""
import typer
from rich import print
from ui import prompt_model_action, prompt_model_selector
from registry import search_models

app = typer.Typer(no_args_is_help=True)


@app.command()
def main():
    """
    Main entry point displaying welcome message.
    """
    print("Welcome to ORCA")


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
    if selected_model is None:
        return
    if selected_model == "<- exit":
        return
    else:
        prompt_model_action(selected_model)




if __name__ == "__main__":
    app()