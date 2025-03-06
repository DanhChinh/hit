print("khoi tao du lieu...")
from db import readTable, df_get_hsft
from scipy.stats import linregress
import numpy as np
import pandas as pd

df =  readTable()

def get_slope(data):
    """
    Tính độ dốc trung bình của dữ liệu.
    Nếu độ dốc > 0 → Xu hướng tăng.
    Nếu độ dốc < 0 → Xu hướng giảm.
    """
    if len(data) < 2:
        return 0  # Không đủ dữ liệu để tính toán
    slope = (data[-1] - data[0]) / len(data)
    return slope
def get_correlation(data):
    """
    Tính hệ số tương quan r giữa chỉ số và dữ liệu.
    Nếu r > 0.5 → Xu hướng tăng.
    Nếu r < -0.5 → Xu hướng giảm.
    """
    if len(data) < 2:
        return 0  # Không đủ dữ liệu để tính toán

    x = np.arange(len(data))  # Chỉ số x: [0,1,2,...]
    slope, intercept, r_value, p_value, std_err = linregress(x, data)
    return r_value
def get_moving_average(data, window=3):
    """
    Tính trung bình động với kích thước cửa sổ `window`.
    Giá trị trả về là một danh sách đã làm mượt.
    """
    df = pd.DataFrame({"values": data})
    df["MA"] = df["values"].rolling(window=window, min_periods=1).mean()
    return df["MA"].values  # Trả về numpy array
def flatten_transform_df(df):
    df.drop(columns=['id', 'sid'], inplace=True)
    arr_prf = df['prf'].to_numpy()
    slope = get_slope(arr_prf)
    correlation = get_correlation(arr_prf)
    ma = get_moving_average(arr_prf)
    arr_trend = np.concatenate([ma,[slope],[correlation]])
    flatten = df.to_numpy().flatten()
    return  np.concatenate([flatten, arr_trend])
def label_df(df):
    row0 = df.iloc[0]
    return f"{row0['mB']>row0['mW']}_{row0['uB']>row0['uW']}_{row0['rs18']>10}"




def handle_data():
    data = []
    label = []
    size = 30
    for sid in df['sid']:
        state, reward = df_get_hsft(sid, size)
        if len(state)!= size+1 or len(reward)!=1:
            continue 
        data.append(flatten_transform_df(state))
        label.append(label_df(reward))
    np.savez('data_transform3.npz', data=np.array(data), label=np.array(label))
    print("luu du lieu moi hoan tat")
def loadTransform3():
    loaded_data = np.load('data_transform3.npz')
    print("tai len du lieu cu hoan tat")
    return loaded_data['data'], loaded_data['label']
# handle_data()


# data, label = loadTransform3()
# print(data)
# print(label)