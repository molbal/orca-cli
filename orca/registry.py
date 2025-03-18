"""
Functions for interacting with the Ollama registry.
"""
import requests
from bs4 import BeautifulSoup
from rich.progress import Progress, SpinnerColumn, TextColumn


def search_models(query):
    """
    Search the Ollama registry for models matching the query.

    Args:
        query: Search term

    Returns:
        List of model names matching the search
    """
    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
    ) as progress:
        progress.add_task(description=f"Querying Ollama Registry for {query}...", total=None)
        response = requests.get(f"https://ollama.com/search?q={query}")
        soup = BeautifulSoup(response.content, features="html.parser")
        models = []
        for a in soup.select('li.flex > a:nth-child(1) > div:nth-child(1) > h2:nth-child(1)'):
            models.append(a.text.strip())

    return models


def get_model_tags(selected_model):
    """
    Get available tags for a specific model.

    Args:
        selected_model: The model to get tags for

    Returns:
        List of available tags
    """
    if "/" in selected_model:
        url = f"https://ollama.com/{selected_model}/tags"
    else:
        url = f"https://ollama.com/library/{selected_model}/tags"

    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
    ) as progress:
        progress.add_task(description=f"Querying Ollama Registry for {selected_model} tags...", total=None)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, features="html.parser")
        tags = []
        for a in soup.select(
                'body > main > div > section > div > div > div > div > div.flex.space-x-2.items-center > a > div'):
            tags.append(a.text.strip())

    return tags