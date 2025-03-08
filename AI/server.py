from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import json
from db import addData
# from models import makePredict
from newprd import predict



app = Flask(__name__)
CORS(app)  # Bật CORS cho toàn bộ ứng dụng
socketio = SocketIO(app, cors_allowed_origins="*")  # Cho phép tất cả nguồn



@socketio.on('message')
def handle_message(msg):
    hs_json = json.loads(msg)
    print(hs_json["sid"])
    [xx1, xx2, xx3] = sorted([hs_json["xx1"], hs_json["xx2"], hs_json["xx3"]])
    hs_arr =  [hs_json["sid"], hs_json["mB"], hs_json["mW"], hs_json["uB"], hs_json["uW"], xx1, xx2, xx3, hs_json["rs18"], hs_json["prf"]]

    addData(hs_arr)
    # predictions = makePredict(hs_json['sid'])
    predictions = predict()
    emit('response', json.dumps({"predictions":predictions}))
    

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)