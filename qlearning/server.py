from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import json
import numpy as np
from q_agent import *
app = Flask(__name__)
CORS(app)  # Bật CORS cho toàn bộ ứng dụng
socketio = SocketIO(app, cors_allowed_origins="*")  # Cho phép tất cả nguồn

QBot = QLearningAgent()

state_list = []
action_list = []
reward_list = []
choice_list = []

@socketio.on('message')
def handle_message(msg):
    global state_list, action_list, reward_list
    print()
    gameinfo_list = json.loads(msg)
    if len(gameinfo_list) == 0:
        return

    state = makeState(gameinfo_list[-1])
    state_list.append(state)

    action = QBot.choose_action(state, gameinfo_list[-1])
    action_list.append(action)

    choice = int(action.split('_')[0])
    choice_list.append(choice)

    reward = int(action.split('_')[1])
    reward_list.append(reward)

    print("state", state)
    print("action", action)
    print(f"{choice}->{reward}")

    #update
    if len(state_list)>1:
        print("update")
        state = state_list[-2]
        next_state = state_list[-1]
        action = action_list[-2]
        choice = choice_list[-2]
        reward = reward_list[-2]
        result = 1
        if gameinfo_list[-1]['result_18']<=10:
            result = 0
        if result != choice:
            reward *= -1
        print("result_18:", gameinfo_list[-1]['result_18'])
        print("reward:", reward)
        QBot.update_q_value(state, action, reward, next_state, gameinfo_list[-1])
        QBot.save_q_table()




    # emit('response', json.dumps({"content": prd}))

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)