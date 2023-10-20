import socket
import threading

# Create a socket and connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 12345))  # Replace 'server_ip' with the actual IP address of your server

# Create a function to send messages
def send_message():
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))

# Create a thread for sending messages
send_thread = threading.Thread(target=send_message)
send_thread.start()

# Create a function to receive and display messages
def receive_message():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            print("An error occurred.")
            client_socket.close()
            break

# Create a thread for receiving messages
receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

# Run the CLI application
if __name__ == "__main__":
    receive_thread.join()
    send_thread.join()

