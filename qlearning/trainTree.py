
from db import readTable
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
scaler = MinMaxScaler()
import sys , os, random
import joblib
import numpy as np
def stop():
    sys.exit()


def makeDataset():
    df = readTable()
    label = df['rs18'].shift(-1)>10
    label = label.drop(df.index[-1])
    df = df.drop(df.index[-1])
    df.drop(columns=['id', 'sid'], inplace=True)
    columns_to_sort = ['xx1', 'xx2', 'xx3']
    df[columns_to_sort] = np.sort(df[columns_to_sort].values, axis=1)
    df = df.to_numpy()
    df = scaler.fit_transform(df).round(2)


    # df = pd.DataFrame(scaler.fit_transform(df).round(2), columns=df.columns)
    # print(df)
    # joblib.dump(scaler, "scaler.pkl")
    return df, label.to_numpy()



import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from xgboost import XGBClassifier

from sklearn.naive_bayes import GaussianNB

def getAccuracyScoreMax(model, X, y):
    # Chia tập dữ liệu (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    model.fit(X_train, y_train)
    # Dự đoán trên tập test
    y_pred = model.predict(X_test)

    # Đánh giá độ chính xác
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy


# Tạo mô hình cây quyết định
# clf = DecisionTreeClassifier()#max_depth=5, random_state=42)
# X, y = makeDataset()

# maxAccuracy = 0
# bestRandomStateXY = 0

# for random_state_XY in range(100):
#     accuracy = getAccuracyScoreMax(X, y, random_state_XY)
#     if accuracy > maxAccuracy:
#         maxAccuracy = accuracy
#         bestRandomStateXY = random_state_XY

# print(f"Mô hình tốt nhất với đ�� chính xác: {maxAccuracy:.2f} với random_state={bestRandomStateXY}")
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=bestRandomStateXY)
# clf.fit(X_train, y_train)







def train():
    X, y = makeDataset()
    for i in range(10):
        filePath = f"./models/model_{i}.joblib"
        # print(filePath)
        maxModel = None
        maxAccuracy = 0
        if os.path.exists(filePath):
            maxModel,maxAccuracy = joblib.load(filePath)
        model = random.choice([DecisionTreeClassifier(), XGBClassifier(), GaussianNB()])
        accuracy = getAccuracyScoreMax(model, X, y)
        if accuracy > maxAccuracy:
            maxAccuracy = accuracy
            maxModel = model
            joblib.dump((maxModel, maxAccuracy), filePath)
            print(f"Mô hình thứ {i} đã được lưu và đánh giá đ�� chính xác: {maxAccuracy:.2f}")

for i in range(1000):
    print(">", end="")
    if i % 100 == 0:
        print()
    train()
joblib.dump(scaler, "scaler.pkl")