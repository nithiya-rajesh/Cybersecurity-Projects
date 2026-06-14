# Ghost-Scanner: Enterprise Network Reconnaissance Tool

![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-blue)
![License](https://img.shields.io/badge/License-MIT-orange)
![Category](https://img.shields.io/badge/Category-Network%20Security-red)

## 📋 Table of Contents
- [🔰 Overview](#-overview)
- [🎯 Objectives](#-objectives)
- [📂 Repository Structure](#-repository-structure)
- [⚙️ Setup & Requirements](#-setup--requirements)
- [🚀 Key Features](#-key-features)
- [📦 Deliverables](#-deliverables)
- [🔒 Security & Compliance](#-security--compliance)
- [🤝 Contribution Guidelines](#-contribution-guidelines)
- [⚖️ License](#-license)
- [👤 Author](#-author)

## 🔰 Overview
**Ghost-Scanner** is an enterprise-grade network reconnaissance utility designed to accelerate the identification of attack surfaces through high-concurrency port scanning and intelligent service enumeration.

This project demonstrates the integration of low-level **Socket programming** and **asynchronous concurrency (ThreadPoolExecutor)** to solve the critical issue of slow and inaccurate network inventory during time-sensitive security engagements. It was built with modularity and interoperability in mind, featuring JSON data exports suitable for ingestion into SIEMs or downstream automation pipelines.

## 🎯 Objectives
The primary goals of this project are:
*   **Performance:** Reduce scan times by over 90% compared to sequential scripts by implementing a multi-threaded architecture capable of handling 100+ concurrent connections.
*   **Visibility:** Improve the fidelity of asset inventory by distinguishing between simple open ports and specific running service versions (Banner Grabbing).
*   **Interoperability:** Provide structured data output (JSON) to enable seamless integration with other security tools and dashboards.
*   **Vulnerability Detection:** Automate the detection of low-hanging fruit, specifically targeting misconfigured Anonymous FTP access.

## 📂 Repository Structure
The codebase is organized to ensure clarity and maintainability:

```text
Ghost-Scanner/
├── ghost_scanner.py         # Core application logic (Scanner Class & Threading)
├── requirements.txt         # Development dependencies (Linters, Formatters)
├── .gitignore               # Git exclusion rules (prevents sensitive log uploads)
├── README.md                # Project documentation
```

## ⚙️ Setup & Requirements

### Prerequisites
*   **Python 3.9+**: Ensure Python is installed and added to your system PATH.
*   **Network Access**: The host machine requires network visibility to the target IP range.

### Installation Steps

**1. Clone the Repository**
```bash
git clone https://github.com/nithiya-rajesh/Ghost-Scanner.git
cd Ghost-Scanner
```
**2. Create a Virtual Environment (Recommended)**
It is best practice to run security tools in an isolated environment.
```
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```
**3. Install Dependencies**
```
pip install -r requirements.txt
```
---
Usage
To start the scanner, run the script from your terminal:
```
python ghost_scanner.py -t 192.168.1.1 -p 1-1024
```
---

## 🚀 Key Features
*   **Multi-threaded Scanning:** Utilizes Python's `threading` module to scan hundreds of ports simultaneously, significantly reducing scan time.
*   **Banner Grabbing:** Captures service banners to identify running applications and versions.
*   **User-Friendly CLI:** Clean command-line interface with argument parsing for IP ranges and port selection.
*   **Error Handling:** Robust exception handling for timeouts and unreachable hosts.

Deliverables
------------
- Fully functional Python source code.
- JSON-formatted scan reports.
- Technical documentation and usage guide.

Security & Compliance
---------------------
Ethical Disclaimer: This tool is intended for authorized security testing only.
The author is not responsible for unauthorized use.
Ensure you have explicit permission from the network owner before scanning.

Contribution Guidelines
-----------------------
Contributions are welcome! Please fork the repository and submit a Pull Request.

License
-------
This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Nithiya Rajendran**

*   **Role:** Cybersecurity Analyst / Penetration Tester / Security Engineer
*   **Portfolio:** https://github.com/nithiya-rajesh/Ghost-Scanner.git
*   **LinkedIn:** https://www.linkedin.com/in/nithya-rajendran/
*   **GitHub:** https://github.com/nithiya-rajesh/
