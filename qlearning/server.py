from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import json, os
from db import *
from q_agent import *

app = Flask(__name__)
CORS(app)  # Bật CORS cho toàn bộ ứng dụng
socketio = SocketIO(app, cors_allowed_origins="*")  # Cho phép tất cả nguồn


@socketio.on('message')
def handle_message(msg):
    hs = json.loads(msg) 
    addData(hs["sid"], hs["mB"], hs["mW"], hs["uB"], hs["uW"], hs["xx1"], hs["xx2"], hs["xx3"], hs["rs18"], hs["prf"])
    npdata = readHs(int(hs['sid']))
    if len(npdata) == 0:
        print('No data found')
        return
    state = makeState(npdata)
    print(state)
    action = Q_bot.play_game(state)
    print(action)
    (choice, value) = action.split('_')
    #tai eid1, xiu eid2
    if choice == "black":
        choice = 1
    else:
        choice = 2

    emit('response', json.dumps({"eid": choice,"b": int(value)*10000}))

@socketio.on('connect')
def handle_connect():
    os.system('clear')
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)