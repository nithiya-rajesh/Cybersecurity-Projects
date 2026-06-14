import csv
import random
from datetime import datetime, timedelta
from faker import Faker

# Setup
fake = Faker()
log_file = "auth_logs.csv"
num_records = 1000

# The "Attacker" Profile
attacker_ip = "192.168.1.105"
target_users = [fake.user_name() for _ in range(10)] # 10 specific targets

print(f"Generating {num_records} log entries...")
print(f"SIMULATING ATTACK: IP {attacker_ip} is spraying {len(target_users)} accounts.")

with open(log_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['timestamp', 'username', 'source_ip', 'status'])

    start_time = datetime.now() - timedelta(hours=24)

    for i in range(num_records):
        # 1. Advance time slightly
        start_time += timedelta(seconds=random.randint(1, 60))
        timestamp = start_time.strftime('%Y-%m-%d %H:%M:%S')

        # 2. Determine if this is part of the attack or normal traffic
        if i % 50 == 0 and len(target_users) > 0: 
            # Inject Attack Traffic (Every 50th record roughly)
            user = target_users.pop() # Pick a target
            ip = attacker_ip
            status = "Failed" # Sprays usually fail
        else:
            # Normal Traffic
            user = fake.user_name()
            ip = fake.ipv4()
            status = random.choice(["Success", "Success", "Failed"]) # Mostly success

        writer.writerow([timestamp, user, ip, status])

print(f"Done! Created {log_file}. Check your folder.")