print("khoi tao du lieu...")
from db import readTable, df_get_hsft
from sklearn.preprocessing import MinMaxScaler
import numpy as np
scaler = MinMaxScaler()
def flatten_transform_df(df):
    df.drop(columns=['id', 'sid'], inplace=True)
    df = scaler.transform(df).round(3)
    return df.flatten()
def label_df(df):
    r = df.iloc[0]
    # m = r['mB']>r['mW']
    # u = r['uB']>r['uW']
    # rs = r['rs18']>10
    # return f"{m}_{u}_{rs}"
    if r['rs18']>10:
        return 1
    return 0
def split_random_data(array_2d_1, array_2d_2, array_1d):
    n_samples = array_2d_1.shape[0]

    # Tạo tập chỉ số ngẫu nhiên
    random_indices = np.random.choice(n_samples, size=int(0.8 * n_samples), replace=False)

    # Tách dữ liệu thành hai phần
    # Phần 1: 70% dữ liệu ngẫu nhiên
    array_2d_1_part1 = array_2d_1[random_indices]
    array_2d_2_part1 = array_2d_2[random_indices]
    array_1d_part1 = array_1d[random_indices]

    # Phần 2: 30% dữ liệu còn lại
    array_2d_1_part2 = np.delete(array_2d_1, random_indices, axis=0)
    array_2d_2_part2 = np.delete(array_2d_2, random_indices, axis=0)
    array_1d_part2 = np.delete(array_1d, random_indices)

    return array_2d_1_part1, array_2d_1_part2, array_2d_2_part1, array_2d_2_part2, array_1d_part1, array_1d_part2

# =
df =  readTable()

df_scaler = df.drop(columns=['id', 'sid'], inplace=False)
scaler.fit_transform(df_scaler).round(3)


def makeSave():
    data = []
    next_data = []
    label = []
    for sid in df['sid']:
        state, nextstate, reward = df_get_hsft(sid)
        if len(state)!=6 or len(nextstate)!=6 or len(reward)!=1:
            continue 
        data.append(flatten_transform_df(state))
        next_data.append(flatten_transform_df(nextstate))
        label.append(label_df(reward))
    data = np.array(data)
    next_data = np.array(next_data)
    label = np.array(label)
    np.savez('data_transform3.npz', data=data, next_data=next_data, label=label)
    print("luu du lieu moi hoan tat")
def loadTransform3():
    loaded_data = np.load('data_transform3.npz')
    print("tai len du lieu cu hoan tat")
    return loaded_data['data'], loaded_data['next_data'], loaded_data['label']
# makeSave()
data, next_data, label = loadTransform3()