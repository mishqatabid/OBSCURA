import socket
import subprocess
import os
import signal
import time

def kill_existing_process(port):
    """Kill the process running on the specified port."""
    try:
        result = subprocess.run(
            ["lsof", "-ti", f":{port}"],
            capture_output=True,
            text=True
        )
        pids = result.stdout.strip().splitlines()
        
        for pid in pids:
            os.kill(int(pid), signal.SIGTERM)  # Terminate the process
            print(f"Killed process with PID: {pid} on port: {port}")
            time.sleep(1)  # Wait for the process to terminate
            if os.path.exists(f"/proc/{pid}"):
                os.kill(int(pid), signal.SIGKILL)  # Force kill if still running
                print(f"Forcefully killed process with PID: {pid} on port: {port}")

    except Exception as e:
        print(f"Error killing process on port {port}: {e}")

def is_port_open(port):
    """Check if the specified port is open."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def start_service(port, service_name, service_version):
    """Start a simple TCP server that pretends to run the specified service."""
    while is_port_open(port):
        print(f"Waiting for port {port} to be free...")
        time.sleep(1)  # Wait for a second before checking again

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('0.0.0.0', port))
            s.listen(1)
            print(f"{service_name} {service_version} is now running on port {port}...")

            try:
                while True:
                    conn, addr = s.accept()
                    with conn:
                        print(f"Connection from {addr} established.")
                        # Send a fake banner to the client using the user-defined service version
                        if service_name.lower() == "http":
                            banner = (f"HTTP/1.1 200 OK\r\n"
                                       f"Server: Apache/{service_version} (Ubuntu)\r\n"
                                       "Date: Sat, 29 Sep 2024 12:00:00 GMT\r\n"
                                       "Content-Type: text/html; charset=UTF-8\r\n"
                                       "Content-Length: 71\r\n"
                                       "Connection: close\r\n\r\n"
                                       "<html><body><h1>Welcome to the Fake HTTP Server!</h1></body></html>")
                        elif service_name.lower() == "ftp":
                            banner = f"220 (vsFTPd {service_version})\r\n"
                        elif service_name.lower() == "smtp":
                            banner = f"220 mail.example.com ESMTP Postfix ({service_version})\r\n"
                        elif service_name.lower() == "pop3":
                            banner = f"+OK POP3 server ready\r\n"
                        elif service_name.lower() == "ssh":
                            banner = f"SSH-2.0-OpenSSH_{service_version}\r\n"
                        else:
                            banner = "Unknown service\r\n"

                        conn.sendall(banner.encode())

                        # Wait for a short period to allow the client to receive the banner
                        time.sleep(0.5)

            except KeyboardInterrupt:
                print("Service stopped.")
    except OSError as e:
        print(f"Error starting service on port {port}: {e}")

def main():

    print_ascii_art()
    
    # Get user input for port number, service name, and service version
    port = int(input("[+] ENTER PORT NUMBER: "))
    service_name = input("[+] ENTER SERVICE NAME \r\n"
                         "         [1] HTTP \r\n"
                         "         [2] SMTP \r\n"
                         "         [3] POP3 \r\n"
                         "         [4] SSH \r\n")
    service_version = input("[+] ENTER SERVICE VERSION: ")
    
    # Kill existing process on the port if necessary
    kill_existing_process(port)

    # Start the spoofed service
    start_service(port, service_name, service_version)
    
def print_ascii_art():
    art = r"""
    ▒█████   ▄▄▄▄     ██████  ▄████▄   █    ██  ██▀███   ▄▄▄      
    ▒██▒  ██▒▓█████▄ ▒██    ▒ ▒██▀ ▀█   ██  ▓██▒▓██ ▒ ██▒▒████▄    
    ▒██░  ██▒▒██▒ ▄██░ ▓██▄   ▒▓█    ─ ▓██  ▒██░▓██ ░▄█ ▒▒██  ▀█▄  
    ▒██   ██░▒██░█▀    ▒   ██▒▒▓▓▄ ▄██▒▓▓█  ░██░▒██▀▀█▄  ░██▄▄▄▄██ 
    ░ ████▓▒░░▓█  ▀█▓▒██████▒▒▒ ▓███▀ ░▒▒█████▓ ░██▓ ▒██▒ ▓█   ▓██▒
    ░ ▒░▒░▒░ ░▒▓███▀▒▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░░▒▓▒ ▒ ▒ ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░
      ░ ▒ ▒░ ▒░▒   ░ ░ ░▒  ░ ░  ░  ▒   ░░▒░ ░ ░   ░▒ ░ ▒░  ▒   ▒▒ ░
    ░ ░ ░ ▒   ░    ░ ░  ░  ░  ░         ░░░ ░ ░   ░░   ░   ░   ▒   
        ░ ░   ░            ░  ░ ░         ░        ░           ░  ░
                   ░          ░                                    
    """
    print(art)

if __name__ == "__main__":
    main()
