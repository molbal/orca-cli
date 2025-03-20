# ORCA: Ollama Registry CLI Application

ORCA is a command-line interface application that allows you to search, explore, and download models from the Ollama 
Registry. It provides an intuitive interface for discovering models, viewing their tags, and pulling them to your local 
Ollama installation.

## Features

- Search the Ollama Registry for models
- View available tags for models
- Pull models directly to your local Ollama installation
- Open model pages in your browser for more information

## Usage
You will need Python 3.10 installed. 
```bash
pip install orca-cli
```

Then you can call the tool via the **orca-cli** command

```bash
>orca-cli

 Usage: orca-cli [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.          │
│ --show-completion             Show completion for the current shell, to copy it  │
│                               or customize the installation.                     │
│ --help                        Show this message and exit.                        │
╰──────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────╮
│ search     Searches the Ollama Registry for a model.                             │
│ download   Downloads a model from Ollama Registry to the specified location. For │
│            example the following command downloads llama3.2:1b as model.gguf to  │
│            the current working directory.: `orca-cli llama3.2 1b model.gguf .`   │
╰──────────────────────────────────────────────────────────────────────────────────╯
```


### CLI Commands

ORCA provides the following commands:

#### Search for models
```bash
orca-cli search [QUERY]
```
If no query is provided, you'll be prompted to enter a search term interactively.

Example:
```bash
orca-cli search gemma3
```

#### Download a model
```bash
orca-cli download [MODEL_NAME] [TAG] [FILE_NAME] [DIRECTORY]
```
- Downloads a specific model tag to the specified file and directory.
- If the Ollama Registry contains an adapter alongside the base model, orca-cli will override the given filename and add
`-base` and `-adapter` postfixes to the filename.

Example:
```bash
orca-cli download llama3.2 1b model.gguf .
``` 
--- 
## Installation from the repository

### Prerequisites

- Python 3.10 or higher
- Ollama installed on your system

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/molbal/orca.git
   cd orca
   ```

2. Create virtual environment if you want, then install the required dependencies:
   ```bash
   pip install -r requirements.txt
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

- [Ollama](https://ollama.com/), obviously
- All the open-source projects that make ORCA possible

---

*ORCA is not officially affiliated with Ollama.*
