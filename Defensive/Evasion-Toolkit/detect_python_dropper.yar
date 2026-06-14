rule Suspicious_Python_Dropper {
    meta:
        description = "Detects Python scripts acting as evasive PowerShell droppers"
        author = "Your Name"
        date = "2023-10-27"
        severity = "High"
    
    strings:
        // 1. Detects the import of critical libraries
        $import1 = "import subprocess"
        $import2 = "import base64"
        $import3 = "import requests"

        // 2. Detects the specific execution method
        // We split these because in Python lists, they are separate strings
        $exec_method = "powershell.exe" nocase
        $exec_policy = "-ExecutionPolicy" nocase
        $exec_bypass = "Bypass" nocase
        $exec_stdin = "-Command" 

        // 3. Detects Sandbox Evasion techniques
        $sandbox_check1 = "os.getenv"
        $sandbox_check2 = "USERNAME"
        $sandbox_check3 = "sandbox" nocase

    condition:
        // The file must start with typical Python shebang OR contain the imports
        (uint16(0) == 0x2123 or all of ($import*)) and
        
        // Must contain ALL the execution arguments
        all of ($exec*) and 
        
        // Must contain ANY of the sandbox checks
        any of ($sandbox*)
}