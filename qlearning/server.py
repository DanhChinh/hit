from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import json
from db import addData
from trainTree import *



app = Flask(__name__)
CORS(app)  # Bật CORS cho toàn bộ ứng dụng
socketio = SocketIO(app, cors_allowed_origins="*")  # Cho phép tất cả nguồn



@socketio.on('message')
def handle_message(msg):
    hs = json.loads(msg) 
    addData(hs["sid"], hs["mB"], hs["mW"], hs["uB"], hs["uW"], hs["xx1"], hs["xx2"], hs["xx3"], hs["rs18"], hs["prf"])
    record = [hs["mB"], hs["mW"], hs["uB"], hs["uW"], hs["xx1"], hs["xx2"], hs["xx3"], hs["rs18"], hs["prf"]]
    xy_test.addData(record)


    

    emit('response', json.dumps({"eid": choice,"b": value}))

@socketio.on('connect')
def handle_connect():
    # os.system('clear')
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)