import sqlite3
from scapy.all import sniff, IP, UDP

def setup_database():
    conn = sqlite3.connect('netflow.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS netflow_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            time TEXT,
            router_ip TEXT,
            num_packets INTEGER,
            src_ip TEXT,
            dst_ip TEXT,
            protocol TEXT,
            src_port INTEGER,
            dst_port INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def handle_packet(packet):
    if IP in packet and UDP in packet and packet[UDP].dport == 2055:

        date = '2024-02-04'
        time = '12:00:00'
        router_ip = packet[IP].src
        num_packets = 10  
        src_ip = '1.2.3.4' 
        dst_ip = '5.6.7.8'  
        protocol = 'TCP'  
        src_port = 12345 
        dst_port = 80 

        # Save to database
        save_to_database(date, time, router_ip, num_packets, src_ip, dst_ip, protocol, src_port, dst_port)

def save_to_database(date, time, router_ip, num_packets, src_ip, dst_ip, protocol, src_port, dst_port):
    conn = sqlite3.connect('netflow.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO netflow_data (date, time, router_ip, num_packets, src_ip, dst_ip, protocol, src_port, dst_port)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (date, time, router_ip, num_packets, src_ip, dst_ip, protocol, src_port, dst_port))
    conn.commit()
    conn.close()

def start_sniffer():
    print("Starting NetFlow sniffer...")
    sniff(filter="udp port 2055", prn=handle_packet)

if __name__ == '__main__':
    setup_database()
    start_sniffer()
