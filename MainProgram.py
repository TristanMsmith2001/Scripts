import subprocess
import matplotlib.pyplot as plt
import sqlite3

def main():
    while True:
        choice = show_menu()

        if choice == "A":
            add_router()
        elif choice == "B":
            delete_router()
        elif choice == "C":
            list_routers()
        elif choice == "D":
            set_backup_time()
        elif choice == "E":
            set_router_netflow()
        elif choice == "F":
            remove_router_netflow()
        elif choice == "G":
            set_router_snmp()
        elif choice == "H":
            remove_router_snmp()
        elif choice == "I":
            show_router_config()
        elif choice == "J":
            show_changes_in_config()
        elif choice == "K":
            display_netflow()
        elif choice == "L":
            show_router_syslog()
        elif choice == "M":
            print("Exiting program.")
            break
        else:
            print("Invalid choice, please try again.")

def show_menu():
    print("""
    A) Add Router
    B) Delete Router
    C) List Router
    D) Set Backup Time
    E) Set Router Netflow Settings
    F) Remove Router Netflow Settings
    G) Set Router SNMP Settings
    H) Remove Router SNMP Settings
    I) Show Router Config
    J) Show Changes in Router Config
    K) Display Router Netflow Statistics
    L) Show Router Syslog
    M) Exit
    """)
    return input("Enter the number of your choice: ")

# Functions
def add_router():
    router_name = input("Enter Router Name: ")
    router_ip = input("Enter Router IP: ")
    router_username = input("Enter Router Username: ")
    router_password = input("Enter Router Password: ")
    subprocess.run(["python3", "/home/tristan/Desktop/New Folder/Scripting assignment/ManageDevices.py", "add", router_name, router_ip, router_username, router_password])

def delete_router():
    router_ip = input("Enter Router IP to delete: ")
    subprocess.run(["python3", "/home/tristan/Desktop/New Folder/Scripting assignment/ManageDevices.py", "delete", router_ip])

def list_routers():
    subprocess.run(["python3", "/home/tristan/Desktop/New Folder/Scripting assignment/ManageDevices.py", "list"])

def display_netflow(protocol_data):
    
    protocols = list(protocol_data.keys())
    packet_counts = list(protocol_data.values())

    # Generate pie chart
    plt.figure(figsize=(10, 7))
    plt.pie(packet_counts, labels=protocols, autopct='%1.1f%%', startangle=140)
    plt.title('Packet Distribution by Protocol')
    plt.show()

def set_backup_time():
    backup_time = input("Enter the new backup time (HH:MM): ").strip()
    
    # Connect to the SQLite database
    conn = sqlite3.connect('routers.db')
    cursor = conn.cursor()
    
    # Check if there's already a setting in the table
    cursor.execute("SELECT count(*) FROM backup_settings")
    exists = cursor.fetchone()[0]
    
    if exists:
        # Update the existing backup time
        cursor.execute("UPDATE backup_settings SET backup_time = ? WHERE id = 1", (backup_time,))
    else:
        # Insert a new backup time if the table is empty
        cursor.execute("INSERT INTO backup_settings (id, backup_time) VALUES (1, ?)", (backup_time,))
    
    conn.commit()
    conn.close()

    print(f"Backup time set to {backup_time}.")

def set_router_netflow():
    router_ip = input("Enter the router IP address to set NetFlow settings: ").strip()
    netflow_enabled = input("Enable NetFlow? (yes/no): ").strip().lower() == 'yes'
    
    conn = sqlite3.connect('routers.db')
    cursor = conn.cursor()
    
    # Fetch router ID based on IP
    cursor.execute("SELECT id FROM routers WHERE ip_address = ?", (router_ip,))
    router_id = cursor.fetchone()
    
    if router_id:
        router_id = router_id[0]
        # Insert or update NetFlow settings
        cursor.execute("INSERT OR REPLACE INTO router_netflow_settings (router_id, enabled) VALUES (?, ?)", (router_id, netflow_enabled))
        print("NetFlow settings updated successfully.")
    else:
        print("Router not found.")
    
    conn.commit()
    conn.close()

def remove_router_netflow():
    router_ip = input("Enter the router IP address to remove NetFlow settings: ").strip()

    conn = sqlite3.connect('routers.db')
    cursor = conn.cursor()
    
    # Fetch router ID based on IP
    cursor.execute("SELECT id FROM routers WHERE ip_address = ?", (router_ip,))
    router_id = cursor.fetchone()
    
    if router_id:
        router_id = router_id[0]
        # Delete NetFlow settings for this router
        cursor.execute("DELETE FROM router_netflow_settings WHERE router_id = ?", (router_id,))
        if cursor.rowcount > 0:
            print("NetFlow settings removed successfully.")
        else:
            print("No NetFlow settings found for the specified router.")
    else:
        print("Router not found.")
    
    conn.commit()
    conn.close()

