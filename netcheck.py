import requests
import socket
import subprocess
from rich import print
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

# Checks if there is an internet connection
def checkConnection():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False    

# Gets the local IP address
def getLocalIp():
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
    except:
        local_ip = "Error"
    return local_ip

# Gets the public IP address
def getPublicIp():
    try:
        public_ip = requests.get("https://api.ipify.org?format=json").json()["ip"]
    except:
        public_ip = "Error"
    return public_ip

# Performs a network speed test with live updates
def runSpeedTest():
    # Create a table for results
    table = Table(title="Network Speed Test Results")
    table.add_column("Test", style="cyan")
    table.add_column("Speed", style="green")
    
    # Create progress displays
    download_progress = Progress(
        SpinnerColumn(),
        TextColumn("[bold green]Testing download speed...[/bold green]"),
        transient=True
    )
    
    upload_progress = Progress(
        SpinnerColumn(),
        TextColumn("[bold green]Testing upload speed...[/bold green]"),
        transient=True
    )
    
    try:
        # Run speedtest-cli to get server information
        print("[bold yellow]Finding best server...[/bold yellow]")
        server_result = subprocess.run(
            ["speedtest-cli", "--list"],
            capture_output=True,
            text=True,
            check=True
        )
        print("[bold green]Server found![/bold green]")
        
        # Test download speed with live updates
        with Live(download_progress) as live:
            download_task = download_progress.add_task("download", total=None)
            download_result = subprocess.run(
                ["speedtest-cli", "--no-upload", "--simple"],
                capture_output=True,
                text=True,
                check=True
            )
            download_progress.update(download_task, completed=True)
        
        # Parse download result
        download_output = download_result.stdout
        download_speed = None
        for line in download_output.splitlines():
            if "Download" in line:
                download_speed = float(line.split(":")[1].strip().split(" ")[0])
                break
        
        # Test upload speed with live updates
        with Live(upload_progress) as live:
            upload_task = upload_progress.add_task("upload", total=None)
            upload_result = subprocess.run(
                ["speedtest-cli", "--no-download", "--simple"],
                capture_output=True,
                text=True,
                check=True
            )
            upload_progress.update(upload_task, completed=True)
        
        # Parse upload result
        upload_output = upload_result.stdout
        upload_speed = None
        ping = None
        for line in upload_output.splitlines():
            if "Upload" in line:
                upload_speed = float(line.split(":")[1].strip().split(" ")[0])
            if "Ping" in line:
                ping = float(line.split(":")[1].strip().split(" ")[0])
        
        # Add results to the table
        if download_speed is not None:
            table.add_row("Download", f"[bold green]{download_speed:.2f} Mbps[/bold green]")
        else:
            table.add_row("Download", "[bold red]Failed to get download speed[/bold red]")
            
        if upload_speed is not None:
            table.add_row("Upload", f"[bold green]{upload_speed:.2f} Mbps[/bold green]")
        else:
            table.add_row("Upload", "[bold red]Failed to get upload speed[/bold red]")
            
        if ping is not None:
            table.add_row("Ping", f"[bold green]{ping:.2f} ms[/bold green]")
        else:
            table.add_row("Ping", "[bold red]Failed to get ping[/bold red]")
        
    except subprocess.CalledProcessError as e:
        print(f"[bold red]Error running speed test: {e}[/bold red]")
        table.add_row("Error", f"[bold red]Failed to run speed test[/bold red]")
    except Exception as e:
        print(f"[bold red]Unexpected error: {e}[/bold red]")
        table.add_row("Error", f"[bold red]{str(e)}[/bold red]")
    
    return table

# Main function
def main():
    if not checkConnection():
        print("No internet connection")
        return

    # Get and print the local and public IP addresses
    local_ip = getLocalIp()
    public_ip = getPublicIp()

    ipPanel = Panel(
        f"Local IP: [bold green]{local_ip}[/bold green]\nPublic IP: [bold green]{public_ip}[/bold green]",
        title="Internet Status: [bold green]Connected[/bold green]",
        border_style="green"
    )
    print(ipPanel)
    
    speed_table = runSpeedTest()
    print(speed_table)

if __name__ == "__main__":
    main()