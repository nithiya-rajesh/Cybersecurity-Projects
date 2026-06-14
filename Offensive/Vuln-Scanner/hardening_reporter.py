import json
import argparse
import os

# ==============================================================================
# REMEDIATION DATABASE
# ==============================================================================
REMEDIATION_DB = {
    "Apache": "Update Apache HTTP Server to the latest stable version. Disable directory listing.",
    "OpenSSH": "Update OpenSSH. Disable root login in sshd_config. Use Key-based authentication.",
    "vsftpd": "Consider switching to SFTP (SSH File Transfer Protocol). If FTP is required, enforce TLS.",
    "Nginx": "Update Nginx. Hide version tokens in config (server_tokens off).",
    "Unknown": "Service unrecognized. Investigate manually and ensure least-privilege access."
}

def generate_report(json_file):
    if not os.path.exists(json_file):
        print(f"[!] Error: File {json_file} not found. Run scanner_v2.py first.")
        return

    with open(json_file, 'r') as f:
        findings = json.load(f)

    print("="*60)
    print("===         AUTOMATED HARDENING REPORT         ===")
    print("="*60)

    if not findings:
        print("[*] No open ports or vulnerabilities found in the scan data.")
        return

    for item in findings:
        port = item['port']
        banner = item['service']
        vuln = item['vulnerability']
        
        print(f"\n[+] Service Detected on Port {port}")
        print(f"    Banner: {banner[:60]}...")
        
        if vuln:
            print(f"    \033[91m[!] VULNERABILITY: {vuln}\033[0m")
        
        # Dynamic Recommendation based on Service Name
        rec = "General hardening required."
        for key, advice in REMEDIATION_DB.items():
            if key in banner:
                rec = advice
                break
        
        print(f"    \033[93m[->] RECOMMENDATION: {rec}\033[0m")
        print("-" * 40)

def main():
    parser = argparse.ArgumentParser(description="Generate Hardening Report from Scan")
    parser.add_argument("--input", help="Input JSON file from scanner", default="scan_results.json")
    args = parser.parse_args()
    
    generate_report(args.input)

if __name__ == "__main__":
    main()