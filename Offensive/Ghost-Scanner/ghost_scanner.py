import socket
import argparse
import sys
import threading
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime


class GhostScanner:
    def __init__(self, target_ip, port_range, threads, output_file=None):
        self.target_ip = target_ip
        self.start_port, self.end_port = self.parse_ports(port_range)
        self.threads = threads
        self.output_file = output_file
        self.results = []  # Storage for JSON export
        self.lock = threading.Lock()  # Prevents race conditions when writing to results

    def parse_ports(self, port_str):
        try:
            start, end = map(int, port_str.split("-"))
            return start, end
        except ValueError:
            print("[-] Invalid port range. Use start-end (e.g., 1-100).")
            sys.exit(1)

    def grab_banner(self, s):
        try:
            s.send(b"HEAD / HTTP/1.0\r\n\r\n")
            banner = s.recv(1024).decode().strip()
            return banner.replace("\n", " ").replace("\r", " ")
        except:
            return ""

    def check_anon_ftp(self):
        """
        Specific check for Anonymous FTP login on Port 21.
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2.0)
            s.connect((self.target_ip, 21))
            banner = s.recv(1024).decode()

            # Send User
            s.send(b"USER anonymous\r\n")
            user_response = s.recv(1024).decode()

            # Send Pass
            s.send(b"PASS anonymous@example.com\r\n")
            pass_response = s.recv(1024).decode()

            s.close()

            # 230 is the FTP code for "User logged in, proceed"
            if "230" in pass_response:
                return True
            return False
        except:
            return False

    def scan_port(self, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.0)
            result = s.connect_ex((self.target_ip, port))

            if result == 0:
                # 1. Grab Banner
                banner = self.grab_banner(s)

                # 2. Service Identification
                service_id = "Unknown"
                if banner:
                    service_id = banner
                else:
                    try:
                        service_id = socket.getservbyport(port, "tcp").upper()
                    except:
                        pass

                # 3. Special Vulnerability Check: Anonymous FTP
                vuln_info = ""
                if port == 21:
                    if self.check_anon_ftp():
                        vuln_info = "[!] VULNERABLE: Anonymous FTP Allowed"
                    else:
                        vuln_info = "FTP Secure"

                # 4. Console Output
                output_str = f"[+] Port {port:<5} OPEN | {service_id} {vuln_info}"
                print(output_str)

                # 5. Store Data for JSON (Thread-safe)
                with self.lock:
                    self.results.append(
                        {
                            "port": port,
                            "status": "open",
                            "service": service_id,
                            "vulnerability": vuln_info,
                        }
                    )

            s.close()
        except Exception as e:
            pass

    def save_json(self):
        if self.output_file:
            data = {
                "target": self.target_ip,
                "scan_time": str(datetime.now()),
                "findings": self.results,
            }
            try:
                with open(self.output_file, "w") as f:
                    json.dump(data, f, indent=4)
                print(f"[*] Results saved to {self.output_file}")
            except Exception as e:
                print(f"[-] Failed to save JSON: {e}")

    def run(self):
        print(f"[*] Starting Scan on {self.target_ip}")
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            ports = range(self.start_port, self.end_port + 1)
            executor.map(self.scan_port, ports)

        self.save_json()
        print("[*] Scan Complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ghost-Scanner: Enterprise Edition")
    parser.add_argument("target", help="Target IP Address")
    parser.add_argument("-p", "--ports", default="1-1024", help="Port range")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Threads")
    parser.add_argument("-o", "--output", help="Save results to JSON file")

    args = parser.parse_args()

    scanner = GhostScanner(args.target, args.ports, args.threads, args.output)
    scanner.run()
