import argparse
import csv
import json
import os
import sys
import Evtx.Evtx as evtx
import xml.etree.ElementTree as ET
from datetime import datetime

# --- Configuration ---
# If no arguments are provided, try to load from the previous step's JSON output
DEFAULT_META_FILE = 'best_log_meta.json'

# Target Event IDs
EVENT_TYPES = {
    1: "Process Creation",
    3: "Network Connection",
    11: "File Creation"
}

# --- ANSI Colors for Console Output ---
class Colors:
    RED = '\033[91m'      # Process (High Risk)
    YELLOW = '\033[93m'   # Network (Medium Risk)
    CYAN = '\033[96m'     # File (Low Risk)
    RESET = '\033[0m'
    BOLD = '\033[1m'

def get_tag_text(element, tag_name):
    """
    Robustly finds a tag's text regardless of XML namespace.
    """
    for child in element.iter():
        if child.tag.endswith(tag_name):
            return child.text
    return None

def get_data_field(event_data, field_name):
    """
    Extracts a specific named field from the <EventData> block.
    """
    for data in event_data.iter():
        if data.get('Name') == field_name:
            return data.text
    return "N/A"

def parse_record(record):
    """
    Parses a single record and returns a structured dictionary if relevant.
    """
    try:
        xml_content = record.xml()
        root = ET.fromstring(xml_content)
        
        # 1. Get Event ID
        event_id_text = get_tag_text(root, 'EventID')
        if not event_id_text: return None
        event_id = int(event_id_text)
        
        if event_id not in EVENT_TYPES:
            return None

        # 2. Get Timestamp
        time_str = get_tag_text(root, 'TimeCreated') # Attribute is usually 'SystemTime'
        # The Evtx library sometimes puts the attribute in the text or we need to find the node
        # Let's try a more direct approach for the timestamp attribute
        system_node = None
        for child in root:
            if child.tag.endswith('System'):
                system_node = child
                break
        
        timestamp = "Unknown Time"
        if system_node is not None:
            for child in system_node:
                if child.tag.endswith('TimeCreated'):
                    timestamp = child.get('SystemTime')
                    break

        # 3. Get Event Data
        event_data_node = None
        for child in root:
            if child.tag.endswith('EventData'):
                event_data_node = child
                break
        
        if event_data_node is None: return None

        # 4. Build the Event Object
        event_obj = {
            'timestamp': timestamp,
            'event_id': event_id,
            'type': EVENT_TYPES[event_id],
            'details': ""
        }

        # 5. Extract Specific Details based on ID
        if event_id == 1: # Process Create
            image = get_data_field(event_data_node, 'Image')
            cmd = get_data_field(event_data_node, 'CommandLine')
            user = get_data_field(event_data_node, 'User')
            event_obj['details'] = f"EXECUTION: {image} | CMD: {cmd} | User: {user}"
            event_obj['color'] = Colors.RED

        elif event_id == 3: # Network
            image = get_data_field(event_data_node, 'Image')
            dest_ip = get_data_field(event_data_node, 'DestinationIp')
            dest_port = get_data_field(event_data_node, 'DestinationPort')
            event_obj['details'] = f"NETWORK: {image} -> {dest_ip}:{dest_port}"
            event_obj['color'] = Colors.YELLOW

        elif event_id == 11: # File Create
            image = get_data_field(event_data_node, 'Image')
            target = get_data_field(event_data_node, 'TargetFilename')
            event_obj['details'] = f"FILE DROP: {image} created {target}"
            event_obj['color'] = Colors.CYAN

        return event_obj

    except Exception:
        return None

def main():
    parser = argparse.ArgumentParser(description="Forensic Timeline Generator")
    parser.add_argument("--log", help="Path to the EVTX file. If not provided, tries to read best_log_meta.json")
    parser.add_argument("--output", default="attack_timeline.csv", help="Output CSV filename")
    args = parser.parse_args()

    # 1. Determine Input File
    target_file = args.log
    if not target_file:
        if os.path.exists(DEFAULT_META_FILE):
            try:
                with open(DEFAULT_META_FILE, 'r') as f:
                    meta = json.load(f)
                    target_file = meta.get('best_log')
                    print(f"[*] Auto-detected best log from previous step: {target_file}")
            except Exception:
                pass
    
    if not target_file or not os.path.exists(target_file):
        print(f"{Colors.RED}[!] Error: No log file provided and {DEFAULT_META_FILE} not found.{Colors.RESET}")
        print("Usage: python timeline_generator.py --log <path_to_evtx>")
        return

    print(f"[*] Parsing {target_file} for timeline reconstruction...")
    
    timeline = []
    
    # 2. Parse File
    with evtx.Evtx(target_file) as log:
        for i, record in enumerate(log.records()):
            if i % 5000 == 0 and i > 0:
                print(f"    ...processed {i} records...")
            
            event = parse_record(record)
            if event:
                timeline.append(event)

    # 3. Sort by Timestamp
    # Timestamps are strings in ISO format, so string sorting works perfectly
    timeline.sort(key=lambda x: x['timestamp'])

    # 4. Output to Console (Colorized)
    print("\n" + "="*80)
    print(f"{'TIMESTAMP':<25} {'TYPE':<20} {'DETAILS'}")
    print("="*80)
    
    for event in timeline:
        c = event.get('color', Colors.RESET)
        print(f"{c}{event['timestamp']:<25} {event['type']:<20} {event['details']}{Colors.RESET}")