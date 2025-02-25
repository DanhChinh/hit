import numpy as np
import pandas as pd
import os
from db import readTable, df_get_hsft
from models import *
from dataTransform import *



# data, label = make_data()


# X_train, X_test, y_train, y_test = train_test_split(data, label, test_size=0.2, random_state=42)
# model_1.fit(X_train, y_train)
# prd = model_1.predict_proba([X_test[0]])[0]
# print(f"Model 1 predict: {prd}")




class QLearningAgent:
    def __init__(self, qtable_file="q_table.csv", learning_rate=0.8, discount_factor=0.95, exploration_rate=1.0, exploration_decay=0.995):
        self.qtable_file = qtable_file  # Tên file để lưu Q-table
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay

        # 🔹 Nếu file Q-table tồn tại -> Tải dữ liệu từ file
        if os.path.exists(self.qtable_file):
            self.load_q_table()
        else:
            self.Q_table = np.zeros((0, 20))  # Khởi tạo mặc định
            print("🔹 Không tìm thấy file Q-table, tạo bảng mới.")

    def choose_action(self, state):
        if np.random.rand() < self.exploration_rate:
            return self.env.action_space.sample()
        else:
            return np.argmax(self.Q_table[state, :])  

    def update_q_table(self, state, action, reward, new_state):
        best_next_action = np.max(self.Q_table[new_state, :])
        self.Q_table[state, action] = self.Q_table[state, action] + self.learning_rate * (
            reward + self.discount_factor * best_next_action - self.Q_table[state, action]
        )

    def train(self):
        dt7, dt3, ndt7, ndt3, lb7, lb3 = split_random_data()
        model_fit(dt7, lb7)
        for i in range(len(dt3)):
            state = model_makestate(dt3[i])
            nextstate = model_makestate(ndt3[i])
            action = self.choose_action(state)
            reward 






        print(array_part3)
                    # for i in range(l):
        #     x = X_test[i]


        #     while not done:
        #         action = self.choose_action(state)  
        #         new_state, reward, done, _, _ = self.env.step(action)  

        #         self.update_q_table(state, action, reward, new_state)  
        #         state = new_state

        #     self.exploration_rate *= self.exploration_decay

        print("✅ Huấn luyện hoàn tất!")

    def test(self, max_steps=10):
        state = self.env.reset()[0]
        self.env.render()

        for _ in range(max_steps):
            action = np.argmax(self.Q_table[state, :])  
            new_state, reward, done, _, _ = self.env.step(action)
            self.env.render()
            state = new_state
            if done:
                break

    def save_q_table(self):
        df = pd.DataFrame(self.Q_table)
        df.to_csv(self.qtable_file, index=False, header=False)
        print(f"✅ Q-table đã được lưu vào {self.qtable_file}")

    def load_q_table(self):
        df = pd.read_csv(self.qtable_file, header=None)
        self.Q_table = df.values  
        print(f"✅ Q-table đã được tải từ {self.qtable_file}")

# =======================
# 🎯 Chạy chương trình
# =======================

# 1️⃣ Khởi tạo bot (tự động kiểm tra file Q-table)
agent = QLearningAgent()
agent.train(100)

# # 2️⃣ Huấn luyện bot nếu cần
# agent.train(num_episodes=5000)

# # 3️⃣ Lưu bảng Q-table sau khi huấn luyện
# agent.save_q_table()

# # 4️⃣ Kiểm tra bot sau khi học xong
# agent.test()
