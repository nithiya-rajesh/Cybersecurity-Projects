# 🐍 SQL-Viper: Automated SQL Injection Fuzzer

## Language & Category Focus
![Language: Python 3](https://img.shields.io/badge/Language-Python_3-blue)
![Category: Web Security](https://img.shields.io/badge/Category-Web_Security-red)
![Focus: SQL Injection](https://img.shields.io/badge/Focus-SQL_Injection-orange)

---

## 📋 Table of Contents
- [Overview](#-overview)
- [Objectives](#-objectives)
- [Repository Structure](#-repository-structure)
- [Key Features](#-key-features)
- [Installation & Usage](#-installation--usage)
- [How It Works](#-how-it-works)
- [Security & Compliance](#-security--compliance)
- [Contribution Guidelines](#-contribution-guidelines)
- [License](#-license)
- [Author](#-author)



---

## 🔰 Overview
**SQL-Viper** is a lightweight web security scanner designed to detect **Error-Based SQL Injection (SQLi)** vulnerabilities in web applications.

SQL Injection remains one of the most prevalent and dangerous risks in the OWASP Top 10. This tool automates the *fuzzing* phase of a penetration test by injecting standard SQL syntax breakers (like `'`) into URL parameters and analyzing HTTP responses for database error signatures.

It serves as a custom, minimal alternative to heavy tools like **SQLMap**, demonstrating the core logic behind vulnerability detection without the overhead of exploitation features.

---

## 🎯 Objectives
- **Educational Value**: Demonstrate how automated scanners parse URLs and interact with HTTP headers/bodies programmatically.  
- **Detection**: Identify potential entry points for SQL injection by triggering database syntax errors.  
- **Lightweight Automation**: Provide a fast, dependency-light CLI tool for quick reconnaissance before launching full-scale exploitation tools.  

---
```
📂 Repository Structure

SQL-Viper/
├──  injector.py      # Core logic for sending requests and parsing responses       
├── requirements.txt     # Python dependencies
└── README.md            # Documentation
```
---

## 🚀 Key Features
- **Parameter Parsing**: Automatically extracts query parameters (e.g., `id=1`, `cat=book`) from the target URL.  
- **Smart Fuzzing**: Iterates through every parameter, injecting payloads while keeping others stable.  
- **Multi-DB Support**: Specific error detection for:
  - MySQL / MariaDB  
  - PostgreSQL  
  - Microsoft SQL Server  
  - Oracle DB  
- **Request Customization**: Supports User-Agent randomization to bypass basic bot filters.  
- **Reporting**: Clear, color-coded console output indicating vulnerable parameters.  

---

## ⚡ Installation & Usage

### Prerequisites
- Python 3.x  
- `requests` library  

### Installation
```bash
git clone https://github.com/yourusername/SQL-Viper.git
cd SQL-Viper
pip install -r requirements.txt
```
---
Usage

Run the tool by providing a target URL containing parameters.

Basic Scan:
```bash
python injector.py "http://testphp.vulnweb.com/artists.php?artist=1"
```
---
Example Output:

```
[+] Parsing parameters for: http://site.com/view.php?id=10
[+] Fuzzing parameter: [id]
[!] VULNERABILITY DETECTED!
    [-] Parameter: id
    [-] Payload: '
    [-] Database: MySQL
    [-] Error: "You have an error in your SQL syntax"
```

---
## 🔒 Security & Compliance

SQL-Viper is designed with **responsible security practices** in mind. While it demonstrates how automated fuzzing can detect SQL Injection vulnerabilities, it is **not intended for malicious use**. To ensure compliance and ethical application:

- **Authorized Testing Only**  
  Use SQL-Viper exclusively on systems you own or have explicit written permission to test.

- **Legal Boundaries**  
  Running scans against third-party systems without consent may violate local, state, or federal laws. Always confirm compliance with applicable regulations before use.

- **Data Privacy**  
  SQL-Viper does not store or transmit scanned data externally. All results remain local to the user’s environment.

- **Responsible Disclosure**  
  If vulnerabilities are discovered during authorized testing, follow industry best practices for responsible disclosure to the affected party.

- **Compliance Alignment**  
  - OWASP Testing Guide principles  
  - GDPR and other data protection regulations (when handling user data during authorized tests)  
  - ISO/IEC 27001 standards for information security management  

- **No Exploitation Features**  
  SQL-Viper focuses on detection only. It does not include exploitation modules, reducing risk of accidental damage.

---

⚠️ **Reminder**: Misuse of this tool for unauthorized scanning or exploitation is strictly prohibited. The developer assumes no liability for any unlawful activity conducted with SQL-Viper.
---
## 🤝 Contribution Guidelines

Contributions are welcome! To maintain quality and consistency:

- **Fork the Repository**: Create your own branch for changes.  
- **Coding Standards**: Follow PEP8 style guidelines for Python code.  
- **Commit Messages**: Use clear, descriptive commit messages (e.g., `fix: handle PostgreSQL error parsing`).  
- **Pull Requests**: Provide detailed descriptions of changes and reference related issues if applicable.  
- **Testing**: Ensure your code runs without errors and does not break existing functionality.  
- **Respect Security Ethics**: Contributions must align with responsible disclosure and ethical hacking practices.  

---

## 📜 License

This project is licensed under the **MIT License** — you are free to use, modify, and distribute the code with proper attribution.  
See the [LICENSE](LICENSE) file for full details.

---

## 👤 Author

**Nithiya Rajendran**  
- *Role*: Aspiring Security Engineer / SOC Analyst  
- *Certifications*: CCNA, Certified in Cybersecurity, CompTIA Security+  
- *LinkedIn*: [linkedin.com/in/nithya-rajendran](https://www.linkedin.com/in/nithya-rajendran/)  
- *GitHub*: [github.com/nithiya-rajesh/Password-Spray-Detector](https://github.com/nithiya-rajesh/Sql-Viper.git)  

---

