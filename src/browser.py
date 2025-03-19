"""
Functions for browser interactions.
"""
import requests
import typer
from bs4 import BeautifulSoup
from rich import print
from rich.console import Console
from rich.markdown import Markdown
from rich.progress import Progress, TextColumn, SpinnerColumn


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



def read_modelfile(selected_model):
    if "/" in selected_model:
        url = f"https://ollama.com/{selected_model}"
    else:
        url = f"https://ollama.com/library/{selected_model}"

    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
    ) as progress:
        progress.add_task(description=f"Fetching modelcard for {selected_model}...", total=None)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, features="html.parser")

        c = Console()
    for md in soup.select('#editor'):
        modelfile = md.contents[0]
        c.print(Markdown(modelfile))