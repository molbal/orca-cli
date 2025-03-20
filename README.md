# ORCA: Ollama Registry CLI Application

ORCA is a command-line interface application that allows you to search, explore, and download models from the Ollama Registry. It provides an intuitive interface for discovering models, viewing their tags, and pulling them to your local Ollama installation.

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

### CLI Commands

ORCA provides the following commands:

#### Search for models
```bash
python main.py search [QUERY]
```
- If no query is provided, you'll be prompted to enter a search term interactively.

Example:
```bash
python main.py search gemma3
```

#### Download a model
```bash
python main.py download [MODEL_NAME] [TAG] [FILE_NAME] [DIRECTORY]
```
- Downloads a specific model tag to the specified file and directory.

Example:
```bash
python main.py download llama3.2 1b model.gguf .
```

### Getting Help
You can always get help by using:
```bash
python main.py --help
```


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

- [Ollama](https://ollama.com/) for hosting the registry
- All the open-source projects that make ORCA possible

---

*ORCA is not officially affiliated with Ollama.*
