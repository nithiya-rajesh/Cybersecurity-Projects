# 🛡️ Vuln-Scanner: Automated Vulnerability Assessment Tool

<!-- Status Badges -->
![Language](https://img.shields.io/badge/Language-Python%203-blue?style=flat-square)
![Focus](https://img.shields.io/badge/Focus-Vulnerability%20Management-red?style=flat-square)
![Operation](https://img.shields.io/badge/Operation-Recon%20%26%20Audit-orange?style=flat-square)

---

## 📋 Overview

**Vuln-Scanner** is a lightweight vulnerability assessment toolkit designed to identify outdated services and suggest hardening measures.

It operates in two stages:
1.  **The Scanner:** Performs active reconnaissance (Banner Grabbing) to identify service versions running on open ports. It compares these versions against a local database of known CVEs (Common Vulnerabilities and Exposures).
2.  **The Reporter:** Consumes the scan data to generate an actionable "Hardening Report," providing specific remediation steps for system administrators.

This project demonstrates the **"Identify -> Assess -> Remediate"** lifecycle central to Vulnerability Management.

---

## 🚀 Key Features

*   **Service Fingerprinting:** 
    Uses socket programming to grab banners from services (SSH, FTP, HTTP). Includes specific logic to handle HTTP HEAD requests for web servers.
    
*   **CVE Mapping:** 
    Automatically checks grabbed banners against a database of known vulnerable versions (e.g., `vsftpd 2.3.4`, `Apache 2.4.7`).

*   **Automated Reporting:** 
    Decouples the scanning logic from the reporting logic. The scanner outputs raw JSON data, which the reporter converts into a human-readable remediation plan.

*   **Customizable Scope:** 
    Supports CLI arguments to define target IPs and specific port ranges.

---

## 📂 Repository Structure

```text
Vuln-Scanner/
├── scanner_v2.py          # Active Scanner (Generates JSON)
├── hardening_reporter.py  # Report Generator (Reads JSON)
├── scan_results.json      # Output file (Auto-generated)
└── README.md              # Documentation
```
## 🛠️ Usage Guide

**Run the Scanner:**

Scan a target to identify services and vulnerabilities.

```Bash
python scanner_v2.py scanme.nmap.org --ports 21,22,80,443
```
Output:
Displays open ports and saves details to scan_results.json.


**Generate the Report:**

Run the reporter to get remediation advice.

```Bash
python hardening_reporter.py
```
Output:
Prints a structured hardening plan with specific advice 
(e.g., "Update OpenSSH", "Disable FTP").

---

## ⚠️ Disclaimer
This tool is intended for educational purposes and for use on systems you own 
or have explicit permission to scan. Unauthorized scanning is illegal.

---

## 👤 Author

Name: Nithiya Rajendran  
Role: Security Engineer / Vulnerability Analyst  
Focus: Automation, Python, and System Hardening