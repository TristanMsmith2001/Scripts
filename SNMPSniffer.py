from scapy.all import sniff, IP, UDP
from scapy.layers.snmp import SNMP, SNMPtrap
import sqlite3
from datetime import datetime

# Define the OIDs for SYSLOG, LINK UP, and LINK DOWN traps
SYSLOG_OID = '1.3.6.1.4.1.0.1'  # Placeholder OID for SYSLOG
LINK_UP_OID = '1.3.6.1.6.3.1.1.5.4'  # Standard LINK UP Notification OID
LINK_DOWN_OID = '1.3.6.1.6.3.1.1.5.3'  # Standard LINK DOWN Notification OID

def setup_database():
    conn = sqlite3.connect('snmp_traps.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS traps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            time TEXT,
            router_ip TEXT,
            message TEXT,
            interface_name TEXT,
            state TEXT
        )
    ''')
    conn.commit()
    conn.close()

def parse_trap(packet):
    # Check for SNMP trap
    if SNMP in packet:
        # Extract trap data
        varbinds = packet[SNMP].varbindlist
        # Determine type of trap and process accordingly
        for varbind in varbinds:
            oid, value = varbind.oid, varbind.value
            if str(oid) == SYSLOG_OID:
                process_syslog_trap(packet, value)
            elif str(oid) == LINK_UP_OID or str(oid) == LINK_DOWN_OID:
                process_link_trap(packet, oid, value)

def process_syslog_trap(packet, message):
    # Extract data for SYSLOG trap
    date = datetime.now().strftime('%Y-%m-%d')
    time = datetime.now().strftime('%H:%M:%S')
    router_ip = packet[IP].src
    save_trap(date, time, router_ip, message.decode(), None, None)

def process_link_trap(packet, oid, interface_name):
    # Extract data for LINK UP/DOWN trap
    date = datetime.now().strftime('%Y-%m-%d')
    time = datetime.now().strftime('%H:%M:%S')
    router_ip = packet[IP].src
    state = 'UP' if str(oid) == LINK_UP_OID else 'DOWN'
    save_trap(date, time, router_ip, None, interface_name.decode(), state)

def save_trap(date, time, router_ip, message, interface_name, state):
    conn = sqlite3.connect('snmp_traps.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO traps (date, time, router_ip, message, interface_name, state)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (date, time, router_ip, message, interface_name, state))
    conn.commit()
    conn.close()

def start_sniffer():
    print("Starting SNMP sniffer...")
    sniff(filter="udp port 161", prn=parse_trap)

if __name__ == '__main__':
    setup_database()
    start_sniffer()
