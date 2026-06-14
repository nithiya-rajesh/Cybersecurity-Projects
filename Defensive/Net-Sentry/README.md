# 🕸️ Net-Sentry: Multi-Threaded Vulnerability Scanner

<!-- Status Badges -->
![Language](https://img.shields.io/badge/Language-Python%203-blue?style=flat-square)
![Concurrency](https://img.shields.io/badge/Architecture-Multi--Threaded-orange?style=flat-square)
![Focus](https://img.shields.io/badge/Focus-Network%20Recon-red?style=flat-square)

---

## 📋 Table of Contents
- [Overview](#-overview)
- [Objectives](#-objectives)
- [Repository Structure](#-repository-structure)
- [Key Features](#-key-features)
- [Usage](#-usage)
- [Sample Output](#-sample-output)
- [Disclaimer](#-disclaimer)

---

## 🔰 Overview

**Net-Sentry** is a custom-built network reconnaissance tool designed to identify open ports and enumerate service versions on target systems.

While tools like Nmap exist, Net-Sentry was engineered to demonstrate the underlying mechanics of **TCP/IP socket connections** and **concurrent programming**. It moves beyond simple "port knocking" by establishing full TCP handshakes to retrieve service banners (Banner Grabbing), allowing security engineers to identify outdated or vulnerable software versions (e.g., old Apache or OpenSSH instances) instantly.

To ensure performance at scale, the tool utilizes a **Producer-Consumer architecture** with Python's `threading` and `queue` modules, enabling it to scan thousands of ports in seconds rather than minutes.

---

## 🎯 Objectives

The primary goals of this project are:

*   **Network Fundamentals:** Demonstrate a deep understanding of the **TCP 3-Way Handshake** by manually managing socket connections without relying on high-level abstraction libraries.
*   **Performance Engineering:** Implement **Multi-Threading** to solve the "blocking I/O" problem inherent in network scanning, drastically reducing execution time.
*   **Vulnerability Identification:** Go beyond "Open/Closed" status by implementing **Banner Grabbing**, extracting specific version strings to map against known CVEs.

---

## 📂 Repository Structure

```text
Net_Sentry/
├── scanner.py            # The main multi-threaded scanning engine
└── README.md             # Documentation

```
---

## 🚀 Key Features

*   **Concurrent Scanning Engine:**
    Utilizes a **Thread Pool** pattern (50+ worker threads) to scan ports in parallel. This reduces the scan time for 1,024 ports from ~15 minutes (synchronous) to **under 30 seconds**.

*   **Service Fingerprinting (Banner Grabbing):**
    Automatically sends protocol-specific triggers (e.g., HTTP `HEAD` requests) to elicit a response from the server, capturing the exact software version (e.g., `Apache/2.4.7`) for vulnerability analysis.

*   **Raw Socket Management:**
    Built using Python's native `socket` library. Handles connection timeouts, socket creation, and graceful teardowns manually, ensuring precise control over the TCP connection state.

*   **Fault Tolerance:**
    Implements robust error handling to manage connection refusals, timeouts, and unreachable hosts without crashing the scanner.

---

## 💻 Usage

Since this tool uses Python's standard libraries, no external installation (`pip install`) is required.

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/nithiya-rajesh/Net-Sentry.git
    cd Net-Sentry
    ```

2.  **Run the Scanner:**
    ```bash
    python scanner.py
    ```
    *(Note: You can modify the `TARGET_IP` variable inside the script to scan different authorized hosts.)*

---

## 📊 Sample Output

Below is an actual scan result against `scanme.nmap.org`. Note the execution speed and the detailed version banners.

```text
[*] Starting Multi-Threaded Scan on scanme.nmap.org
[*] Scanning ports 1-1024 with 50 threads...
--------------------------------------------------
[+] Port 22 OPEN : SSH-2.0-OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.13
[+] Port 80 OPEN : HTTP/1.1 400 Bad Request
    Server: Apache/2.4.7 (Ubuntu)
--------------------------------------------------
[*] Scan Complete in 21.57 seconds.
[*] Found 2 open ports.
```
---

## ⚠️ Legal Disclaimer

**Authorized Use Only:**
This tool is designed for **educational purposes** and for use on networks where you have explicit permission to scan.
*   The sample output demonstrates a scan against `scanme.nmap.org`, a service provided by the Nmap Project specifically for testing scanners.
*   Scanning unauthorized networks/IPs is illegal and unethical. The author accepts no responsibility for misuse of this code.

---

## 👤 Author

**Nithiya Rajendran**

*   **Role:** Security Engineer / Network Security Specialist
*   **Certifications:** CCNA, Certified in Cybersecurity, CompTIA Security+
*   **LinkedIn:** https://www.linkedin.com/in/nithya-rajendran/
*   **GitHub:** https://github.com/nithiya-rajesh/Net-Sentry
