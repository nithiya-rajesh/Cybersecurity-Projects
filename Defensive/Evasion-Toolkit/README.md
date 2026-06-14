# Evasive Malware Simulation & Detection Lab

## 🛡️ Project Overview
This project demonstrates a **Purple Team** approach to cybersecurity. I developed a custom Python-based simulation of a modern malware dropper to understand evasion techniques, and then engineered **YARA rules** to detect these specific behaviors.

The goal was to move beyond signature-based detection (hashes) and focus on **behavioral detection** (TTPs - Tactics, Techniques, and Procedures).

## 🎯 Key Concepts Demonstrated
### 🔴 Red Team (Attack Simulation)
  The `dropper_final.py` script simulates an Advanced Persistent Threat (APT) loader with three key capabilities:
1.  **Fileless Execution:** Uses `subprocess` pipes to inject Base64-encoded commands directly into PowerShell memory, bypassing disk-based AV scanning.
2.  **Obfuscation:** Payload is retrieved from a C2 (Gist) as a Base64 string to evade network string matching.
3.  **Sandbox Evasion:** Checks environment variables (e.g., `USERNAME`) against a blacklist to detect analysis environments and terminate execution if monitored.

### 🔵 Blue Team (Detection Engineering)
  The `detect_python_dropper.yar` file is a custom YARA rule designed to catch this specific tradecraft.
*   **Logic:** It does not look for the payload itself (which changes). Instead, it looks for the *mechanism* of delivery.
*   **Signatures:** Detects the combination of `subprocess` imports, `powershell -ExecutionPolicy Bypass` arguments, and environment keying checks.

## 📂 Repository Structure
```text
.
├── dropper.py              # V1: Basic file-based dropper (Writes to disk)
├── dropper_evasive.py      # V2: Fileless execution (In-memory only)
├── dropper_final.py        # V3: Adds Sandbox Evasion (The final test subject)
├── detect_python_dropper.yar # The YARA detection rule
└── README.md               # Documentation
```

## 🚀 Usage & Testing

### Prerequisites
- Python 3.x  
- YARA (install via `sudo apt install yara` or Homebrew)

The repository contains three versions of the dropper, showing a progression of techniques:
1. `dropper.py`: A simple dropper that writes the payload to disk.  
2. `dropper_evasive.py`: An improved version that uses Base64 and fileless execution.  
3. `dropper_final.py`: The final version, which adds a sandbox check.  

## ⚠️ **Important:** Update the `C2_URL` variable in the script with your own Gist URL before running.

### Setup and Installation

**Run this exclusively in an isolated Windows Virtual Machine.**

1. **Clone the repository:**
   ```bash
   git clone <YOUR_GITHUB_REPO_URL>
   cd evasion-toolkit
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
2. **Create and activate virtual environment:**
    ```
    python -m venv venv
    .\venv\Scripts\Activate.ps1
   ```

   **Run the Simulation (Optional)**

   **Note:** This will execute a harmless calc.exe or Write-Host payload on Windows

    ```
    python dropper_final.py
    ```

3. **Run the Detection (Core Task)**
    ```
    yara detect_python_dropper.yar dropper_final.py
    ```
4. **Expected Output:**
    ```
    Suspicious_Python_Dropper dropper_final.py
    ```
5. **Install dependencies**
    ```
    pip install -r requirements.txt
    ```



## ⚠️ Disclaimer
This repository is for educational and defensive research purposes only.
The scripts provided are designed to simulate attack behaviors to improve detection engineering skills.
They should never be used on systems without explicit permission.

## 👤 Author
Nithiya Rajendran
- Role: Cybersecurity Analyst / Security Engineer / Technical Writer
- Portfolio: https://github.com/nithiya-rajesh/fraud_detector.py
- LinkedIn: https://linkedin.com/in/nithiya-rajendran
- GitHub: https://github.com/nithiya-rajesh
