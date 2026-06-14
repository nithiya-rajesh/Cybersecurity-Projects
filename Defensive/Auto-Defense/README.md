# 🤖 Auto-Defense: Automated Incident Response (SOAR)

<!-- Status Badges -->
![Language](https://img.shields.io/badge/Language-Python%203-blue?style=flat-square)
![Type](https://img.shields.io/badge/Type-Automation%20%2F%20SOAR-purple?style=flat-square)
![Status](https://img.shields.io/badge/Status-Prototype-success?style=flat-square)

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

**Auto-Defense** is a lightweight **Security Orchestration, Automation, and Response (SOAR)** engine designed to bridge the gap between detection and remediation.

In a modern SOC, speed is critical. Manually reviewing every alert creates "Alert Fatigue" and slows down response times. This project simulates an automated defense system that ingests threat alerts (JSON), evaluates their severity using a logic engine, and automatically executes firewall blocks for high-risk threats without human intervention.

It demonstrates the use of **Object-Oriented Programming (OOP)** to mock enterprise firewall APIs and **Structured Logging** for auditability.

---

## 🎯 Objectives

The primary goals of this project are:

*   **Automated Remediation:** Demonstrate how to reduce Mean Time to Respond (MTTR) by programmatically blocking threats based on severity thresholds.
*   **Decision Logic:** Implement a risk-scoring engine that distinguishes between "Critical Threats" (requiring immediate blocks) and "Low-Fidelity Noise" (requiring logging only).
*   **Software Engineering:** Utilize **Object-Oriented Programming (OOP)** principles (Classes, Methods) to create modular, maintainable code that simulates interaction with external APIs (Mock Firewall).

---

## 📂 Repository Structure

```text
Auto_Defense/
├── soar_engine.py        # Main automation logic and Mock Firewall class
├── firewall_rules.db     # Generated artifact (Log of blocked IPs)
└── README.md             # Documentation
```

---

## 🚀 Key Features

*   **Risk-Based Decision Engine:**
    Ingests JSON-formatted alerts and applies conditional logic to determine the response action.
    *   `Severity >= 80`: **BLOCK** (Immediate Firewall Update)
    *   `Severity < 80`: **LOG** (Flag for Analyst Review)

*   **Mock API Integration:**
    Features a `MockFirewall` class that simulates the behavior of a Next-Generation Firewall (NGFW) API. This abstraction layer demonstrates how to structure code for interacting with third-party vendors (e.g., Palo Alto, Cisco) via Python.

*   **Persistent Audit Trail:**
    Automatically maintains a `firewall_rules.db` flat-file database, recording every blocked IP and the reason for the block. This ensures accountability and allows for easy rollback of automated actions.

*   **Enterprise Logging:**
    Replaces standard `print` statements with Python's `logging` module to generate timestamped, standardized logs suitable for ingestion into a SIEM.

---

## 💻 Usage

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/nithiya-rajesh/Auto-Defense.git
    cd Auto-Defense
    ```

2.  **Run the Engine:**
    ```bash
    python soar_engine.py
    ```

3.  **Verify the Blocklist:**
    Check the newly created database file to see the persistent rules.
    ```bash
    cat firewall_rules.db  # On Linux/Mac
    # OR open firewall_rules.db in Notepad on Windows
    ```

---

## 📊 Sample Output

**1. Console Execution Logs:**
The system processes three simulated alerts with different severity scores.

```text
--- STARTING AUTOMATED RESPONSE ENGINE ---

2023-10-27 10:00:01 - [SOAR ENGINE] - INFO - Analyzing alert: Password Spray (Score: 90)
2023-10-27 10:00:01 - [SOAR ENGINE] - INFO - Connecting to Firewall API...
2023-10-27 10:00:02 - [SOAR ENGINE] - INFO - SUCCESS: IP 192.168.1.105 has been BLOCKED. Reason: Password Spray
--------------------------------------------------
2023-10-27 10:00:02 - [SOAR ENGINE] - INFO - Analyzing alert: Failed Login (Score: 40)
2023-10-27 10:00:02 - [SOAR ENGINE] - INFO - Low severity threat from 10.0.0.55. Logged for review.
--------------------------------------------------
2023-10-27 10:00:02 - [SOAR ENGINE] - INFO - Analyzing alert: Ransomware Beacon (Score: 100)
2023-10-27 10:00:02 - [SOAR ENGINE] - INFO - Connecting to Firewall API...
2023-10-27 10:00:03 - [SOAR ENGINE] - INFO - SUCCESS: IP 45.33.32.156 has been BLOCKED. Reason: Ransomware Beacon
--------------------------------------------------
```

---

## ⚠️ Disclaimer

**Simulation Only:**
This tool contains a `MockFirewall` class intended for demonstration purposes. It **does not** interact with your actual operating system's firewall (iptables/Windows Firewall) or network hardware.
*   The `firewall_rules.db` file is a local text artifact created to simulate a database entry.
*   No actual network traffic is blocked on the host machine running this script.

---

## 👤 Author

**Nithiya Rajendran**

*   **Role:** Security Engineer / Automation Specialist
*   **Certifications:** CCNA, Certified in Cybersecurity, CompTIA Security+
*   **LinkedIn:** https://www.linkedin.com/in/nithya-rajendran/
*   **GitHub:** https://github.com/nithiya-rajesh/Auto-Defense

