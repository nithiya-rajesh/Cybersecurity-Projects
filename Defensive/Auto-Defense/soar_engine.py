import json
import time
import logging

# Configure logging to look like a real system service
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [SOAR ENGINE] - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class MockFirewall:
    """
    Simulates a next-gen firewall API (e.g., Palo Alto, Cisco ASA).
    In a real job, this would use 'requests.post' to send API commands.
    """
    def __init__(self):
        self.blocked_ips = []
        self.database_file = "firewall_rules.db"

    def block_ip(self, ip_address, reason):
        """Adds an IP to the blocklist."""
        logging.info(f"Connecting to Firewall API...")
        time.sleep(1) # Simulate network latency
        
        if ip_address in self.blocked_ips:
            logging.warning(f"Skipping: IP {ip_address} is already blocked.")
            return False
        
        self.blocked_ips.append(ip_address)
        
        # Persist to a file (Simulating the firewall database)
        with open(self.database_file, "a") as f:
            f.write(f"{ip_address} | {reason}\n")
            
        logging.info(f"SUCCESS: IP {ip_address} has been BLOCKED. Reason: {reason}")
        return True

def analyze_threat(alert_data):
    """
    Decides if an alert is dangerous enough to block.
    Returns: Action String ('BLOCK', 'LOG', 'IGNORE')
    """
    score = alert_data.get("severity_score", 0)
    type = alert_data.get("attack_type", "Unknown")
    
    logging.info(f"Analyzing alert: {type} (Score: {score})")
    
    # DECISION LOGIC
    if score >= 80:
        return "BLOCK"
    elif score >= 50:
        return "LOG"
    else:
        return "IGNORE"

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # 1. Initialize our Mock Firewall
    fw = MockFirewall()
    
    # 2. Simulate Incoming Alerts (e.g., from a SIEM or Project 1)
    incoming_alerts = [
        {
            "source_ip": "192.168.1.105",
            "attack_type": "Password Spray",
            "severity_score": 90,  # HIGH RISK -> Should Block
            "timestamp": "2023-10-27T10:00:00Z"
        },
        {
            "source_ip": "10.0.0.55",
            "attack_type": "Failed Login",
            "severity_score": 40,  # LOW RISK -> Should Log only
            "timestamp": "2023-10-27T10:05:00Z"
        },
        {
            "source_ip": "45.33.32.156",
            "attack_type": "Ransomware Beacon",
            "severity_score": 100, # CRITICAL -> Should Block
            "timestamp": "2023-10-27T10:10:00Z"
        }
    ]
    
    print("--- STARTING AUTOMATED RESPONSE ENGINE ---\n")
    
    for alert in incoming_alerts:
        ip = alert["source_ip"]
        action = analyze_threat(alert)
        
        if action == "BLOCK":
            fw.block_ip(ip, alert["attack_type"])
        elif action == "LOG":
            logging.info(f"Low severity threat from {ip}. Logged for review.")
        else:
            logging.info(f"Ignored noise from {ip}.")
            
        print("-" * 50) # Separator