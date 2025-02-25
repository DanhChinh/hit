import numpy as np
import pandas as pd
import os, time
from db import readTable, df_get_hsft
from models import *
from dataTransform import *





def make_action():
    choice = [1, 0]
    values = [1,3,5,7,9]
    actions = []
    for c in choice:
        for v in values:
            actions.append(f"{c}_{v}")
    return  actions


class QLearningAgent:
    def __init__(self, qtable_file="q_table.csv", alpha=0.1, gamma=0.9, epsilon=0.1):
        self.qtable_file = qtable_file  # Tên file để lưu Q-table
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.actions = make_action()

        # 🔹 Nếu file Q-table tồn tại -> Tải dữ liệu từ file
        if os.path.exists(self.qtable_file):
            # self.load_q_table()
            self.q_table = pd.read_csv(qtable_file, index_col=0)
        else:
            self.q_table = pd.DataFrame(0, index=[], columns=self.actions)

            print("🔹 Không tìm thấy file Q-table, tạo bảng mới.")

    def choose_action(self, state):
        if state not in self.q_table.index:
            self.q_table.loc[state] = np.zeros(len(self.actions))  # Thêm state mới
            return np.random.choice(self.actions)  # Chọn action ngẫu nhiên
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.actions)  # Khám phá
        return self.q_table.loc[state].idxmax()  # Khai thác

    def update_q_table(self, state, action, reward, next_state):
        if next_state not in self.q_table.index:
            self.q_table.loc[next_state] = np.zeros(len(self.actions))
        old_value = self.q_table.loc[state, action]
        max_future_value = self.q_table.loc[next_state].max()
        new_value = old_value + self.alpha * (reward + self.gamma * max_future_value - old_value)
        self.q_table.loc[state, action] = new_value
        # return q_table
    def train(self, eps=1000):
        for _ in range(eps):
            print("esp:",_)
            dt7, dt3, _, ndt3, lb7, lb3 = split_random_data(data, next_data, label)
            model_fit(dt7, lb7)
            pb1s, pb2s, pb3s = model_makestate_all(dt3)
            npb1s, npb2s, npb3s = model_makestate_all(ndt3)
            for i in range(len(pb1s)):
                state = f"{pb1s[i]}_{pb2s[i]}_{pb3s[i]}"
                next_state = f"{npb1s[i]}_{npb2s[i]}_{npb3s[i]}"
                action = self.choose_action(state)
                [choice, values] = action.split("_")
                reward = int(values)
                if int(choice)!= lb3[i]:
                    reward *= -1
                self.update_q_table(state, action, reward, next_state)
            
        self.q_table.to_csv(self.qtable_file)
        print("✅ Huấn luyện hoàn tất!")
    def use(self, sid):
        start_time = time.time()
        hs6, _, _ = df_get_hsft(sid)
        if len(hs6)!=6:
            return "0_0"
        hs6 = flatten_transform_df(hs6)
        while True:
            dt7, dt3, _, ndt3, lb7, lb3 = split_random_data(data, next_data, label)
            model_fit(dt7, lb7)
            state = model_makestate(hs6)
            print(state)
            if state in self.q_table.index:
                # print(self.q_table.loc[state].idxmax())
                return self.q_table.loc[state].idxmax()
            if time.time()- start_time>30:
                print("over time")
                return "0_0"
    # def save_q_table(self):
    #     df = pd.DataFrame(self.Q_table)
    #     df.to_csv(self.qtable_file, index=False, header=False)
    #     print(f"✅ Q-table đã được lưu vào {self.qtable_file}")

    # def load_q_table(self):
    #     df = pd.read_csv(self.qtable_file, header=None)
    #     self.Q_table = df.values  
    #     print(f"✅ Q-table đã được tải từ {self.qtable_file}")

# =======================
# 🎯 Chạy chương trình
# =======================

agent = QLearningAgent()
# agent.train(500)
# agent.use(1844676)


# # 2️⃣ Huấn luyện bot nếu cần
# agent.train(num_episodes=5000)

# # 3️⃣ Lưu bảng Q-table sau khi huấn luyện
# agent.save_q_table()

# # 4️⃣ Kiểm tra bot sau khi học xong
# agent.test()
