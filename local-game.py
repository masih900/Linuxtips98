#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.progress import track, Progress, SpinnerColumn, TextColumn
from rich.table import Table
import os
import re
import urllib.parse
import json
import time
import threading
import sys
import http.server
import socketserver

console = Console()
server_running = True

def download_game(url, game_name):
    game_dir = os.path.join("playhop_games", game_name)
    os.makedirs(game_dir, exist_ok=True)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124"}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        with open(os.path.join(game_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(response.text)
        assets = set()
        for tag in soup.find_all(["script", "link", "img"]):
            src = tag.get("src") or tag.get("href")
            if src and not src.startswith("http"):
                assets.add(src)
        for asset in assets:
            asset_url = urllib.parse.urljoin(url, asset)
            asset_path = os.path.join(game_dir, asset.lstrip("/"))
            os.makedirs(os.path.dirname(asset_path), exist_ok=True)
            try:
                asset_response = requests.get(asset_url, headers=headers, timeout=15)
                with open(asset_path, "wb") as f:
                    f.write(asset_response.content)
            except Exception as e:
                console.print(f"[bold red]Error downloading asset {asset}: {str(e)}[/bold red]")
                with open("error_log.txt", "a") as log:
                    log.write(f"{time.ctime()}: Error downloading asset {asset} - {str(e)}\n")
        game_data = {"name": game_name, "url": url, "dir": game_dir}
        with open("playhop_games.json", "a") as f:
            json.dump(game_data, f)
            f.write("\n")
        console.print(f"[bold green]Game {game_name} downloaded successfully![/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error downloading game {game_name}: {str(e)}[/bold red]")
        with open("error_log.txt", "a") as log:
            log.write(f"{time.ctime()}: Error downloading game {game_name} - {str(e)}\n")

def list_games():
    games = []
    if os.path.exists("playhop_games.json"):
        with open("playhop_games.json", "r") as f:
            for line in f:
                if line.strip():
                    games.append(json.loads(line))
    return games

def show_games():
    games = list_games()
    if not games:
        console.print("[bold yellow]No games downloaded yet.[/bold yellow]")
        return
    table = Table(title="Downloaded Games")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("URL", style="blue")
    for idx, game in enumerate(games, 1):
        table.add_row(str(idx), game["name"], game["url"])
    console.print(table)

def start_server(game_dir):
    os.chdir(game_dir)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", 8080), handler) as httpd:
        console.print("[bold green]Server running at http://localhost:8080[/bold green]")
        httpd.serve_forever()

def check_shutdown():
    global server_running
    console.print("[bold blue]Type 'q' and press Enter to stop the server[/bold blue]")
    while server_running:
        try:
            if input().lower() == 'q':
                server_running = False
                console.print("[bold yellow]Shutting down server...[/bold yellow]")
                sys.exit(0)
        except:
            time.sleep(1)

def main():
    console.print("[bold yellow]🌐 Playhop Game Downloader 🌐[/bold yellow]")
    os.makedirs("playhop_games", exist_ok=True)
    while True:
        console.print("[bold cyan]Options:[/bold cyan]")
        console.print("1. Download a new game")
        console.print("2. Run server = 01")
        console.print("q. Quit")
        choice = input("Enter choice: ").strip().lower()
        if choice == "q":
            console.print("[bold yellow]Exiting...[/bold yellow]")
            break
        elif choice == "1":
            console.print("[bold cyan]Enter Playhop game URL (e.g., https://playhop.com/game/solitaire):[/bold cyan]")
            url = input().strip()
            console.print("[bold cyan]Enter game name (e.g., Solitaire):[/bold cyan]")
            game_name = input().strip()
            game_name = re.sub(r"[^\w\-]", "_", game_name)
            with Progress(SpinnerColumn(), TextColumn("[cyan]Downloading {task.description}..."), transient=True) as progress:
                progress.add_task(game_name)
                download_game(url, game_name)
        elif choice == "2":
            console.print("[bold green]run server = 01[/bold green]")
            show_games()
            games = list_games()
            if games:
                console.print("[bold cyan]Enter game ID to run (or 'q' to go back):[/bold cyan]")
                game_id = input().strip()
                if game_id.lower() == "q":
                    continue
                try:
                    game_idx = int(game_id) - 1
                    if 0 <= game_idx < len(games):
                        game_dir = games[game_idx]["dir"]
                        threading.Thread(target=start_server, args=(game_dir,), daemon=True).start()
                        threading.Thread(target=check_shutdown).start()
                        while server_running:
                            time.sleep(1)
                    else:
                        console.print("[bold red]Invalid game ID.[/bold red]")
                except ValueError:
                    console.print("[bold red]Invalid input. Enter a number.[/bold red]")
        else:
            console.print("[bold red]Invalid choice.[/bold red]")

if __name__ == "__main__":
    main()
