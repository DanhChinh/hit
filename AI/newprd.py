from db import readTable
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()

def makeData():
    df = readTable()
    l = len(df)
    data = []
    label = []
    for i in range(10, l):
        dt = df["prf"].iloc[max(0, i-10):i].tolist()
        data.append(dt)
        row = df.iloc[i]
        im = row['mB']> row['mW']
        iu = row['uB']> row['uW']
        rs = row['rs18']>10
        label.append(f"{im}_{iu}_{rs}")
    xpredict = df["prf"].iloc[max(0, l-10):l].tolist()

    return scaler.fit_transform(data).round(3), le.fit_transform(label),scaler.transform([xpredict]).round(3)
def split_data(data, label, size=10):
    index = len(data)- size
    return data[:index], data[index:], label[:index], label[index:]

def compare_labels(label1, label2):
    arr1 = label1.split('_')
    arr2 = label2.split('_')
    if arr1[0] == arr2[0] and arr1[1] == arr2[1]:
        if arr1[2] == arr2[2]:
            return 1
        return -1
    return 0
def findBestModel(data_train, data_test, label_train, label_test):
    label_test = le.inverse_transform(label_test)
    bestModel = None
    bestScore = -1
    for i in range(10):
        model = RandomForestClassifier()
        model.fit(data_train, label_train)
        predictions = model.predict(data_test)
        predictions =  le.inverse_transform(predictions)#.tolist()
        slopes = []
        for i in range(len(label_test)):
            slope = compare_labels(predictions[i], label_test[i])
            slopes.append(slope)
        print(slopes)
        return 1

def predict():
    data, label, xpredict = makeData()
    data_train, data_test, label_train, label_test = split_data(data, label, 10)
    bestModel = findBestModel(data_train, data_test, label_train, label_test)

predict()

