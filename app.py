from flask import Flask, render_template
from flask_socketio import SocketIO, send, request
import random

app = Flask(__name__)
socketio = SocketIO(app)

# Store active users and their assigned colors
active_users = {}

@app.route('/')
def home():
    return render_template('index.html')

@socketio.on('message')
def handle_message(message):
    # Broadcast message to all users with sender color
    send({'user': active_users[request.sid], 'message': message}, broadcast=True)

@socketio.on('connect')
def handle_connect():
    # Assign a random color to each new user
    user_color = "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    active_users[request.sid] = user_color
    print(f'User connected: {request.sid}, assigned color: {user_color}')

@socketio.on('disconnect')
def handle_disconnect():
    # Remove user from the active users list on disconnect
    print(f'User disconnected: {request.sid}')
    if request.sid in active_users:
        del active_users[request.sid]

if __name__ == '__main__':
    socketio.run(app, debug=True)
