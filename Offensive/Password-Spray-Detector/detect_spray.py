import csv
import requests  # New library for API calls
import time
from collections import defaultdict

# CONFIGURATION
LOG_FILE = 'auth_logs.csv'
SPRAY_THRESHOLD = 5

def get_ip_location(ip_address):
    """
    Queries a free GeoIP API to get the country/ISP of an IP.
    """
    # 192.168.x.x is private, so let's simulate a public IP for the demo
    # if the IP matches our test attacker.
    query_ip = ip_address
    if ip_address == "192.168.1.105":
        query_ip = "45.33.32.156" # A random public IP for demonstration

    try:
        # We use ip-api.com (Free, no key required for low volume)
        response = requests.get(f"http://ip-api.com/json/{query_ip}")
        data = response.json()
        
        if data['status'] == 'success':
            return f"{data['country']} ({data['isp']})"
        else:
            return "Private/Reserved IP"
            
    except Exception as e:
        return "Lookup Failed"

def analyze_logs(filename):
    print(f"[*] Analyzing {filename} for Password Spraying...")
    suspicious_activity = defaultdict(set)

    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['status'] == 'Failed':
                    suspicious_activity[row['source_ip']].add(row['username'])
    except FileNotFoundError:
        print("File not found.")
        return

    print("\n--- INTELLIGENCE REPORT ---")
    found_attacker = False
    
    for ip, users_targeted in suspicious_activity.items():
        if len(users_targeted) >= SPRAY_THRESHOLD:
            found_attacker = True
            
            # ENRICHMENT STEP: Get Location
            print(f"[*] Fetching Geo-Data for {ip}...")
            location = get_ip_location(ip)
            
            print(f"\n[ALERT] PASSWORD SPRAY DETECTED")
            print(f"   > Source IP: {ip}")
            print(f"   > Origin:    {location}")  # <--- The new context
            print(f"   > Targets:   {len(users_targeted)} unique accounts")
            print("-" * 40)
            
            # Be nice to the free API
            time.sleep(1) 

    if not found_attacker:
        print("No threats detected.")

if __name__ == "__main__":
    analyze_logs(LOG_FILE)