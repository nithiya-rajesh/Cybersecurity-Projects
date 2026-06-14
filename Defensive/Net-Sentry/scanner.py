import socket
import threading
from queue import Queue
import time

# CONFIGURATION
TARGET_IP = "scanme.nmap.org"
START_PORT = 1
END_PORT = 1024 # Scanning the "Well Known Ports" range
THREAD_COUNT = 50 # How many threads to run at once

# Thread-safe queue to hold the ports we want to scan
port_queue = Queue()
open_ports = [] # List to store results

def grab_banner(s):
    try:
        s.settimeout(2.0)
        return s.recv(1024).decode().strip()
    except:
        return "No Banner"

def scan_port(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        result = s.connect_ex((TARGET_IP, port))
        
        if result == 0:
            # If open, try to grab banner
            if port == 80:
                s.send(b"HEAD / HTTP/1.1\r\n\r\n")
            banner = grab_banner(s)
            
            # Save the result safely
            output = f"Port {port} OPEN : {banner}"
            print(f"[+] {output}") # Print immediately
            open_ports.append(output)
            
        s.close()
    except:
        pass

def worker():
    """
    The worker thread function.
    It grabs a port from the queue, scans it, and repeats until queue is empty.
    """
    while not port_queue.empty():
        port = port_queue.get()
        scan_port(port)
        port_queue.task_done()

# --- MAIN EXECUTION ---
print(f"[*] Starting Multi-Threaded Scan on {TARGET_IP}")
print(f"[*] Scanning ports {START_PORT}-{END_PORT} with {THREAD_COUNT} threads...")
print("-" * 50)

start_time = time.time()

# 1. Fill the Queue
for port in range(START_PORT, END_PORT + 1):
    port_queue.put(port)

# 2. Create and Start Threads
thread_list = []
for _ in range(THREAD_COUNT):
    t = threading.Thread(target=worker)
    t.start()
    thread_list.append(t)

# 3. Wait for all threads to finish
for t in thread_list:
    t.join()

end_time = time.time()
duration = end_time - start_time

print("-" * 50)
print(f"[*] Scan Complete in {duration:.2f} seconds.")
print(f"[*] Found {len(open_ports)} open ports.")