from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import os
from handle_data import *
app = Flask(__name__)
CORS(app)  # Bật CORS cho toàn bộ ứng dụng
socketio = SocketIO(app, cors_allowed_origins="*")  # Cho phép tất cả nguồn

@socketio.on('xulydulieu')
def handle_message(msg):
    # print("📨 Nhận từ client:", msg)
    data = handle_progress(msg, isEnd=False)
    print(data)
    emit('server_message', {"server_mess": "👋 Xin chào từ server!"})

@socketio.on('connect')
def handle_connect():
    # os.system('cls' if os.name == 'nt' else 'clear')
    print('✅ Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    # os.system('cls' if os.name == 'nt' else 'clear')
    print('❌ Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
