
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
    # label = df['rs18'].shift(-1)>10
    label = (df['rs18'].shift(-1) > 10).astype(int)
    label = label.drop(df.index[-1])
    df = df.drop(df.index[-1])
    df.drop(columns=['id', 'sid'], inplace=True)
    data = df.to_numpy()
    data = scaler.fit_transform(data).round(3)
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
        self.maxAccuracy = -1
        self.arrLen = 0
    def getBestDatatrain(self, x_test, y_test):
        self.maxAccuracy = -1
        l = len(data)-1000
        for i in range(0,l,50):
            x_train = data[i:i + 1000]
            y_train = label[i:i + 1000]
        # for i in range(5):
        #     x_train, y_train = getRandomX_train(data, label)
            self.model.fit(x_train, y_train)
            y_pred = self.model.predict(x_test)
            accuracy = accuracy_score(y_test, y_pred)
            if accuracy> self.maxAccuracy:
                self.maxAccuracy = accuracy
                self.bestModel = copy.deepcopy(self.model)
                # print(f"model: {self.id} -> accuracy: {self.maxAccuracy}")
    def predict(self, x):
        return int(self.bestModel.predict(x)[0])


def getBestDatatrain(x_test, y_test):
    for bot in botGroup:
        bot.getBestDatatrain(x_test, y_test)
def predict(x_prd):
    score_ar = [0,0]
    for bot in botGroup:
        prd = bot.predict(x_prd)
        print(f"bot:{bot.id} accuracy:{bot.maxAccuracy}, prd:{prd}")
        score_ar[prd] += bot.maxAccuracy
    if score_ar[1]> score_ar[0]:
        return 1, int((score_ar[1]/sum(score_ar))*100)-50
    return 2, int((score_ar[0]/sum(score_ar))*100)-50
    return score
def last30(arr, number = 30):
    if len(arr) > number:
        return arr[-number:]
    return arr
class XY_TEST:
    def __init__(self):
        self.x = []
        self.y = []
    def addData(self, record):
        self.x.append(record)
        self.y.append(int(record[-2]>10))
    def makeXYtest(self):
        x_scaler = scaler.transform(self.x).round(3)
        x_prd = np.array(x_scaler)[-1:]
        x_test = np.array(x_scaler)[:-1]
        y_test = np.array(self.y)[1:]
        return last30(x_test), last30(y_test), x_prd
        


############################
data, label = makeDataset()
print(data)
print(label)

bot1 = BOT(1, RandomForestClassifier())
bot2 = BOT(2, RandomForestClassifier())
bot3 = BOT(3, RandomForestClassifier())
bot4 = BOT(4, GaussianNB())
bot5 = BOT(5, GaussianNB())
bot6 = BOT(6, GaussianNB())
bot7 = BOT(7, XGBClassifier())
bot8 = BOT(8, XGBClassifier())
bot9 = BOT(9, XGBClassifier())
# botGroup = [bot1, bot2, bot3, bot4, bot5, bot6, bot7, bot8, bot9]
botGroup = [bot1, bot5, bot9]


xy_test = XY_TEST()
