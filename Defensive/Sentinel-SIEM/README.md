# 🛡️ Sentinel-SIEM: Log Analysis & Threat Intelligence Engine

<!-- Status Badges -->
![Language](https://img.shields.io/badge/Language-Python%203-blue?style=flat-square)
![Focus](https://img.shields.io/badge/Focus-Blue%20Team%20%2F%20Defense-green?style=flat-square)
![Integration](https://img.shields.io/badge/API-AbuseIPDB-orange?style=flat-square)

---

## 📋 Overview

**Sentinel-SIEM** is a lightweight Security Information and Event Management tool designed to detect brute-force attacks in real-time. 

Unlike simple grep scripts, Sentinel-SIEM implements **Logic-Based Correlation** to track repeated failures from specific IP addresses. Furthermore, it integrates with the **AbuseIPDB API** to perform automated Threat Intelligence enrichment, determining if an attacking IP has a known history of malicious behavior.

This project demonstrates the core loop of a SOC Analyst: **Detect -> Correlate -> Enrich -> Report.**

---

## 🚀 Key Features

*   **Log Parsing Engine:** 
    Extracts critical metadata (Timestamp, Attacker IP, Target Username) from unstructured Linux `auth.log` files.
    
*   **Event Correlation:** 
    Aggregates individual events to identify patterns. It flags IPs that exceed a configurable threshold of failed login attempts (Simulating a Brute Force attack).

*   **Threat Intelligence Enrichment:** 
    Automatically queries the **AbuseIPDB API** to retrieve the "Abuse Confidence Score" for high-risk IPs, providing immediate context on the attacker's reputation.

*   **Structured Reporting:** 
    Exports findings to a JSON report (`siem_report.json`) for integration with other security tools or dashboards.

---

## 📂 Repository Structure

```text
Sentinel-SIEM/
├── siem.py            # Main analysis engine
├── auth.log           # Sample log file (Sanitized)
├── requirements.txt   # Dependencies
└── README.md          # Documentation
```
## 🛠️ Setup & Usage

**Install Dependencies:**
```Bash
pip install requests
```
**Configure API Key (Optional):**
To enable Threat Intel features, get a free key from AbuseIPDB and set it in your environment:

```Bash
export ABUSEIPDB_KEY="your_api_key_here"
```
Run the SIEM:
```Bash
python siem.py auth.log --threshold 5
```
View the Report:
Check the console for real-time alerts and open siem_report.json for the summary.
---

📊 Sample Output

```Text
[*] Starting SIEM Analysis on: auth.log
[ALERT] Failed Login: root from 203.0.113.55
[ALERT] Failed Login: admin from 203.0.113.55
[ALERT] Failed Login: user from 203.0.113.55

[!!] CRITICAL ALERT: Brute Force Detected from 203.0.113.55 (3 attempts)
    -> Querying AbuseIPDB...
    -> Threat Intel: 100% Confidence of Abuse
```

## ⚠️ Disclaimer

This tool is intended for educational purposes and for analyzing logs on systems you own or manage.


## 👤 Author

Name: Nithiya Rajendran  
Role: Security Engineer / SOC Analyst  
Focus: Threat Detection, SIEM Development, and Automation