import speedtest
import requests
import socket

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

# Main function
def main():
    print("Checking Internet Connection...")

    if not checkConnection():
        print("No internet connection")
        return
    
    print("Internet Status: Connected")
    print("Getting local IP address...")
    local_ip = getLocalIp()
    print(f"Local IP address: {local_ip}")

    print("Getting public IP address...")
    public_ip = getPublicIp()
    print(f"Public IP address: {public_ip}")
    
    

if __name__ == "__main__":
    main()