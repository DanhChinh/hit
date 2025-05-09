from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import json, time




app = Flask(__name__)
CORS(app)  # Bật CORS cho toàn bộ ứng dụng
socketio = SocketIO(app, cors_allowed_origins="*")  # Cho phép tất cả nguồn



@socketio.on('message')
def handle_message(msg):
    print("receive", msg)
    time.sleep(1)
    data = {"predictions":1}
    emit('response', data)
    print("send", data)
    

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)