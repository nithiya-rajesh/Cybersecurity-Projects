# 🛡️ Identity Guard: Password Spray Detection Engine

<!-- Status Badges -->
![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen?style=flat-square)
![Language](https://img.shields.io/badge/Language-Python%203.x-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Category](https://img.shields.io/badge/Focus-Blue%20Team%20%2F%20Detection-red?style=flat-square)

---

## 📋 Table of Contents
- [Overview](#-overview)
- [Objectives](#-objectives)
- [Repository Structure](#-repository-structure)
- [Setup & Requirements](#-setup--requirements)
- [Key Features](#-key-features)
- [Deliverables](#-deliverables)
- [Security & Compliance](#-security--compliance)
- [Contribution Guidelines](#-contribution-guidelines)
- [License](#-license)
- [Author](#-author)

---

## 🔰 Overview

**Identity Guard** is a specialized security utility designed to **detect and alert on Password Spraying attacks** within authentication logs.

Unlike traditional brute-force attacks (which target one account with many passwords), password spraying targets many accounts with a single password to evade account lockout policies. This project demonstrates the integration of **Log Analysis Heuristics** and **Threat Intelligence APIs** to solve the critical issue of **detecting "low-and-slow" identity attacks**. It was built with efficiency in mind, utilizing O(1) lookup structures to handle log parsing at speed.

---

## 🎯 Objectives

The primary goals of this project are:

*   **Detection Engineering:** Distinguish between legitimate user error, standard brute force, and password spraying patterns using custom logic thresholds.
*   **Contextualization:** Improve alert fidelity by enriching raw IP addresses with **Geo-Location and ISP data** via API integration.
*   **Simulation:** Provide a "Red Team" generator script to create realistic, noisy datasets for validating detection logic.
*   **Automation:** Reduce manual log review time by automating the parsing of CSV/SIEM exports.

---

## 📂 Repository Structure

The codebase is organized as follows to ensure modularity and maintainability:

```text
Identity-Guard/
├── detect_spray.py       # Core Engine: Log parsing, logic detection, and API enrichment
├── generate_logs.py      # Simulation: Generates dummy logs with hidden attack patterns
├── requirements.txt      # Dependencies: Python libraries required for execution
└── README.md             # Documentation: Project overview and usage guide
```

---

## ⚙️ Setup & Requirements

### Prerequisites
Ensure the following tools and dependencies are installed before running the project:

*   **Operating System:** Linux / Windows / macOS
*   **Language:** Python 3.8+
*   **Network:** Internet access required for the Geo-IP API lookup.

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/nithiya-rajesh/Password-Spray-Detector.git
    cd Identity-Guard
    ```

2.  **Set Up Virtual Environment** (Recommended)
    ```bash
    python3 -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On Mac/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

---

## 🚀 Key Features

*   **Heuristic Threat Detection:**
    Continuously monitors authentication logs to identify anomalies using a **"Unique Target per Source"** algorithm. This specifically flags IPs that attempt to access `> X` distinct accounts within a short window.

*   **Threat Intelligence Enrichment:**
    Automatically queries the `ip-api` REST endpoint when a threat is detected. This converts a raw IP (e.g., `45.33.32.156`) into actionable intelligence (e.g., `United States - Akamai Technologies`), allowing SOC analysts to prioritize foreign threats.

*   **Attack Simulation Engine:**
    Includes a custom generator (`generate_logs.py`) utilizing the `Faker` library. This creates realistic datasets containing "Normal Traffic," "User Noise," and "Hidden Spray Attacks," allowing for robust testing without needing real sensitive logs.

*   **Scalable Data Structures:**
    Built using Python `Sets` and `DefaultDicts` to ensure duplicate username attempts are handled efficiently, preventing false positives from a single user failing to login multiple times.

---

## 📦 Deliverables

This repository includes functional scripts that output immediate console alerts.

**Sample Alert Output:**
When the tool identifies a spray pattern, it generates a high-fidelity alert in the terminal:

```text
[*] Analyzing auth_logs.csv for Password Spraying...

--- INTELLIGENCE REPORT ---
[*] Fetching Geo-Data for 192.168.1.105...

[ALERT] PASSWORD SPRAY DETECTED
   > Source IP: 192.168.1.105
   > Origin:    United States (Akamai Technologies, Inc.)
   > Targets:   10 unique accounts
   > Action:    Recommend immediate IP Block and User Password Reset.
----------------------------------------
```

## 🔐 Security & Compliance

**⚠️ Ethical Use Warning:**
This tool is intended for **educational purposes** and **defensive security engineering** only. The simulation script generates fake data.

*   **Data Privacy & Sanitization:**
    *   The `generate_logs.py` script uses the `Faker` library to create entirely fictitious PII (names, IPs). No real user data is processed or stored in this repository.
    *   If using this tool on real production logs, ensure you comply with your organization's data handling policies (GDPR/CCPA).

*   **Code Integrity:**
    *   The source code relies on standard libraries and trusted APIs.
    *   **Result:** No hardcoded credentials or API keys are required for the basic functionality.

---

## 🤝 Contribution Guidelines

Contributions are welcome to improve this project. To contribute:

1.  **Fork** the project repository.
2.  Create a new **Feature Branch** (`git checkout -b feature/NewDetectionRule`).
3.  **Commit** your changes.
4.  **Push** to the branch.
5.  Open a **Pull Request**.

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

## 👤 Author

**Nithiya Rajendran**

*   **Role:** Aspiring Security Engineer / SOC Analyst
*   **Certifications:** CCNA, Certified in Cybersecurity, CompTIA Security+
*   **LinkedIn:** https://www.linkedin.com/in/nithya-rajendran/
*   **GitHub:** https://github.com/nithiya-rajesh/Password-Spray-Detector.git

