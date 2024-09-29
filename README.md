# OBSCURA - Port Spoofing Tool
This Python-based tool simulates common network services such as HTTP, SMTP, POP3, SSH, and more. It allows you to start a fake service on any specified port, sending custom service banners to any client connecting to the service. This is useful for network testing, honeypot setups, or security research.

## Features
- **Kill Existing Processes**: Automatically kills any process running on the selected port.
- **Simulate Various Services**: Mimic HTTP, SMTP, FTP, POP3, or SSH services, responding with realistic banners.
- **Customizable Service Versions**: Specify the version of the service being simulated, e.g., `Apache/2.4.41`, `Postfix/3.4.13`, etc.
- **Simple and Easy to Use**: Command-line tool with intuitive prompts for input.

## Requirements
- Python 3.x
- Linux/macOS (for the `lsof` command to detect processes on the port)
- The following Python modules:
  - `socket`
  - `subprocess`
  - `os`
  - `signal`
  - `time`

## Installation
Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/mishqatabid/OBSCURA.git
cd OBSCURA
```

Ensure Python 3.x is installed:

```bash
python3 --version
```

## Usage
1. Run the Python script:

    ```bash
    python3 obscura.py
    ```

2. Enter the desired port number, service name, and version when prompted.

3. The script will:
   - Kill any existing process on the specified port.
   - Start the selected service on the given port.
   - Listen for incoming connections and send a corresponding fake banner.

## Example
1. Run the script:

    ```bash
    python3 obscura.py
    ```

2. Example interaction:

    ```console
    [+] ENTER PORT NUMBER: 8080
    [+] ENTER SERVICE NAME 
             [1] HTTP 
             [2] SMTP 
             [3] POP3 
             [4] SSH
    1
    [+] ENTER SERVICE VERSION: 2.4.41
    ```

    The script will start an HTTP service on port `8080`, mimicking Apache version `2.4.41`:

    ```console
    HTTP/1.1 200 OK
    Server: Apache/2.4.41 (Ubuntu)
    Date: Sat, 29 Sep 2024 12:00:00 GMT
    Content-Type: text/html; charset=UTF-8
    Content-Length: 71
    Connection: close
    
    <html><body><h1>Welcome to the Fake HTTP Server!</h1></body></html>
    ```

4. When a client connects to the service, the script will print:

    ```console
    Connection from ('127.0.0.1', 54321) established.
    ```

## Available Services
- **HTTP**: Simulates a basic HTTP web server.
- **SMTP**: Simulates an email server (e.g., Postfix).
- **POP3**: Simulates a POP3 mail retrieval service.
- **SSH**: Simulates an OpenSSH server.
- **FTP**: Simulates an FTP server.

## Customization

You can easily add more service types by editing the `start_service()` function and defining a new banner for any custom protocol you want to mimic.

