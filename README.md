# ORCA: Ollama Registry CLI Application

ORCA is a command-line interface application that allows you to search, explore, and manage models from the Ollama Registry. It provides an intuitive interface for discovering models, viewing their tags, and pulling them to your local Ollama installation.

## Features

- Search the Ollama Registry for models
- View available tags for models
- Pull models directly to your local Ollama installation
- Open model pages in your browser for more information

## Installation

### Prerequisites

- Python 3.10 or higher
- Ollama installed on your system

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/molbal/orca.git
   cd orca
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Commands

Search for models:
```bash
python main.py search gemma3
```

If you run the search command without arguments, you'll be prompted to enter a search term:
```bash
python main.py search
```

### CLI Interface

ORCA provides a CLI interface that allows you to:

1. Select a model from search results
2. Choose actions for a model:
   - Pull the model to your local Ollama installation
   - View available tags
   - Open the model page in your browser
3. Select specific tags and perform actions on them

## Project Structure

- `main.py`: Entry point for the application
- `models.py`: Functions for handling Ollama model operations
- `browser.py`: Functions for browser interactions
- `ui.py`: User interface functions
- `registry.py`: Functions for interacting with the Ollama registry

## Dependencies

- `typer`: Command-line interface creation
- `rich`: Rich text and formatting in the terminal
- `inquirer`: Interactive command-line user interfaces
- `requests`: HTTP requests to the Ollama Registry
- `beautifulsoup4`: HTML parsing for registry data

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add some new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## License

This project is licensed under the Apache - see the LICENSE file for details.

## Acknowledgments

- [Ollama](https://ollama.com/) for providing the registry and models
- All the open-source projects that make ORCA possible

---

*ORCA is not officially affiliated with Ollama.*