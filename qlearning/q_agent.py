import json, os
import random

class QLearningAgent:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, exploration_rate=0.1):
        self.learning_rate = learning_rate  # Hệ số học
        self.discount_factor = discount_factor  # Hệ số giảm giá
        self.exploration_rate = exploration_rate  # Tỉ lệ khám phá
        self.load_q_table()

    def get_q_value(self, state, action):
        """Lấy giá trị Q của một trạng thái và hành động."""
        return self.q_table.get(state, {}).get(action, 0.0)

    def choose_action(self, state, GAME_INFO):
        """Chọn hành động dựa trên epsilon-greedy."""
        if state not in self.q_table:
            actions = makeActions(GAME_INFO)
            self.q_table[state] = {action: 0.0 for action in actions}  # Tạo trạng thái mới và gán giá trị Q cho tất cả hành đ��ng
            return random.choice(list(actions))
        if random.random() < self.exploration_rate:
            actions = self.q_table[state].keys()
            return random.choice(list(actions))  # Khám phá
        else:
            # Khai thác giá trị Q tốt nhất
            # q_values = {action: self.get_q_value(state, action) for action in self.actions}
            # return max(q_values, key=q_values.get)
            best_action = max(self.q_table[state], key=self.q_table[state].get)
            return best_action

    def update_q_value(self, state, action, reward, next_state, GAME_INFO):
        """Cập nhật Q-Table theo công thức Q-Learning."""
        if next_state not in self.q_table:
            actions = makeActions(GAME_INFO)
            self.q_table[next_state] = {action: 0.0 for action in actions}  # Tạo trạng thái mới và gán giá trị Q cho tất cả hành đ��ng
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








def makeState(GAME_INFO):
    #profitList 
    l = min(len(GAME_INFO['profitList']), 10)
    profitList10 = GAME_INFO['profitList'][-l:]
    fixnumber500M = 500000000
    totalFixed = round(sum(profitList10)/fixnumber500M)*fixnumber500M
    fixnumber100M = 100000000
    coefficient_money = round((GAME_INFO['moneyOfBlack'] - GAME_INFO['moneyOfWhite'])/fixnumber100M)* fixnumber100M
    coefficient_user = round(GAME_INFO['usersOfBlack']/GAME_INFO['usersOfWhite'], 1)
    #add timeFrame
    return f"{l}, {int(totalFixed/1000000)} | {int(coefficient_money/1000000)} , {coefficient_user} | "

def makeActions(GAME_INFO):
    # choices = ['0', '1']
    choices = ["follow","reverse"]
    values = [i for i in range(1,10,2)]
    actions = []
    for c in choices:
        for v in values:
            actions.append(f"{c}_{v}")
    return actions