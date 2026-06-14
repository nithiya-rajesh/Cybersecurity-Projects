# 💀 Red-Connect: Python Reverse Shell & C2 Agent

<!-- Status Badges -->
![Language](https://img.shields.io/badge/Language-Python%203-blue?style=flat-square)
![Category](https://img.shields.io/badge/Category-Offensive%20Security-red?style=flat-square)
![Type](https://img.shields.io/badge/Type-Command%20%26%20Control-black?style=flat-square)

---

## 📋 Table of Contents
- [Overview](#-overview)
- [Objectives](#-objectives)
- [Repository Structure](#-repository-structure)
- [Key Features](#-key-features)
- [Usage](#-usage)
- [Disclaimer](#-disclaimer)

---

## 🔰 Overview

**Red-Connect** is a lightweight, custom-built **Reverse Shell** designed to demonstrate the mechanics of Command & Control (C2) communications.

In cybersecurity, understanding how attackers bypass firewalls is critical. Standard "Bind Shells" (where the attacker connects to the victim) are easily blocked by inbound firewall rules. **Red-Connect** utilizes a "Reverse Connection" architecture, where the victim machine initiates an outbound connection to the attacker's listener, often bypassing standard egress filters.

This project serves as a study in **Socket Programming**, **Process creation**, and **Standard I/O redirection** in Python.

---

## 🎯 Objectives

The primary goals of this project are:

*   **C2 Architecture:** Understand the difference between *Bind Shells* and *Reverse Shells* and why the latter is the standard for post-exploitation.
*   **Socket Persistence:** Implement a stable TCP connection that keeps the session alive for multiple commands, rather than closing after a single execution.
*   **Low-Level I/O:** Manually handle `stdin`, `stdout`, and `stderr` redirection using the `subprocess` library to simulate a real interactive terminal.

---

## 📂 Repository Structure

```text
Red_Connect/
├── listener.py           # The Server (Attacker): Waits for connection and sends commands
├── payload.py            # The Client (Victim): Connects back and executes commands
└── README.md             # Documentation
```
---

## 🚀 Key Features

*   **Firewall Evasion Logic:**
    Utilizes a **Reverse TCP** connection model. Since most enterprise firewalls block *inbound* traffic but allow *outbound* traffic (e.g., port 443 or 80), this tool mimics legitimate client behavior to establish a session.

*   **Remote Command Execution (RCE):**
    Leverages Python's `subprocess` module to execute system commands directly on the host OS. It captures both `stdout` (success) and `stderr` (errors) and pipes them back to the attacker in real-time.

*   **Session Persistence:**
    Unlike simple "one-shot" command execution, this tool implements a `while True` loop, maintaining the socket connection for continuous interaction until explicitly terminated.

*   **Custom Shell Navigation:**
    Includes specific logic to handle the `cd` (Change Directory) command. Since `subprocess` calls spawn new shell instances, standard `cd` commands would not persist. This tool intercepts `cd` and uses `os.chdir()` to actually change the working directory of the agent.

---

## 💻 Usage

To simulate an attack scenario, you will need two terminal windows (or two separate machines in a lab environment).

### Step 1: Start the Listener (Attacker)
On the attacking machine, start the server to wait for the incoming connection.
```bash
python listener.py
# Output: [*] Listening for incoming connections on 4444...
```
### Step 2: Execute the Payload (Target)

On the victim machine, run the client script.
```bash
python payload.py
# (No output will be shown on the victim side to maintain stealth)
```
### Step 3: Control the Session
Return to the Listener terminal. You will see a connection confirmation. You can now execute system commands.
```bash
[+] Connection established from 127.0.0.1
Shell> whoami
kali

Shell> pwd
/home/kali/Red-Connect

Shell> ls -la
total 12
drwxr-xr-x 2 kali kali 4096 Oct 27 10:00 .
drwxr-xr-x 4 kali kali 4096 Oct 27 09:55 ..
-rw-r--r-- 1 kali kali  850 Oct 27 10:00 listener.py
-rw-r--r-- 1 kali kali  620 Oct 27 10:00 payload.py
```

---

## ⚠️ Legal Disclaimer

**EDUCATIONAL USE ONLY.**
This tool is a Proof of Concept (PoC) designed to demonstrate the mechanics of TCP socket communications and Reverse Shell architecture.
*   **Authorization:** Do not run `payload.py` on any network or machine where you do not have explicit, written permission.
*   **Liability:** The author accepts no responsibility for any illegal use of this code. Accessing computers without authorization is a crime under the Computer Fraud and Abuse Act (CFAA) and similar international laws.

---

## 👤 Author

**Nithiya Rajendran**

*   **Role:** Penetration Tester / Security Researcher
*   **Certifications:** CCNA, Certified in Cybersecurity, CompTIA Security+
*   **LinkedIn:** https://www.linkedin.com/in/nithya-rajendran/
*   **GitHub:** https://github.com/nithiya-rajesh/Red-Connect

*This project is part of my offensive security portfolio, focusing on Post-Exploitation tactics and C2 development.*