import sqlite3
import time
import paramiko
from datetime import datetime

# and 'routers' table with the necessary router details.

def get_backup_time():
    conn = sqlite3.connect('routers.db')
    cursor = conn.cursor()
    cursor.execute("SELECT time FROM backup_schedule LIMIT 1")
    backup_time = cursor.fetchone()[0]
    conn.close()
    return backup_time

def get_routers():
    conn = sqlite3.connect('routers.db')
    cursor = conn.cursor()
    cursor.execute("SELECT ip_address, username, password FROM routers")
    routers = cursor.fetchall()
    conn.close()
    return routers

def backup_router(router):
    ip_address, username, password = router
    # Connect to the router using SSH and copys the running config
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=ip_address, username=username, password=password)
        stdin, stdout, stderr = ssh_client.exec_command('show running-config')
        router_config = stdout.read().decode('utf-8')
        with open(f'{ip_address}.config', 'w') as file:
            file.write(router_config)
        ssh_client.close()
        print(f"Backup for {ip_address} completed successfully.")
    except Exception as e:
        print(f"An error occurred while backing up {ip_address}: {e}")

def perform_backups():
    routers = get_routers()
    for router in routers:
        backup_router(router)

def main():
    while True:
        current_time = datetime.now().strftime('%H:%M')
        backup_time = get_backup_time()
        if current_time == backup_time:
            perform_backups()
        time.sleep(60)  # Waits 1min beofre trying again

if __name__ == '__main__':
    main()
