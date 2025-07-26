#!/usr/bin/env python3

import requests
from flask import Flask, request, Response
from rich.console import Console
from rich.progress import track, Progress, SpinnerColumn, TextColumn
from bs4 import BeautifulSoup
import time
import warnings
import threading
import sys
import socket
import os

os.environ["FLASK_ENV"] = "production"
warnings.filterwarnings("ignore")

console = Console()
app = Flask(__name__)
server_running = True

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def get_proxies():
    try:
        response = requests.get("https://advanced.name/freeproxy", headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table")
        proxies = []
        for row in table.find_all("tr")[1:30]:
            cols = row.find_all("td")
            if len(cols) > 1:
                ip = cols[0].text
                port = cols[1].text
                protocol = cols[2].text.lower()
                if "https" in protocol:
                    proxies.append(f"http://{ip}:{port}")
        return proxies
    except Exception as e:
        console.print(f"[bold red]Error fetching proxies: {str(e)}[/bold red]")
        with open("error_log.txt", "a") as log:
            log.write(f"{time.ctime()}: Error fetching proxies - {str(e)}\n")
        return []

def test_proxy(proxy):
    try:
        response = requests.get("https://www.youtube.com/", proxies={"http": proxy, "https": proxy}, timeout=5)
        return response.status_code == 200
    except:
        return False

def fetch_youtube(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    proxies = get_proxies()
    if not proxies:
        console.print("[bold red]Error: No proxies available[/bold red]")
        with open("error_log.txt", "a") as log:
            log.write(f"{time.ctime()}: No proxies available\n")
        return None
    for proxy in proxies:
        console.print(f"[bold yellow]Testing proxy: {proxy}[/bold yellow]")
        if test_proxy(proxy):
            try:
                response = requests.get(url, headers=headers, proxies={"http": proxy, "https": proxy}, timeout=15, verify=False)
                response.raise_for_status()
                return response.text
            except requests.exceptions.RequestException as e:
                console.print(f"[bold red]Proxy failed: {proxy} - {str(e)}[/bold red]")
                with open("error_log.txt", "a") as log:
                    log.write(f"{time.ctime()}: Proxy {proxy} failed - {str(e)}\n")
                continue
    console.print("[bold red]Error: No working proxy found[/bold red]")
    with open("error_log.txt", "a") as log:
        log.write(f"{time.ctime()}: No working proxy found\n")
    return None

@app.route('/')
@app.route('/<path:path>')
def proxy(path=""):
    console.print("[bold cyan]Processing YouTube request...[/bold cyan]")
    youtube_url = f"https://www.youtube.com/{path}" if path else "https://www.youtube.com/"
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True
    ) as progress:
        task = progress.add_task("[cyan]Fetching YouTube...", total=None)
        content = fetch_youtube(youtube_url)
    if content:
        console.print("[bold green]Success! YouTube loaded![/bold green]")
        return Response(content, mimetype='text/html')
    else:
        return Response("Error: Could not fetch YouTube. Check error_log.txt.", status=500)

@app.route('/shutdown')
def shutdown():
    global server_running
    server_running = False
    console.print("[bold yellow]Shutting down server...[/bold yellow]")
    threading.Thread(target=lambda: time.sleep(1) or sys.exit(0)).start()
    return Response("Server is shutting down...", status=200)

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
    console.print("[bold yellow]🌐 YouTube Proxy Server 🌐[/bold yellow]")
    local_ip = get_local_ip()
    console.print(f"[bold green]Access YouTube at: http://{local_ip}:8080 or http://localhost:8080[/bold green]")
    for _ in track(range(100), description="[cyan]Starting server..."):
        time.sleep(0.02)
    threading.Thread(target=check_shutdown).start()
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    main()
