from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow CORS for all origins

# Store WebRTC session information
clients = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/client')
def client():
    return render_template('client.html')

@socketio.on('join')
def handle_join(data):
    clients[request.sid] = data
    print(f"Client joined: {data}")
    emit('update_clients', list(clients.values()), broadcast=True)

@socketio.on('offer')
def handle_offer(data):
    print(f"Received offer from {request.sid}: {data}")
    emit('offer', data, room=data['to'])

@socketio.on('answer')
def handle_answer(data):
    print(f"Received answer from {request.sid}: {data}")
    emit('answer', data, room=data['to'])

@socketio.on('candidate')
def handle_candidate(data):
    print(f"Received ICE candidate from {request.sid}: {data}")
    emit('candidate', data, room=data['to'])

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in clients:
        del clients[request.sid]
        print(f"Client disconnected: {request.sid}")
        emit('update_clients', list(clients.values()), broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
