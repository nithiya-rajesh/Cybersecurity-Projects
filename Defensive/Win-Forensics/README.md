# 🕵️‍♂️ Win-Forensics: Automated Attack Timeline Generator

<!-- Status Badges -->
![Language](https://img.shields.io/badge/Language-Python%203-blue?style=flat-square)
![Focus](https://img.shields.io/badge/Focus-Digital%20Forensics-red?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Windows%20%2F%20Sysmon-blueviolet?style=flat-square)

---

## 📋 Overview

**Win-Forensics** is a modular Python pipeline designed to automate the initial triage phase of an Incident Response (IR) investigation. 

In a real-world breach, analysts are often overwhelmed with gigabytes of EVTX (Windows Event Log) files. Manually finding the "needle in the haystack" is inefficient. This toolkit solves that problem by:
1.  **Hunting:** Automatically scanning directories to identify the most suspicious log file based on a weighted scoring algorithm.
2.  **Triaging:** Summarizing event types to understand the log's context.
3.  **Reconstructing:** Generating a color-coded, chronological timeline of the attack chain (Process Execution -> Network Connection -> File Drop).

---

## 🚀 Key Features

*   **Heuristic Log Ranking:**
    Instead of just counting events, the "Hunter" script calculates a **Forensic Score** for each file. Logs containing a full "Kill Chain" (e.g., Process Creation + Network Connections) are ranked higher than logs with only one event type.
    
*   **Automated Pipeline:**
    The tools are integrated. The "Hunter" saves metadata (`best_log_meta.json`) which is automatically consumed by the "Timeline Generator," eliminating manual file selection.

*   **Visual & Structured Reporting:**
    *   **Console:** ANSI color-coded output for immediate visual identification of high-risk events (Red for Execution, Yellow for Network).
    *   **CSV:** Automatically generates `attack_timeline.csv` for professional reporting and further analysis in Excel/SIEM.

*   **Robust Parsing:**
    Built on `python-evtx`, the tool handles XML namespace variations and messy real-world data without crashing.

---

## 📂 Project Structure

```text
Win-Forensics-Timeline/
├── find_best_log.py       # [The Hunter] Scans directories & ranks logs by forensic value
├── log_inspector.py       # [The Triage] Summarizes Event IDs (Knowledge Base included)
├── timeline_generator.py  # [The Analyst] Builds the attack timeline (CSV + Console)
├── requirements.txt       # Dependencies
└── README.md              # Documentation
```
---
## 🛠️ Setup & Installation

Clone the Repository:
```Bash
git clone https://github.com/YourUsername/Win-Forensics-Timeline.git
cd Win-Forensics-Timeline
```
Install Dependencies:
```Bash
pip install -r requirements.txt
```
---

💻 Usage Guide

Phase 1: The Hunt
Scan a directory of unzipped EVTX files to find the one containing the attack.

```Bash
python find_best_log.py /path/to/logs/

Output:
Identifies the best file and saves the path to best_log_meta.json.
```
Phase 2: The Timeline
Generate the forensic timeline. The script automatically loads the file identified in Phase 1.

```Bash
python timeline_generator.py

Output:
Displays a color-coded timeline in the terminal and saves attack_timeline.csv.
```

---

## 📊 Sample Output

Console View (Timeline):
```Text
TIMESTAMP                 TYPE                 DETAILS
--------------------------------------------------------------------------------
2023-05-15 14:30:01       Process Creation     EXECUTION: cmd.exe | CMD: powershell -enc ...
2023-05-15 14:30:05       Network Connection   NETWORK: powershell.exe -> 192.168.1.50:4444
2023-05-15 14:30:10       File Creation        FILE DROP: powershell.exe created payload.exe
```
CSV Report:
The tool generates attack_timeline.csv containing structured data suitable for evidence submission.
---

## ⚠️ Disclaimer
This tool is intended for educational purposes and authorized forensic analysis only. 
It is designed to help security professionals understand and defend against cyber attacks.


## 👤 Author

Name: Nithiya Rajendran  
Role: Security Engineer / SOC Analyst  
Focus: Automation, Forensics, and Network Defense  
LinkedIn: https://www.linkedin.com/in/nithya-rajendran/  
GitHub: https://github.com/nithiya-rajesh


