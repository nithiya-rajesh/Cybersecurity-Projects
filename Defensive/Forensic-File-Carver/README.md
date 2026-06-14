# 🕵️‍♂️ Forensic File Carver

<!-- Status Badges -->
![Language](https://img.shields.io/badge/Language-Python%203-blue?style=flat-square)
![Focus](https://img.shields.io/badge/Focus-Digital%20Forensics-red?style=flat-square)
![Operation](https://img.shields.io/badge/Operation-Binary%20Analysis-orange?style=flat-square)

---

## 📋 Overview

**Forensic File Carver** is a low-level data recovery tool designed to extract deleted or fragmented files from raw disk images (`.dd`, `.img`). 

Unlike standard file system tools that rely on the Master File Table (MFT) or Inodes, this tool uses **File Carving** techniques. It scans the raw byte stream for specific file signatures ("Magic Bytes"), allowing it to recover data even when the file system is corrupted or the file has been "permanently" deleted.

This project demonstrates core competencies in **Digital Forensics**, **Binary Data Manipulation**, and **Evidence Integrity**.

---

## 🚀 Key Features

*   **Signature-Based Recovery:** 
    Identifies JPEG artifacts by scanning for standard headers (`\xFF\xD8\xFF\xE0`) and footers (`\xFF\xD9`).
    
*   **Automated Integrity Hashing:** 
    Calculates the **MD5 Hash** of every recovered file immediately upon extraction. This ensures cryptographic proof of integrity, a requirement for forensic evidence handling.

*   **Forensic Reporting:** 
    Generates a structured CSV report (`report.csv`) detailing:
    *   Offset Location (Start/End Bytes)
    *   File Size
    *   MD5 Hash
    *   Recovery Timestamp

*   **Test Data Generator:** 
    Includes a utility script to generate valid raw disk images with embedded artifacts for safe testing and validation.

---

## 📂 Repository Structure

```text
Forensic-File-Carver/
├── carve_jpegs.py         # Main recovery engine
├── create_test_image.py   # Utility to generate dummy .dd images
├── requirements.txt       # Dependencies
└── README.md              # Documentation
```

## 🛠️ Technical Architecture

 The tool operates on a Byte-Stream level:

 * Ingestion: Opens the target disk image in binary read mode (rb).  
 * Scanning: Iterates through the byte stream looking for the JPEG Start of Image (SOI) marker.  
 * Extraction: Upon finding a header, it captures the stream until the End of Image (EOI) marker is detected.  
 * Validation: The extracted byte block is hashed and saved to the recovered/ directory.  


## 💻 Usage Guide

1. Setup: Clone the repository and navigate to the directory:

```Bash  
git clone https://github.com/YourUsername/Forensic-File-Carver.git  
cd Forensic-File-Carver  
```
2. Generate Test Data: Create a 5MB raw disk image with hidden JPEG files:

```Bash  
python create_test_image.py  
```
Output: Creates test_disk.dd


3. Run Recovery: Execute the carving tool against the disk image:

```Bash  
python carve_jpegs.py  
```
4. View Results: Check the recovered/ directory for the images and the CSV report:

```Bash  
cat recovered/report.csv  
```

## ⚠️ Disclaimer

This tool is intended for educational purposes and authorized forensic analysis only.  
Always ensure you have permission before analyzing disk images or recovering data.  


## 👤 Author

Name: Nithiya Rajendran  
Role: Security Engineer / SOC Analyst  
Focus: DFIR, Automation, and Network Defense