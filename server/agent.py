import pandas as pd
import numpy as np
import os
import random
import matplotlib.pyplot as plt
def plot_cumulative(arr, title='Biểu đồ cộng dồn'):
    """
    Vẽ biểu đồ cộng dồn của một mảng số.

    Parameters:
        arr (list hoặc np.array): Dữ liệu đầu vào.
        title (str): Tiêu đề biểu đồ.
    """
    arr = np.array(arr)
    cum_sum = np.cumsum(arr)

    plt.figure(figsize=(8, 4))
    plt.plot(cum_sum, marker='o')
    plt.title(title)
    plt.xlabel('Chỉ số')
    plt.ylabel('Tổng cộng dồn')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def get_reward(action, result):
    [predict, point] = action.split('_')
    predict = int(predict)
    point = int(point)
    result = int(result)
    if predict == result:
        return point
    return -point
class QLearning:
    def __init__(self, actions, qtable_path='qtable.csv', alpha=0.1, gamma=0.9, epsilon=0.1):
        self.actions = actions  # danh sách hành động (ví dụ: ['left', 'right', 'up', 'down'])
        self.qtable_path = qtable_path
        self.alpha = alpha      # learning rate
        self.gamma = gamma      # discount factor
        self.epsilon = epsilon  # exploration rate

        self.q_table = self._load_qtable()

    def _load_qtable(self):
        if os.path.exists(self.qtable_path):
            return pd.read_csv(self.qtable_path, index_col=0)
        else:
            return pd.DataFrame(columns=self.actions)

    def _save_qtable(self):
        self.q_table.to_csv(self.qtable_path)

    def _ensure_state_exists(self, state):
        state_str = str(state)
        if state_str not in self.q_table.index:
            self.q_table.loc[state_str] = [1.0] * len(self.actions)

    def choose_action(self, state, play=False):
        self._ensure_state_exists(state)
        if np.random.rand() < self.epsilon and not play:
            return random.choice(self.actions)  # explore
        else:
            state_actions = self.q_table.loc[str(state)]
            return state_actions.idxmax()  # exploit

    def update(self, state, action, reward, play=False):
        alpha = self.alpha
        if play:
            alpha = 0.7
        self._ensure_state_exists(state)
        q_predict = self.q_table.loc[state, action]
        q_target = reward + self.gamma
        self.q_table.loc[state, action] += alpha * (q_target - q_predict)

    def train(self, data, label):
        """
        Huấn luyện agent trong môi trường `env` (phải có: reset(), step(action)).
        """
        l = len(data)
        for i in range(l):
            state = f"{data[i]}"
            action = self.choose_action(state)
            reward = get_reward(action, label[i])
            # next_state, reward, done = env.step(action)
            self.update(state, action, reward)
        self._save_qtable()

    def play(self, data, label):
        """
        Chơi và cập nhật Q-table trong khi tương tác với môi trường.
        """
        rewards = []
        l = len(data)
        for i in range(l):
            state = f"{data[i]}"
            action = self.choose_action(state, True)
            reward = get_reward(action, label[i])
            rewards.append(reward)
            # next_state, reward, done = env.step(action)
            self.update(state, action, reward)
        # self._save_qtable()
        plot_cumulative(rewards)


