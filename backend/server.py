from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room
import json, os

config_file_name = 'config.json'

if not os.path.exists(config_file_name):
    config_file_name = 'config.json.cfg'

with open(config_file_name, 'r') as config_file:
    config = json.load(config_file)
    
app = Flask(__name__)
app.config['SECRET_KEY'] = config['flask']['secret_key']
app.config['LOG_FILE'] = config['app']['log_file']
socketio = SocketIO(app)


active_users = {}


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def handle_connect():
    username = request.headers['username']
    active_users[username] = request.sid
    print(f'{username} has connected')
    join_room(username)


@socketio.on('private_message')
def handle_private_message(data):
    sender = data['sender']
    receiver = data['receiver']
    message = data['message']
    

    if sender in active_users:
        receiver_sid = active_users.get(receiver)
        if receiver_sid:
            socketio.emit('private_message', {'sender': sender, 'message': message}, room=receiver_sid)
        else:
            socketio.emit('private_message', {'sender': 'Server', 'message': 'User not found.'}, room=request.sid)
    else:
        socketio.emit('private_message', {'sender': 'Server', 'message': 'Invalid sender username.'}, room=request.sid)



@socketio.on('disconnect')
def handle_disconnect():
    username = [k for k, v in active_users.items() if v == request.sid][0]
    del active_users[username]
    leave_room(username)
    print(f'{username} has disconnected')


if __name__ == '__main__':
    socketio.run(app, debug=True)
