import os
import requests
import json
import argparse
from datetime import datetime
from collections import defaultdict

# ==============================================================================
# CONFIGURATION & CONSTANTS
# ==============================================================================
ABUSEIPDB_API_URL = 'https://api.abuseipdb.com/api/v2/check'
DEFAULT_THRESHOLD = 3  # Number of failed logins to trigger a High Priority Alert

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================
def check_ip_reputation(ip_address, api_key):
    """
    Queries AbuseIPDB to check IP reputation.
    Returns: Score (0-100) or None if request fails.
    """
    if not api_key:
        return None

    headers = {
        'Accept': 'application/json',
        'Key': api_key
    }
    params = {
        'ipAddress': ip_address,
        'maxAgeInDays': 90
    }

    try:
        response = requests.get(ABUSEIPDB_API_URL, headers=headers, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data['data'].get('abuseConfidenceScore')
        elif response.status_code == 429:
            print(f"  [!] API Rate Limit Exceeded for {ip_address}")
        else:
            print(f"  [!] API Error {response.status_code} for {ip_address}")
    except Exception as e:
        print(f"  [!] Connection Error checking {ip_address}: {e}")
    
    return None

def parse_log_line(line):
    """
    Parses a single line of auth.log.
    Returns a dictionary if it's a failed login, otherwise None.
    """
    if "Failed password" not in line:
        return None

    try:
        parts = line.split()
        # Extract Timestamp (Standard Linux Log Format: Mon DD HH:MM:SS)
        timestamp = " ".join(parts[:3])
        
        # Extract IP Address (usually follows 'from')
        if "from" in parts:
            ip_index = parts.index("from") + 1
            ip_address = parts[ip_index]
        else:
            return None

        # Extract Username (usually follows 'for')
        username = "Unknown"
        if "for" in parts:
            user_index = parts.index("for") + 1
            if parts[user_index] == "invalid":
                username = parts[user_index + 2] # "invalid user [name]"
            else:
                username = parts[user_index]

        return {
            "timestamp": timestamp,
            "ip": ip_address,
            "username": username
        }
    except Exception:
        return None

# ==============================================================================
# MAIN LOGIC
# ==============================================================================
def main():
    parser = argparse.ArgumentParser(description="Custom SIEM: SSH Log Analysis & Threat Intel")
    parser.add_argument("logfile", help="Path to the auth.log file")
    parser.add_argument("--threshold", type=int, default=DEFAULT_THRESHOLD, help="Failed login count to trigger alert")
    parser.add_argument("--json", help="Output results to a JSON file", default="siem_report.json")
    args = parser.parse_args()

    if not os.path.exists(args.logfile):
        print(f"[!] Error: File '{args.logfile}' not found.")
        return

    # Get API Key from Environment Variable
    api_key = os.getenv('ABUSEIPDB_KEY')
    if not api_key:
        print("[*] Note: 'ABUSEIPDB_KEY' not found in environment. Threat Intel features disabled.")

    print(f"[*] Starting SIEM Analysis on: {args.logfile}")
    print(f"[*] Alert Threshold: {args.threshold} failed attempts")
    print("-" * 60)

    failed_logins = []
    ip_counts = defaultdict(int)

    # 1. Parse the Log
    with open(args.logfile, 'r') as f:
        for line in f:
            event = parse_log_line(line)
            if event:
                failed_logins.append(event)
                ip_counts[event['ip']] += 1
                
                # Real-time Console Alert
                print(f"[ALERT] Failed Login: {event['username']} from {event['ip']} at {event['timestamp']}")

    print("-" * 60)
    print("[*] Log Parsing Complete. Beginning Correlation & Enrichment...")
    
    # 2. Correlate and Enrich
    siem_results = []
    
    for ip, count in ip_counts.items():
        if count >= args.threshold:
            print(f"\n[!!] CRITICAL ALERT: Brute Force Detected from {ip} ({count} attempts)")
            
            # Threat Intel Check
            reputation = "Not Checked"
            if api_key:
                print(f"    -> Querying AbuseIPDB for {ip}...")
                score = check_ip_reputation(ip, api_key)
                if score is not None:
                    reputation = f"{score}% Confidence of Abuse"
                    print(f"    -> Threat Intel: {reputation}")
            
            siem_results.append({
                "ip": ip,
                "attempts": count,
                "reputation": reputation,
                "status": "High Priority"
            })

    # 3. Generate Report
    if args.json:
        with open(args.json, 'w') as jf:
            json.dump(siem_results, jf, indent=4)
        print(f"\n[+] SIEM Report saved to: {args.json}")

if __name__ == "__main__":
    main()