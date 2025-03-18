from setuptools import setup, find_packages

setup(
    name="orca",
    version="1.0.0",
    description="ORCA: Ollama Registry CLI Application",
    author="Balint Molnar-Kalo",
    packages=find_packages(),
    install_requires=[
        "typer[all]",
        "rich",
        "inquirer",
        "requests",
        "beautifulsoup4",
    ],
    entry_points={
        "console_scripts": [
            "orca=orca.main:app",
        ],
    },
)
