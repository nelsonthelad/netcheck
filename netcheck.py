import requests
import socket
import speedtest
from rich import print
from rich.panel import Panel
from rich.live import Live
from rich.spinner import Spinner

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

# Handles speed test UI
def getSpeedTestPanel(ping, download_speed, upload_speed, status):
    pingString = f"Ping: [bold green]{ping} ms[/bold green]"
    downloadString = f"Download Speed: [bold green]{download_speed} Mbps[/bold green]"
    uploadString = f"Upload Speed: [bold green]{upload_speed} Mbps[/bold green]"
    statusString = f"Status: [bold yellow]{status}[/bold yellow]"

    bgColor = "blue"

    if ping == None:
        pingString = f"Ping: [bold red]Loading...[/bold red]"
    if download_speed == None:
        downloadString = f"Download Speed: [bold red]Loading...[/bold red]"
    if upload_speed == None:
        uploadString = f"Upload Speed: [bold red]Loading...[/bold red]"

    if status == "Complete":
        bgColor = "green"
        statusString = f"Status: [bold green]Complete[/bold green]"
        
    return Panel(
        statusString + "\n" + "\n" + pingString + "\n" + downloadString + "\n" + uploadString,
        title="Network Speed Test",
        border_style=bgColor
    )

# Performs a network speed test with live updates
def runSpeedTest(): 
    try:
        st = speedtest.Speedtest()
        st.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

        with Live(getSpeedTestPanel(None, None, None, "Testing Ping..."), refresh_per_second=4) as live:
            st.get_best_server()
            ping = f"{st.results.ping:.2f}"
            livePanel = getSpeedTestPanel(ping, None, None, "Testing Download...")
            live.update(livePanel)

            download_speed = f"{(st.download() / 1_000_000):.2f}"
            livePanel = getSpeedTestPanel(ping, download_speed, None, "Testing Upload...")
            live.update(livePanel)
            
            upload_speed = f"{(st.upload() / 1_000_000):.2f}"
            livePanel = getSpeedTestPanel(ping, download_speed, upload_speed, "Complete")
            live.update(livePanel)
    except Exception as e:
        errorPanel = Panel(f"Error: [bold red]{e}[/bold red]", title="Network Speed Test", border_style="red")
        print(errorPanel)

        if e.args[0] == "HTTP Error 403: Forbidden":
            print("Server is busy, please try again later.")

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

    # Run speed test
    runSpeedTest()

if __name__ == "__main__":
    main()