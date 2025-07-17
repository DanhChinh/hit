from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import os, json
from agl import *
app = Flask(__name__)
CORS(app)  # Bật CORS cho toàn bộ ứng dụng
socketio = SocketIO(app, cors_allowed_origins="*")  # Cho phép tất cả nguồn

@socketio.on('xulydulieu')
def handle_message(msg):

    x_new_raw = handle_progress(msg, isEnd=False)
    print(x_new_raw)
    x_new_raw = is_pass_filtered(scaler, x_new_raw, X_filtered, y_filtered)
    print(x_new_raw)

    # prd, value = my_predict(x_test)
    # emit('server_message', {"predict": prd, "value":value})

@socketio.on('connect')
def handle_connect():
    print('✅ Client connected')

@socketio.on('getAgl')
def handle_getAgl():
    load_polot_data()
    emit('agl', plot_data)
@socketio.on('disconnect')
def handle_disconnect():
    print('❌ Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
