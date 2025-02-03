import json, os, sys
import random
from db import *
def stop():
    sys.exit()


class QLearningAgent:
    def __init__(self):
        self.learning_rate = 0.1  # Hệ số học
        self.discount_factor = 0.9  # Hệ số giảm giá
        self.exploration_rate = 0.1  # Tỉ lệ khám phá
        self.load_q_table()
        self.actions = makeActions()


    def get_q_value(self, state, action):
        """Lấy giá trị Q của một trạng thái và hành động."""
        return self.q_table.get(state, {}).get(action, 0.0)

    def choose_action(self, state):
        """Chọn hành động dựa trên epsilon-greedy."""
        if state not in self.q_table:
            self.q_table[state] = {action: 0.0 for action in self.actions}  # Tạo trạng thái mới và gán giá trị Q cho tất cả hành đ��ng
            return random.choice(list(self.actions))
        if random.random() < self.exploration_rate:
            return random.choice(list(self.actions))
        else:
            # Khai thác giá trị Q tốt nhất
            # q_values = {action: self.get_q_value(state, action) for action in self.actions}
            # return max(q_values, key=q_values.get)
            best_action = max(self.q_table[state], key=self.q_table[state].get)
            return best_action
    def play_game(self, state):
        if state not in self.q_table:
            return "black_0"
        return max(self.q_table[state], key=self.q_table[state].get)
    def update_q_value(self, state, action, reward, next_state):
        """Cập nhật Q-Table theo công thức Q-Learning."""
        if next_state not in self.q_table:
            self.q_table[next_state] = {action: 0.0 for action in self.actions}  # Tạo trạng thái mới và gán giá trị Q cho tất cả hành đ��ng
        old_value = self.get_q_value(state, action)
        next_max = max(self.q_table[next_state].values())
        new_value = old_value + self.learning_rate * (reward + self.discount_factor * next_max - old_value)
        
        # Cập nhật Q-Table
        # if state not in self.q_table:
        #     self.q_table[state] = {}
        self.q_table[state][action] = new_value

    def save_q_table(self, file_path = 'q_table.json'):
        """Lưu Q-Table vào file JSON."""
        with open(file_path, 'w') as f:
            json.dump(self.q_table, f, indent=2)

    def load_q_table(self, file_path = 'q_table.json'):
        """Tải Q-Table từ file JSON."""
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                self.q_table = json.load(f)
        else:
            self.q_table = {}







# def makeState(npdata):
#     def getPercent(A, B):
#         return round(A/B, 1)
#     print(npdata)
#     total_profit = sum(npdata[:,-1])
#     total_profit = round((total_profit/1000000000), 1)*10
#     hs_result = npdata[:,-2]
#     hs_result = [i>10 for i in hs_result]
#     lastHs = npdata[-1]
#     result = lastHs[-2]
#     pm = getPercent(lastHs[2], lastHs[3])
#     pu = getPercent(lastHs[4], lastHs[5])
#     return f"|{total_profit}|{pm}|{pu}|{result}"
def makeState(npdata):
    state = []
    for row in npdata:
        pm = int(row[2]) > int(row[3])
        pu = int(row[4]) > int(row[5])
        rs = row[-2] > 10
        state.append(pm)
        state.append(pu)
        state.append(rs)
    return str(state)
    return f"|{pm}| |{pu}|{result}"

def makeActions():
    choices = ["black","white"]
    values = [1, 5, 9]
    actions = []
    for c in choices:
        for v in values:
            actions.append(f"{c}_{v}")
    return actions
def callReward(action, next_state):
    (choice, value) = action.split('_')
    value = int(value)
    result = "white"
    if next_state[-2]>10:
        result = "black"
    if choice == result:
        return value
    return -value



def train(number_epoch = 100):
    df = readTable()
    sids = list(df['sid'])
    Q_bot = QLearningAgent()
    for e in range(number_epoch):
        print("Training",e)
        for index, row in df.iterrows():
            sid = int(row['sid'])
            npdata = readHs(sid)
            npdata_next = readHs(sid+1)
            if len(npdata)==0 or len(npdata_next)==0:
                continue
            state = makeState(npdata)
            next_state = makeState(npdata_next)
            action = Q_bot.choose_action(state)
            reward = callReward(action, npdata_next[-1])
            Q_bot.update_q_value(state, action, reward, next_state)
    Q_bot.save_q_table()




#fix state mb-mw