def set_router_snmp():
    router_ip = input("Enter the router IP address to set SNMP settings: ").strip()
    snmp_enabled_input = input("Enable SNMP? (yes/no): ").strip().lower()
    snmp_enabled = snmp_enabled_input == 'yes'
    
    # Only ask for the community string if SNMP is enabled
    snmp_community = ""
    if snmp_enabled:
        snmp_community = input("Enter SNMP community string: ").strip()

    conn = sqlite3.connect('routers.db')
    cursor = conn.cursor()
    
    # Fetch router ID based on IP
    cursor.execute("SELECT id FROM routers WHERE ip_address = ?", (router_ip,))
    router_id_result = cursor.fetchone()
    
    if router_id_result:
        router_id = router_id_result[0]
        # Insert or update SNMP settings
        cursor.execute("""
            INSERT INTO router_snmp_settings (router_id, snmp_enabled, snmp_community)
            VALUES (?, ?, ?)
            ON CONFLICT(router_id) 
            DO UPDATE SET snmp_enabled = excluded.snmp_enabled, 
                          snmp_community = excluded.snmp_community
            """, (router_id, snmp_enabled, snmp_community))
        print("SNMP settings updated successfully.")
    else:
        print("Router not found.")
    
    conn.commit()
    conn.close()

def set_router_snmp():
    # Prompt for router IP and SNMP settings
    router_ip = input("Enter the router IP address to set SNMP settings: ").strip()
    snmp_enabled_input = input("Enable SNMP? (yes/no): ").strip().lower()
    snmp_enabled = snmp_enabled_input == 'yes'
    
    snmp_community = ""
    if snmp_enabled:
        snmp_community = input("Enter SNMP community string: ").strip()

    # Connect to the database
    conn = sqlite3.connect('routers.db')
    cursor = conn.cursor()
    
    # Attempt to fetch the router ID based on the provided IP
    cursor.execute("SELECT id FROM routers WHERE ip_address = ?", (router_ip,))
    router_id_result = cursor.fetchone()
    
    if router_id_result:
        router_id = router_id_result[0]
        # Check if SNMP settings already exist for this router
        cursor.execute("SELECT COUNT(*) FROM router_snmp_settings WHERE router_id = ?", (router_id,))
        exists = cursor.fetchone()[0] > 0

        if exists:
            # Update existing SNMP settings
            cursor.execute("""
                UPDATE router_snmp_settings
                SET snmp_enabled = ?, snmp_community = ?
                WHERE router_id = ?
                """, (snmp_enabled, snmp_community, router_id))
        else:
            # Insert new SNMP settings
            cursor.execute("""
                INSERT INTO router_snmp_settings (router_id, snmp_enabled, snmp_community)
                VALUES (?, ?, ?)
                """, (router_id, snmp_enabled, snmp_community))
        
        print("SNMP settings updated successfully.")
    else:
        print("Router not found.")

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def remove_router_snmp():
    # Prompt the user for the router's IP address
    router_ip = input("Enter the router IP address to remove SNMP settings: ").strip()

    # Connect to the SQLite database
    conn = sqlite3.connect('routers.db')
    cursor = conn.cursor()
    
    # First, find the router's ID using the provided IP address
    cursor.execute("SELECT id FROM routers WHERE ip_address = ?", (router_ip,))
    router_id_result = cursor.fetchone()
    
    if router_id_result:
        router_id = router_id_result[0]
        # Delete the SNMP settings for the router with the fetched ID
        cursor.execute("DELETE FROM router_snmp_settings WHERE router_id = ?", (router_id,))
        if cursor.rowcount > 0:
            print("SNMP settings removed successfully.")
        else:
            print("No SNMP settings found for the specified router.")
    else:
        print("Router not found.")

    # Commit the transaction and close the database connection
    conn.commit()
    conn.close()
def show_router_config():
    # Prompt the user for the router's IP address
    router_ip = input("Enter the router IP address to view its configuration: ").strip()

    # Connect to the SQLite database
    conn = sqlite3.connect('routers.db')
    cursor = conn.cursor()
    
    # Fetch the router's configuration details using the provided IP address
    cursor.execute("""
        SELECT name, ip_address, username, password
        FROM routers
        WHERE ip_address = ?
    """, (router_ip,))
    router_config = cursor.fetchone()
    
    if router_config:
        # Display the router's configuration details
        print("Router Configuration:")
        print(f"Name: {router_config[0]}")
        print(f"IP Address: {router_config[1]}")
        print(f"Username: {router_config[2]}")
        print(f"Password: {router_config[3]}")
    else:
        print("Router not found.")

    # Close the database connection
    conn.close()

def show_changes_in_config():
    main()

def show_router_syslog():
    main()


if __name__ == '__main__':
    main()
