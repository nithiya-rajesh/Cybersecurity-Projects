import sys
import socket
import argparse
import json
import time

# ==============================================================================
# CONFIGURATION & VULNERABILITY DATABASE
# ==============================================================================
VULNERABILITY_DB = {
    "Apache/2.4.7": "CRITICAL: Remote Code Execution (CVE-2021-42013).",
    "OpenSSH_7.4": "HIGH: User enumeration vulnerability (CVE-2018-15473).",
    "OpenSSH_6.6.1p1": "MEDIUM: Old SSH version. Recommend upgrade.",
    "vsftpd 2.3.4": "CRITICAL: Backdoor Command Execution (CVE-2011-2523).",
    "vsftpd 3.0.2": "HIGH: Denial of Service vulnerability."
}

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================
def grab_banner(ip, port):
    """
    Connects to a port and grabs the banner.
    Handles HTTP specifically by sending a HEAD request.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((ip, port))
        
        # If HTTP/HTTPS port, send a request
        if port in [80, 8080, 443]:
            sock.send(b'HEAD / HTTP/1.1\r\nHost: ' + ip.encode() + b'\r\n\r\n')
        
        banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
        sock.close()
        return banner if banner else "OPEN (No Data)"
    except Exception:
        return None

def check_vuln(banner):
    """Checks banner against local DB."""
    for signature, description in VULNERABILITY_DB.items():
        if signature in banner:
            return description
    return None

# ==============================================================================
# MAIN LOGIC
# ==============================================================================
def main():
    parser = argparse.ArgumentParser(description="Simple Vulnerability Scanner")
    parser.add_argument("target", help="Target IP or Hostname")
    parser.add_argument("--ports", help="Comma-separated ports (e.g. 21,22,80)", default="21,22,80,443,8080")
    parser.add_argument("--output", help="Save results to JSON file", default="scan_results.json")
    args = parser.parse_args()

    target_ip = socket.gethostbyname(args.target)
    ports = [int(p) for p in args.ports.split(',')]
    
    print(f"[*] Starting Vulnerability Scan on {args.target} ({target_ip})")
    print("-" * 60)

    results = []

    for port in ports:
        print(f"Scanning Port {port}...", end='\r')
        banner = grab_banner(target_ip, port)
        
        if banner:
            print(f"[+] Port {port:<5} [OPEN] : {banner[:50]}...") # Truncate long banners
            
            vuln = check_vuln(banner)
            finding = {
                "port": port,
                "service": banner,
                "vulnerability": vuln
            }
            
            if vuln:
                print(f"    \033[91m[!] VULN DETECTED: {vuln}\033[0m")
            
            results.append(finding)
        else:
            # Optional: Print closed ports or just ignore
            pass

    print("-" * 60)
    
    # Save to JSON for the Reporter Script
    with open(args.output, 'w') as f:
        json.dump(results, f, indent=4)
    print(f"[*] Scan complete. Results saved to {args.output}")

if __name__ == "__main__":
    main()