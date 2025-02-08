
from db import readTable
import pandas as pd
import numpy as np
import os, joblib
import copy

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
    data = df.to_numpy()
    data = scaler.fit_transform(df).round(3)
    return data, label.to_numpy()

def workWithHistory(history):
    df = pd.DataFrame(history, columns=['mB', 'mW', 'uB', 'uW', 'xx1', 'xx2', 'xx3', 'rs18', 'prf'])
    label = df['rs18'].shift(-1)>10
    label = label.drop(df.index[-1])
    df = df.drop(df.index[-1])

def getRandomX_train(data, label):
    start_index = np.random.randint(0, len(data) - 1000)
    return data[start_index:start_index + 1000], label[start_index:start_index + 1000]



class BOT:
    def __init__(self, id, model):
        self.id = id
        self.model = model
        self.bestModel = None
        self.maxAccuracy = 0
    def getBestDatatrain(self, x_test, y_test):
        x_train, y_train = getRandomX_train(data, label)
        self.model.fit(x_train, y_train)
        y_pred = self.model.predict(x_test)
        accuracy = accuracy_score(y_test, y_pred)
        if accuracy> self.maxAccuracy:
            self.maxAccuracy = accuracy
            self.bestModel = copy.deepcopy(self.model)
            print(self.id, self.maxAccuracy)
    def predict(self, x):
        return self.bestModel.predict([x])[0]



bot1 = BOT(1, RandomForestClassifier())
bot2 = BOT(2, RandomForestClassifier())
bot3 = BOT(3, RandomForestClassifier())
bot4 = BOT(4, GaussianNB())
bot5 = BOT(5, GaussianNB())
bot6 = BOT(6, GaussianNB())
bot7 = BOT(7, XGBClassifier())
bot8 = BOT(8, XGBClassifier())
bot9 = BOT(9, XGBClassifier())
botGroup = [bot1, bot2, bot3, bot4, bot5, bot6, bot7, bot8, bot9]
data, label = makeDataset()



def getBestDatatrain(x_test, y_test):
    for bot in botGroup:
        bot.getBestDatatrain(x_test, y_test)
def predict(record):
    record = scaler.transform([record]).round(3)[0]
    print("record", record)
    record = np.array(record)
    record[3:6] = np.sort(record[3:6])
    for bot in botGroup:
        bot.predict(record)


class XY_TEST:
    def __init__(self):
        self.x = []
        self.y = []
    def addData(self, record):
        self.x.append(record)
        self.y.append(record[-2]>10)
    def makeXYtest(self):
        x_test
        #cat phan tu dau tien cua y_test
        #cat phan tu cuoi cung cua x_test
        


        


xy_test = XY_TEST()