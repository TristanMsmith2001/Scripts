import socket
import sqlite3
import ssl
import json

def handle_client(conn, addr):
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            # Decrypt and process the request
            request = json.loads(data.decode())
            response = process_request(request)
            # Encrypt and send the response
            conn.sendall(json.dumps(response).encode())

def process_request(request):
    # This function will process the request (Add, Delete, List) and interact with the SQLite database.
    pass

def main():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    certfile_path = '/home/tristan/Desktop/New Folder/Scripting assignment/Scripts/cert.pem'
    keyfile_path = '/home/tristan/Desktop/New Folder/Scripting assignment/Scripts/key.pem'
    context.load_cert_chain(certfile=certfile_path, keyfile=keyfile_path)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.bind(('localhost', 12345))
        sock.listen(5)
        with context.wrap_socket(sock, server_side=True) as ssock:
            while True:
                conn, addr = ssock.accept()
                handle_client(conn, addr)

def process_request(request):
    if request['command'] == 'add':
        return add_router(request['data'])
    elif request['command'] == 'delete':
        return delete_router(request['data'])
    elif request['command'] == 'list':
        return list_routers()
    else:
        return {'status': 'error', 'message': 'Invalid command'}

# add a router
def add_router(data):
    try:
        conn = sqlite3.connect('routers.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO routers (name, ip_address, username, password) VALUES (?, ?, ?, ?)',
                       (data['name'], data['ip_address'], data['username'], data['password']))
        conn.commit()
        return {'status': 'success', 'message': 'Router added'}
    except sqlite3.IntegrityError:
        return {'status': 'error', 'message': 'IP Address must be unique'}
    finally:
        conn.close()

# Delete a router
def delete_router(data):
    try:
        conn = sqlite3.connect('routers.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM routers WHERE ip_address = ?', (data['ip_address'],))
        conn.commit()
        if cursor.rowcount == 0:
            return {'status': 'error', 'message': 'Router not found.'}
        else:
            return {'status': 'success', 'message': 'Router deleted successfully.'}
    finally:
        conn.close()

# List all routers
def list_routers():
    try:
        conn = sqlite3.connect('routers.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name, ip_address, username, password FROM routers')
        routers = cursor.fetchall()
        router_list = [{'name': router[0], 'ip_address': router[1], 'username': router[2], 'password': router[3]} for router in routers]
        return {'status': 'success', 'data': router_list}
    finally:
        conn.close()


if __name__ == '__main__':
    main()



