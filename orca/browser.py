"""
Functions for browser interactions.
"""
import typer
from rich import print


def open_browser(selected_model):
    """
    Open the model page in the default web browser.

    Args:
        selected_model: Name of the model to view
    """
    print(f"Opening [bold green]{selected_model}[/bold green] page in browser.")
    if "/" in selected_model:
        typer.launch(f"https://ollama.com/{selected_model}")
    else:
        typer.launch(f"https://ollama.com/library/{selected_model}")