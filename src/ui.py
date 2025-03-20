"""
User interface functions for ORCA.
"""
import os
import inquirer
from rich import print
from .models import pull_model
from .browser import open_browser, read_modelfile
from .downloader import download_model
from .registry import get_model_tags

def prompt_model_action(selected_model):
    """
    Prompt the user for actions to perform on a selected model.

    Args:
        selected_model: The model to perform actions on
    """
    questions = [inquirer.List('action',
                               message=f"What do you want to do with {selected_model}?",
                               choices=['pull', 'view tags', 'read modelfile', 'open in browser', 'export gguf', '<- back', '<- exit'],
                               )]
    answers = inquirer.prompt(questions)
    if answers is None:
        return

    match answers['action']:
        case 'pull':
            pull_model(selected_model)
        case 'view tags':
            view_tags(selected_model)
        case 'open in browser':
            open_browser(selected_model)
        case 'read modelfile':
            read_modelfile(selected_model)
        case 'export gguf':
            export_model_gguf(selected_model)
        case '<- back':
            pass
        case '<- exit':
            pass
        case _:
            pass

def prompt_model_tag_action(selected_model, tags, selected_action=None):
    """
    Prompt the user for actions on a specific model tag.

    Args:
        selected_model: The model to perform actions on
        tags: List of available tags for the model
        :param selected_action: Unless this is set, a selector will be displayed.
    """
    tags_select = tags.copy()
    tags_select.append('<- back')
    questions = [inquirer.List('tag',
                               message="Select a tag from the results",
                               choices=tags_select,
                               )]
    answers = inquirer.prompt(questions)
    if answers is None:
        return

    selected_tag = answers['tag']
    if selected_tag == '<- back':
        prompt_model_action(selected_model)
        return

    print(f"The selected tag is {selected_tag}")

    if selected_action is None:
        questions = [inquirer.List('action',
                                   message=f"What to do with {selected_model}:{selected_tag}?",
                                   choices=['pull', 'open in browser', 'export gguf', '<- select another tag'],
                                   )]
        answers = inquirer.prompt(questions)
        if answers is None:
            return
        selected_action = answers['action']

    match selected_action:
        case 'pull':
            pull_model(f"{selected_model}:{selected_tag}")
        case 'open in browser':
            open_browser(f"{selected_model}:{selected_tag}")
        case 'export gguf':
            export_tag_gguf(selected_model, selected_tag)
        case '<- select another tag':
            prompt_model_tag_action(selected_model, tags)
        case _:
            pass


def view_tags(selected_model):
    """
    View and interact with tags for a selected model.

    Args:
        selected_model: The model to view tags for
    """
    tags = get_model_tags(selected_model)
    prompt_model_tag_action(selected_model, tags)

def export_model_gguf(selected_model):
    """
    Export a GGUF file for a model by first selecting a tag.

    Args:
        selected_model: The model to export
    """
    tags = get_model_tags(selected_model)
    if not tags:
        print("[bold orange]Warning:[/bold orange] No tags found for this model")
        return

    prompt_model_tag_action(selected_model, tags, selected_action="export gguf")



def export_tag_gguf(selected_model, selected_tag, filename="", directory="."):
    """
    Export a GGUF file for a specific model tag.

    Args:
        selected_model: The model to export
        selected_tag: The tag to export
    """

    if filename=="" and directory==".":
        # Get default filename
        default_filename = f"{selected_model.split('/')[-1]}-{selected_tag}.gguf"

        # Ask for output location
        questions = [
            inquirer.Text('filename',
                         message="Enter output filename",
                         default=default_filename),
            inquirer.Path('directory',
                         message="Enter output directory",
                         path_type=inquirer.Path.DIRECTORY,
                         default=os.getcwd(),
                         exists=True)
        ]

        answers = inquirer.prompt(questions)
        if answers is None:
            return

        output_path = os.path.join(answers['directory'], answers['filename'])
    else:
        output_path = os.path.join(directory, filename)

    # Confirm if file exists
    if os.path.exists(output_path):
        questions = [inquirer.Confirm('overwrite',
                                     message=f"File {output_path} already exists. Overwrite?",
                                     default=False)]
        answers = inquirer.prompt(questions)
        if answers is None or not answers['overwrite']:
            print("Export cancelled")
            return

    # Download the GGUF file
    success = download_model(selected_model, selected_tag, output_path)

    if success:
        print(f"[bold green]Success:[/bold green] GGUF file exported to: {output_path}")
    else:
        print("[bold red]Error:[/bold red] Failed to export GGUF file")


def prompt_model_selector(models, query=""):
    """
    Prompt the user to select a model from search results.

    Args:
        models: List of model names to choose from
        query: The search query that was used (for context)

    Returns:
        The selected model name or None if canceled
    """
    questions = [inquirer.List('model',
                               message="Select a model from the results",
                               choices=models,
                               )]

    answers = inquirer.prompt(questions)
    if answers is None:
        return ""
    return answers['model']