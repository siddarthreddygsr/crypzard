import socketio
import threading

sio = socketio.Client()

username = input("Enter your username: ")

@sio.event
def connect():
    print('Connected to the server')
    sio.emit('connect', username, namespace='/')

@sio.event
def private_message(data):
    print(f'{data["sender"]}: {data["message"]}')

def send_message():
    while True:
        message = input()
        if message:
            receiver = input("Enter the receiver's username: ")
            sio.emit('private_message', {'sender': username, 'receiver': receiver, 'message': message}, namespace='/')

if __name__ == '__main__':
    sio.connect('http://127.0.0.1:5000', namespaces=['/'], headers={'username': username})
    t = threading.Thread(target=send_message)
    t.daemon = True
    t.start()
    sio.wait()
