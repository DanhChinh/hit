
from db import readTable
import pandas as pd
import numpy as np
import os, joblib

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()


from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.naive_bayes import GaussianNB




def makeDataset():
    df = readTable()
    label = df['rs18'].shift(-1)>10
    label = label.drop(df.index[-1])
    df = df.drop(df.index[-1])
    df.drop(columns=['id', 'sid'], inplace=True)
    columns_to_sort = ['xx1', 'xx2', 'xx3']
    df[columns_to_sort] = np.sort(df[columns_to_sort].values, axis=1)
    df = df.to_numpy()
    df = scaler.fit_transform(df).round(3)

    return df, label.to_numpy()



def getAccuracyScoreMax(model, X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy


#randomforest
#Naive Bayes

model_list = [RandomForestClassifier(),  GaussianNB(), XGBClassifier()]


def train():
    X, y = makeDataset()
    for i in range(9):
        filePath = f"./models/model_{i}.joblib"
        maxModel = None
        maxAccuracy = 0
        if os.path.exists(filePath):
            maxModel,maxAccuracy = joblib.load(filePath)
        model = model_list[i%3]
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