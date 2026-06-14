import os
import argparse
import json
import Evtx.Evtx as evtx
import xml.etree.ElementTree as ET
from collections import Counter
from tqdm import tqdm  # Professional progress bar

# --- Configuration ---
# We look for these specific Sysmon Event IDs
INTERESTING_EVENT_IDS = {
    1: "Process Creation",
    3: "Network Connection", 
    11: "File Creation"
}

def strip_namespace(xml_content):
    """
    Removes the annoying XML namespaces (xmlns=...) so we can parse 
    tags easily without worrying about the specific schema version.
    """
    # A simple, robust way to ignore namespaces is to just parse and ignore them in logic,
    # but stripping is cleaner for ElementTree in this specific use case.
    # However, to keep it fast, we will just handle the namespace in the lookup logic below.
    return xml_content

def get_event_id(root):
    """
    Robustly finds the EventID regardless of the XML namespace.
    """
    # Iterate over all elements to find the EventID tag, ignoring the namespace prefix
    for neighbor in root.iter():
        if 'EventID' in neighbor.tag:
            return int(neighbor.text)
    return None

def analyze_evtx_file(filepath):
    """
    Analyzes a single EVTX file.
    Returns: A dictionary with counts and a 'score'.
    """
    event_counts = Counter()
    
    try:
        with evtx.Evtx(filepath) as log:
            for record in log.records():
                try:
                    xml_content = record.xml()
                    # Parse XML
                    root = ET.fromstring(xml_content)
                    
                    # Robustly get Event ID
                    event_id = get_event_id(root)
                    
                    if event_id in INTERESTING_EVENT_IDS:
                        event_counts[event_id] += 1
                        
                except Exception:
                    continue # Skip malformed records
                    
    except Exception as e:
        # If the file is locked or corrupt, return None
        return None

    return event_counts

def calculate_score(counts):
    """
    Calculates a 'Forensic Value Score'.
    A log with a MIX of events is worth more than a log with just one type.
    """
    total_events = sum(counts.values())
    if total_events == 0:
        return 0
    
    # Diversity Bonus: How many unique types of interesting events did we find?
    unique_types = len(counts.keys())
    
    # Formula: Total Events + (Unique Types * 100)
    # This ensures a log with ID 1, 3, and 11 ranks higher than a log with just ID 1.
    score = total_events + (unique_types * 100)
    return score

def main():
    parser = argparse.ArgumentParser(description="Forensic Log Hunter: Ranks EVTX files by attack chain relevance.")
    parser.add_argument("search_directory", help="Path to the directory containing EVTX files.")
    parser.add_argument("--output", help="Save the best file path to a JSON file for the next script.", default="best_log_meta.json")
    args = parser.parse_args()

    search_path = args.search_directory
    if not os.path.isdir(search_path):
        print(f"[!] ERROR: Directory '{search_path}' not found.")
        return

    # 1. Gather all .evtx files first
    evtx_files = []
    for root, dirs, files in os.walk(search_path):
        for filename in files:
            if filename.endswith(".evtx"):
                evtx_files.append(os.path.join(root, filename))

    if not evtx_files:
        print("[!] No .evtx files found in the target directory.")
        return

    print(f"[*] Found {len(evtx_files)} EVTX files. Beginning analysis...")
    
    results = []

    # 2. Analyze with Progress Bar (tqdm)
    for filepath in tqdm(evtx_files, unit="file"):
        counts = analyze_evtx_file(filepath)
        
        if counts and sum(counts.values()) > 0:
            score = calculate_score(counts)
            results.append({
                "path": filepath,
                "score": score,
                "counts": dict(counts)
            })

    # 3. Sort and Display
    if not results:
        print("\n[-] No interesting Sysmon events found in any files.")
        return

    # Sort by Score (Descending)
    results.sort(key=lambda x: x['score'], reverse=True)

    print("\n" + "="*60)
    print(f"{'RANK':<5} {'SCORE':<8} {'FILENAME'}")
    print("="*60)
    
    for i, res in enumerate(results[:5]):
        filename = os.path.basename(res['path'])
        print(f"{i+1:<5} {res['score']:<8} {filename}")
        # Print a mini-summary of what was found
        details = [f"{INTERESTING_EVENT_IDS[k]}: {v}" for k, v in res['counts'].items()]
        print(f"      Found: {', '.join(details)}")
        print("-" * 60)

    best_file = results[0]['path']
    print(f"\n[+] RECOMMENDATION: Use this file for your timeline:")
    print(f"    {best_file}")

    # 4. Save Metadata (Pipeline Feature)
    # This allows your next script (timeline_generator.py) to automatically know which file to use.
    with open(args.output, 'w') as f:
        json.dump({"best_log": best_file, "score": results[0]['score']}, f)
    print(f"[+] Saved recommendation to '{args.output}'")

if __name__ == "__main__":
    main()