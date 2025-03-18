"""
Functions for downloading model files from Ollama registry.
"""
import os
import json
import time
import random
import requests
import threading
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn

# Constants similar to the Go implementation
NUM_DOWNLOAD_PARTS = 8
MIN_DOWNLOAD_PART_SIZE = 100 * 1024 * 1024  # 100 MB
MAX_DOWNLOAD_PART_SIZE = 1000 * 1024 * 1024  # 1000 MB
MAX_RETRIES = 6


class BlobDownloader:
    """
    Class to handle downloading large GGUF files in chunks with progress tracking.
    """

    def __init__(self, url, output_path):
        self.url = url
        self.output_path = output_path
        self.total_size = 0
        self.completed = 0
        self.parts = []
        self.done_event = threading.Event()
        self.error = None

    def prepare(self):
        """Initialize the download by determining file size and creating parts"""
        # Get file size with HEAD request
        response = requests.head(self.url)
        self.total_size = int(response.headers.get('Content-Length', 0))

        if self.total_size == 0:
            raise ValueError("Could not determine file size")

        # Calculate part size
        part_size = self.total_size // NUM_DOWNLOAD_PARTS
        if part_size < MIN_DOWNLOAD_PART_SIZE:
            part_size = MIN_DOWNLOAD_PART_SIZE
        elif part_size > MAX_DOWNLOAD_PART_SIZE:
            part_size = MAX_DOWNLOAD_PART_SIZE

        # Create parts
        offset = 0
        part_num = 0
        while offset < self.total_size:
            size = min(part_size, self.total_size - offset)
            self.parts.append({
                'n': part_num,
                'offset': offset,
                'size': size,
                'completed': 0,
                'last_updated': None
            })
            offset += size
            part_num += 1

        # Create output file with correct size
        with open(self.output_path, 'wb') as f:
            f.seek(self.total_size - 1)
            f.write(b'\0')

        print(f"Downloading file in {len(self.parts)} parts")
        return self.total_size

    def download_part(self, part):
        """Download a specific part of the file"""
        for retry in range(MAX_RETRIES):
            try:
                start = part['offset'] + part['completed']
                end = part['offset'] + part['size'] - 1

                headers = {'Range': f'bytes={start}-{end}'}
                response = requests.get(self.url, headers=headers, stream=True)

                with open(self.output_path, 'r+b') as f:
                    f.seek(start)
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            part['completed'] += len(chunk)
                            self.completed += len(chunk)
                            part['last_updated'] = time.time()

                return True
            except Exception as e:
                if retry < MAX_RETRIES - 1:
                    sleep_time = 2 ** retry
                    print(f"Part {part['n']} failed: {e}, retrying in {sleep_time}s")
                    time.sleep(sleep_time)
                else:
                    self.error = f"Failed to download part {part['n']}: {e}"
                    return False

        return False

    def download(self):
        """Download the file with progress tracking"""
        try:
            self.prepare()

            with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    TaskProgressColumn(),
                    TimeRemainingColumn(),
            ) as progress:
                task = progress.add_task(f"Downloading GGUF file...", total=self.total_size)

                # Create and start download threads
                threads = []
                for part in self.parts:
                    thread = threading.Thread(target=self.download_part, args=(part,))
                    thread.start()
                    threads.append(thread)

                # Update progress while downloading
                while any(thread.is_alive() for thread in threads):
                    progress.update(task, completed=self.completed)
                    if self.error:
                        raise Exception(self.error)
                    time.sleep(0.1)

                # Final update
                progress.update(task, completed=self.total_size)

            print(f"[bold green]Download complete: {self.output_path}[/bold green]")
            return True

        except Exception as e:
            print(f"[bold red]Download failed: {str(e)}[/bold red]")
            # Clean up partial download
            if os.path.exists(self.output_path):
                os.remove(self.output_path)
            return False


def export_gguf(model_name, tag, output_path):
    """
    Export a GGUF file from an Ollama model.

    Args:
        model_name: Name of the model
        tag: Tag of the model
        output_path: Path to save the GGUF file

    Returns:
        bool: True if successful, False otherwise
    """
    # Construct the URL for the GGUF file
    if "/" in model_name:
        url = f"https://ollama.com/{model_name}:{tag}/blob"
    else:
        url = f"https://ollama.com/library/{model_name}:{tag}/blob"

    print(f"Exporting GGUF file for [bold]{model_name}:{tag}[/bold]")

    # Create the downloader and start the download
    downloader = BlobDownloader(url, output_path)
    return downloader.download()