from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import json
from db import addData
from liveTrain import *



app = Flask(__name__)
CORS(app)  # Bật CORS cho toàn bộ ứng dụng
socketio = SocketIO(app, cors_allowed_origins="*")  # Cho phép tất cả nguồn



@socketio.on('message')
def handle_message(msg):
    hs_json = json.loads(msg)
    [xx1, xx2, xx3] = sorted([hs_json["xx1"], hs_json["xx2"], hs_json["xx3"]])
    hs_arr =  [hs_json["sid"], hs_json["mB"], hs_json["mW"], hs_json["uB"], hs_json["uW"], xx1, xx2, xx3, hs_json["rs18"], hs_json["prf"]]

    addData(hs_arr)
    record = hs_arr[1:]
    xy_test.addData(record)
    if len(xy_test.x)<=5:
        print(f"{len(xy_test.x)}/5")
        emit('response', json.dumps({"eid": 1,"b": 0}))
    else:
        x_test, y_test, x_prd = xy_test.makeXYtest()
        print(x_test)
        print(y_test)
        print(x_prd)
        getBestDatatrain(x_test, y_test)
        eid, b = predict(x_prd)
        print(eid, b)
        emit('response', json.dumps({"eid": eid,"b": b}))

@socketio.on('connect')
def handle_connect():
    # os.system('clear')
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)