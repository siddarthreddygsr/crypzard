import socket
import threading

# Create a socket, bind it, and listen for connections
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12345))
server_socket.listen(5)
print("Server is listening for incoming connections...")

# Create a list to store client connections and usernames
clients = []
usernames = {}


# Broadcast messages to all clients
def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except:
                remove(client)


# Remove a client from the list
def remove(client):
    if client in clients:
        clients.remove(client)
        username = usernames[client]
        del usernames[client]
        broadcast(f"{username} has left the chat.".encode('utf-8'), client)


# Handle client connections and messages
def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                remove(client_socket)
                break
            elif message.decode('utf-8').startswith('@'):
                # The message is a private message
                receiver_username, message = message.decode('utf-8').split(' ', 1)
                receiver_username = receiver_username[1:]  # Remove the '@' character
                send_private_message(message, usernames[client_socket], receiver_username)
            else:
                # Broadcast regular messages
                broadcast(message, client_socket)
        except:
            continue


# Send a private message to a specific client
def send_private_message(message, sender_username, receiver_username):
    for client, username in usernames.items():
        if username == receiver_username:
            try:
                client.send(f"{sender_username}: {message}".encode('utf-8'))
            except:
                remove(client)


# Accept incoming connections and start a thread for each client
while True:
    client_socket, client_address = server_socket.accept()
    client_socket.send("Welcome to the chat! Please enter your username:".encode('utf-8'))
    username = client_socket.recv(1024).decode('utf-8')
    clients.append(client_socket)
    usernames[client_socket] = username
    print(f"{username} has connected from {client_address[0]}:{client_address[1]}")
    broadcast(f"{username} has joined the chat.".encode('utf-8'), client_socket)
    client_socket.send("You are now connected!".encode('utf-8'))
    thread = threading.Thread(target=handle_client, args=(client_socket,))
    thread.start()
