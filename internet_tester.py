#!/usr/bin/env python3

import speedtest
import warnings
from rich.console import Console
from rich.table import Table
from rich.progress import track, Progress, SpinnerColumn, TextColumn
import time

warnings.filterwarnings("ignore")

console = Console()

def test_internet():
    try:
        console.print("[bold yellow]🌐 Internet Speed Tester 🌐[/bold yellow]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True
        ) as progress:
            task = progress.add_task("[cyan]Testing internet speed...", total=None)
            st = speedtest.Speedtest()
            st.config['http_headers'] = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            progress.update(task, description="[cyan]Selecting best server...")
            try:
                st.get_best_server()
            except speedtest.SpeedtestBestServerFailure:
                console.print("[bold yellow]Warning: Could not find best server. Using default server...[/bold yellow]")
                st.get_servers()
            
            progress.update(task, description="[cyan]Testing download speed...")
            download_speed = st.download() / 1_000_000
            progress.update(task, description="[cyan]Testing upload speed...")
            upload_speed = st.upload() / 1_000_000
            ping = st.results.ping
            
        console.print("[bold green]Test completed successfully![/bold green]")
        
        table = Table(title="Internet Speed Test Results", show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        table.add_row("Download Speed", f"{download_speed:.2f} Mbps")
        table.add_row("Upload Speed", f"{upload_speed:.2f} Mbps")
        table.add_row("Ping", f"{ping:.2f} ms")
        table.add_row("Timestamp", time.ctime())
        console.print(table)
        
        return True
    
    except speedtest.HTTPError as http_err:
        console.print(f"[bold red]HTTP Error: {str(http_err)}. Server blocked the request (403 Forbidden). Try again or check network settings.[/bold red]")
        with open("error_log.txt", "a") as log:
            log.write(f"{time.ctime()}: HTTP Error - {str(http_err)}\n")
        return False
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}. Check your connection or try again.[/bold red]")
        with open("error_log.txt", "a") as log:
            log.write(f"{time.ctime()}: Error - {str(e)}\n")
        return False

def main():
    for _ in track(range(100), description="[cyan]Initializing tester..."):
        time.sleep(0.02)
    test_internet()

if __name__ == "__main__":
    main()
