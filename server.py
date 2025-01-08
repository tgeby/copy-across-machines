import socket
import threading
import sys

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 37373        # Arbitrary non-privileged port

clients = {}  # Dictionary to map usernames to client sockets

def handle_client(client_socket):
    try:
        # Receive a username
        # The first thing the client does is send its username

        username = client_socket.recv(1024).decode('utf-8').strip()
    
        if username in clients:
            client_socket.send("Username already taken. Restart app.".encode('utf-8'))
            sys.exit()
        
        # Register the client
        clients[username] = client_socket
        print(f"{username} connected.")
        
        # Handle messages
        while True:
            message = client_socket.recv(1024).decode('utf-8').strip()
            if not message:
                break
            
            # Check for private message syntax
            if message.startswith('@'):
                try:
                    target_username, msg = message[1:].split(' ', 1)
                    send_private_message(username, target_username, msg)
                except ValueError:
                    client_socket.send("Invalid message format. Use `@<username> <message>`.\n".encode('utf-8'))
            else:
                client_socket.send("Use `@<username> <message>` to send a private message.\n".encode('utf-8'))
    
    except Exception as e:
        print(f"Error with client {client_socket}: {e}")
    
    finally:
        # Cleanup on disconnect
        for user, socket in clients.items():
            if socket == client_socket:
                del clients[user]
                print(f"{user} disconnected.")
                break
        client_socket.close()

def send_private_message(sender, recipient, message):
    if recipient in clients:
        try:
            clients[recipient].send(message.encode('utf-8'))
        except:
            print(f"Error sending message to {recipient}.")
    else:
        clients[sender].send(f"User {recipient} not found.\n".encode('utf-8'))

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server listening on {HOST}:{PORT}")
    
    while True:
        client_socket, _ = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()