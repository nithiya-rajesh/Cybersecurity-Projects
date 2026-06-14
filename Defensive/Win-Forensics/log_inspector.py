import argparse
import os
import Evtx.Evtx as evtx
import xml.etree.ElementTree as ET
from collections import Counter
from tqdm import tqdm  # Professional progress bar

# --- KNOWLEDGE BASE ---
# A mapping of common Event IDs to human-readable descriptions.
# This adds "Context" to your tool, which is critical for SOC roles.
EVENT_DESCRIPTIONS = {
    # Sysmon
    1: "Sysmon: Process Creation",
    3: "Sysmon: Network Connection",
    11: "Sysmon: File Create",
    12: "Sysmon: Registry Event (Object Create/Delete)",
    13: "Sysmon: Registry Event (Value Set)",
    22: "Sysmon: DNS Query",
    
    # Windows Security
    4624: "Security: Successful Logon",
    4625: "Security: Failed Logon",
    4688: "Security: Process Creation",
    4720: "Security: User Account Created",
    4726: "Security: User Account Deleted",
    1102: "Security: Audit Log Cleared (Suspicious!)"
}

def get_event_id(root):
    """
    Robustly finds the EventID regardless of the XML namespace.
    """
    for neighbor in root.iter():
        if 'EventID' in neighbor.tag:
            try:
                return int(neighbor.text)
            except (ValueError, TypeError):
                return None
    return None

def analyze_log(filepath):
    """
    Parses the EVTX file and counts event IDs.
    """
    event_counts = Counter()
    total_records = 0
    
    # We use mmap=True for performance on large files
    try:
        with evtx.Evtx(filepath) as log:
            # Use tqdm for a progress bar based on the number of records
            # Note: getting len(list(log.records())) is slow, so we just iterate.
            print(f"[*] Parsing {os.path.basename(filepath)}...")
            
            for record in tqdm(log.records(), unit=" logs"):
                total_records += 1
                try:
                    xml_content = record.xml()
                    root = ET.fromstring(xml_content)
                    event_id = get_event_id(root)
                    
                    if event_id is not None:
                        event_counts[event_id] += 1
                except Exception:
                    # Skip malformed records without crashing
                    continue
                    
    except Exception as e:
        print(f"[!] Critical Error opening file: {e}")
        return None, 0

    return event_counts, total_records

def main():
    parser = argparse.ArgumentParser(description="Windows Event Log Inspector: Generates a summary of Event IDs.")
    parser.add_argument("evtx_file", help="Path to the .evtx file to analyze.")
    args = parser.parse_args()

    if not os.path.exists(args.evtx_file):
        print(f"[!] Error: File '{args.evtx_file}' not found.")
        return

    counts, total = analyze_log(args.evtx_file)

    if counts:
        print("\n" + "="*60)
        print(f"ANALYSIS REPORT: {os.path.basename(args.evtx_file)}")
        print(f"Total Records Processed: {total}")
        print("="*60)
        print(f"{'EVENT ID':<10} {'COUNT':<8} {'DESCRIPTION'}")
        print("-" * 60)
        
        # Sort by count (descending)
        for event_id, count in counts.most_common():
            # Get description or default to "Unknown"
            desc = EVENT_DESCRIPTIONS.get(event_id, "Unknown / Other")
            print(f"{event_id:<10} {count:<8} {desc}")
            
        print("="*60)
        
        # Strategic Insight for the User
        if 1102 in counts:
            print("\n[!] ALERT: Event ID 1102 found. The Audit Log was cleared. This is a high-confidence IOC.")

if __name__ == "__main__":
    main()