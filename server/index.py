from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import os, json
from model import *
app = Flask(__name__)
CORS(app)  # Bật CORS cho toàn bộ ứng dụng
socketio = SocketIO(app, cors_allowed_origins="*")  # Cho phép tất cả nguồn

@socketio.on('xulydulieu')
def handle_message(msg):
    prd, value = my_predict(msg)
    emit('server_message', {"predict": prd, "value":value})
    print()

@socketio.on('connect')
def handle_connect():
    print('✅ Client connected')

@socketio.on('reloadModel')
def handle_reloadModel(modelName):
    reloadModel(modelName)
@socketio.on('disconnect')
def handle_disconnect():
    print('❌ Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
