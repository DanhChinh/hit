from collections import defaultdict
import requests
import json
import numpy as np
def get_data_from_webdb():
    url = 'https://thuhuyen.fun/xg79/get_data.php'
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Gây lỗi nếu mã HTTP != 200

        data = response.json()
        return data.get("data", None)

    except requests.exceptions.RequestException as e:
        print("Lỗi kết nối:", e)
        return None



import pandas as pd

# Đọc file CSV
df = pd.read_csv("data.csv")

def handle_progress(progress, isEnd = True):
    progress_arr = json.loads(progress)
    if isEnd and len(progress_arr) != 49:
        return None
    sublist = progress_arr[37:40]

    sum_bc = defaultdict(int)
    sum_v = defaultdict(int)
    count = defaultdict(int)

    for pair in sublist:
        for item in pair:
            eid = item["eid"]
            sum_bc[eid] += item["bc"]
            sum_v[eid] += item["v"]
            count[eid] += 1

    return int(sum_bc[1] / 3)-int(sum_bc[2] / 3), int(sum_v[1] / 3000000)-int(sum_v[2] / 3000000)




data_perfect = []
label_perfect = []
for index, row in df.iterrows():
    formater = handle_progress(row['progress'])
    if formater:
        data_perfect.append(formater)
        rs18 = row['d1']+row['d2']+row['d3']
        label_perfect.append(1 if rs18>10 else 0)


data = np.array(data_perfect)
label = np.array(label_perfect)


data_seq = 3
from sklearn.preprocessing import RobustScaler

scaler = RobustScaler()
data_scaled = scaler.fit_transform(data)

data_rounded = np.round(data_scaled, 1)


def filter_data(X_test=(329, -105)):
    X_test = scaler.transform([X_test])
    X_test = np.round(X_test, 1)
    X_test_0 = X_test[0]
    ft_dt = []
    ft_lb = []
    for i in range(len(data_rounded)):
        if X_test_0[0] == data_rounded[i][0] or X_test_0[1] == data_rounded[i][1]:
            ft_dt.append(data_rounded[i])
            ft_lb.append(label[i])
    return np.array(ft_dt), np.array(ft_lb), X_test


from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier



clfs = [
    MLPClassifier(hidden_layer_sizes=(100, 100, 100), alpha=1e-6, max_iter=1000, random_state=42),
    GradientBoostingClassifier(n_estimators=1000, learning_rate=0.01, max_depth=5, random_state=42),
    RandomForestClassifier(n_estimators=500, max_depth=None, min_samples_split=2, min_samples_leaf=1, random_state=42),
    LogisticRegression(C=1e10, penalty='l2', solver='liblinear'),
    SVC(kernel='rbf', C=1000),
    KNeighborsClassifier(n_neighbors=1),
    DecisionTreeClassifier(max_depth=None, min_samples_split=2, min_samples_leaf=1, random_state=42)
]



def my_predict(X_test):
    print(X_test)
    ft_dt, ft_lb, X_test = filter_data(X_test)
    count_0 = 0
    count_1 = 0
    for clf in clfs:
        clf.fit(ft_dt, ft_lb)
        y_pred = int(clf.predict(X_test)[0])
        if y_pred == 1:
            count_1+=1
        else:
            count_0 +=1
    print(count_1, count_0)
    if count_1> count_0:
        return 1, count_1-count_0
    return 2, count_0-count_1

