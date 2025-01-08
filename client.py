import socket
import threading
import time
import pyperclip

# Server configuration
HOST = '127.0.0.1'  # Server IP address
PORT = 37373        # Same port as server

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                pyperclip.copy(message)
        except:
            print("Disconnected from server")
            break

def send_messages(client_socket, target_user):
    last_clipboard_content = pyperclip.paste()
    print(f"Chatting with {target_user}.")
    while True:
        time.sleep(1)  # Check every second
        clipboard_content = pyperclip.paste()
        if clipboard_content != last_clipboard_content:
            last_clipboard_content = clipboard_content
            message = str("@" + target_user + " " + last_clipboard_content)
            client_socket.send(message.encode('utf-8'))

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print(f"Connected to server at {HOST}:{PORT}")
    USERNAME = input("Enter the username for this machine: ").strip()
    TARGET_USER = input("Enter the username of your peer machine: ").strip()
    client_socket.send(USERNAME.encode('utf-8'))
    # Start threads for receiving and sending messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    send_thread = threading.Thread(target=send_messages, args=(client_socket, TARGET_USER))
    receive_thread.start()
    send_thread.start()

if __name__ == "__main__":
    start_client()