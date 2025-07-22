#!/usr/bin/env python3

import requests
from rich.console import Console
from rich.table import Table
from rich.progress import track
import time
import os

console = Console()

def download_tip(url, output_file):
    try:
        console.print(f"[bold cyan]Downloading tip from {url}...[/bold cyan]")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        file_size = os.path.getsize(output_file) / 1024
        console.print(f"[bold green]Success! Tip saved to {output_file} (Size: {file_size:.2f} KB)[/bold green]")
        
        table = Table(title="Tips Downloader Summary", show_header=True, header_style="bold magenta")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        table.add_row("URL", url)
        table.add_row("Output File", output_file)
        table.add_row("Size (KB)", f"{file_size:.2f}")
        table.add_row("Status", "Completed")
        console.print(table)
        
    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        return False
    return True

def main():
    console.print("[bold yellow]🌟 Tips Downloader 🌟[/bold yellow]")
    url = console.input("[bold blue]Enter website URL (e.g., https://example.com): [/bold blue]")
    output_file = f"tip_{int(time.time())}.html"
    
    for _ in track(range(100), description="Initializing..."):
        time.sleep(0.02)
    
    download_tip(url, output_file)

if __name__ == "__main__":
    main()
