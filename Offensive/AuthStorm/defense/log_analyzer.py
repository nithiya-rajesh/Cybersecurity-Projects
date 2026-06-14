import json
import time
import os
from collections import defaultdict
from colorama import Fore, init

init(autoreset=True)

# --- DOCKER-READY CONFIGURATION ---
DEFAULT_LOG = "../target/access.log"
LOG_FILE = os.getenv("LOG_PATH", DEFAULT_LOG)

THRESHOLD = 5
TIME_WINDOW = 10

def monitor_logs():
    # --- NEW: WAIT LOOP ---
    print(f"{Fore.BLUE}[*] SIEM Initializing...")
    while not os.path.exists(LOG_FILE):
        print(f"{Fore.YELLOW}[*] Waiting for log file at {LOG_FILE}...")
        time.sleep(2)
    
    print(f"{Fore.GREEN}[*] Log file found! Monitoring started.")
    
    # Track failed logins
    failed_logins = defaultdict(list)

    try:
        with open(LOG_FILE, "r") as f:
            # Move to end of file
            f.seek(0, 2)
            
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.1)
                    continue
                
                try:
                    log = json.loads(line)
                    if log["status_code"] == 401:
                        ip = log["src_ip"]
                        now = time.time()
                        failed_logins[ip].append(now)
                        failed_logins[ip] = [t for t in failed_logins[ip] if now - t < TIME_WINDOW]
                        
                        count = len(failed_logins[ip])
                        print(f"{Fore.YELLOW}[-] Failed Login: {ip} (Count: {count})")

                        if count >= THRESHOLD:
                            print(f"\n{Fore.RED}!!! CRITICAL ALERT !!!")
                            print(f"{Fore.RED}[!] BRUTE FORCE DETECTED: {ip}")
                            failed_logins[ip] = [] # Reset

                except json.JSONDecodeError:
                    pass
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}")

if __name__ == "__main__":
    monitor_logs()