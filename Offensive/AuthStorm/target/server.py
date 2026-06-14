from flask import Flask, request, jsonify
import time
import logging
import json
import os

app = Flask(__name__)

# --- DOCKER-READY CONFIGURATION ---
# 1. Get the base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 2. Define a default local path
DEFAULT_LOG = os.path.join(BASE_DIR, "access.log")
# 3. CRITICAL: Check if Docker passed us a specific 'LOG_PATH'
LOG_FILE = os.getenv("LOG_PATH", DEFAULT_LOG)

# Create a custom logger
logger = logging.getLogger("AuthLogger")
logger.setLevel(logging.INFO)
if logger.hasHandlers():
    logger.handlers.clear()

# Ensure the directory exists (Crucial for Docker volumes)
log_dir = os.path.dirname(LOG_FILE)
if log_dir and not os.path.exists(log_dir):
    os.makedirs(log_dir)

file_handler = logging.FileHandler(LOG_FILE)
logger.addHandler(file_handler)

def log_request(status_code, message):
    log_entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "src_ip": request.remote_addr,
        "method": request.method,
        "endpoint": request.path,
        "status_code": status_code,
        "user_agent": request.headers.get("User-Agent"),
        "message": message
    }
    logger.info(json.dumps(log_entry))

VALID_USER = "admin"
VALID_PASS = "password123"

@app.route('/login', methods=['POST'])
def login():
    time.sleep(0.1)
    data = request.get_json(silent=True)
    if not data:
        log_request(400, "Malformed Request")
        return jsonify({"error": "No data"}), 400

    username = data.get('username')
    password = data.get('password')

    if username == VALID_USER and password == VALID_PASS:
        log_request(200, f"Login Success: {username}")
        return jsonify({"message": "Login Successful"}), 200
    else:
        log_request(401, f"Login Failed: {username}")
        return jsonify({"message": "Invalid Credentials"}), 401

if __name__ == '__main__':
    print(f"[*] Enterprise Server Running.")
    print(f"[*] LOG FILE LOCATION: {LOG_FILE}") 
    
    # Create the file immediately to trigger the SIEM
    with open(LOG_FILE, 'a') as f:
        pass 
        
    # Listen on 0.0.0.0 for Docker
    app.run(debug=True, host='0.0.0.0', port=5000)