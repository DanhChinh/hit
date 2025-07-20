import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from env import make_data, handle_progress
import json

def isPass(data, label, x_pred):
    model = RandomForestClassifier()
    model.fit(data, label)
    probabilities = model.predict_proba(x_pred)[0]
    return round(probabilities[1], 2)

class Model:
    def __init__(self, data, label, model, model_name):
        self.model = model
        self.model_name = model_name
        self.label_percent = 0
        self.filter(data, label)
        self.sid = 1
        self.predict = None
        self.probability = 0
        self.percent = 0
        self.hs = []
        self.score = 0
    def filter(self, data, label):
        while self.label_percent < 0.55:
            x_train, self.x_test, y_train, y_test = train_test_split(
                data, label,
                train_size=0.19,
                test_size=0.019,
                shuffle=True,
                stratify=label
            )
            self.model.fit(x_train, y_train)
            y_pred = self.model.predict(self.x_test)
            self.mask = y_pred == y_test
            self.label_percent = round(sum(self.mask) / len(self.mask), 2)
            print(f"Tỉ lệ nhận đúng của {self.model_name}: {self.label_percent}")

    def make_predict(self, sid, x_pred):
        self.sid = sid
        self.probability = isPass(self.x_test, self.mask, x_pred)
        if self.probability >= 0.6:
            self.predict = self.model.predict(x_pred)[0]
            percent = min(10, len(self.hs))/10 *self.percent
            self.score = int((self.probability * max(percent, 0.1))*100)
        else:
            self.predict = None
            self.score = 0
        return self.predict

    def check(self, result, sid):
        if self.sid is None or self.sid != sid:
            self.sid = "error"
            return
        if self.predict is None:
            self.sid = " "
            return
        self.hs.append(1 if self.predict == result else 0)
        self.percent = round(sum(self.hs) / len(self.hs), 2)
        self.sid = "done"

    def to_dict(self):
        return {
            "sid": self.sid,
            "name": f"{self.model_name} {self.label_percent}",
            "probability": float(self.probability),
            "predict": str(self.predict),
            "percent": float(self.percent),
            'score':int(self.score),
            "hs": len(self.hs)
        }


# Chuẩn bị dữ liệu
scaler, data, label = make_data()

# Tạo các mô hình
classifiers = {}
for i in range(10):
    classifiers[f"RandomForest_{i}"] = Model(data, label, RandomForestClassifier(), f"RF_{i}")




def my_predict(sid, progress):
    x_pred = handle_progress(progress, isEnd=False)
    x_pred = scaler.transform([x_pred])
    x_pred = np.round(x_pred, 1)

    c1 = 0
    c2 = 0
    table = []
    for idx, (name, model) in enumerate(classifiers.items()):
        y_pred = model.make_predict(sid, x_pred)
        table.append(model.to_dict())
        print(f"{model.sid} {model.model_name:15} {model.probability:.2f} {model.percent:.2f} {'' if y_pred is None else y_pred}")
        if y_pred is None:
            continue
        y_pred = int(y_pred)
        if y_pred == 1:
            c1 += model.score 
        else:
            c2 += model.score
    return (1, c1 - c2, table) if c1 > c2 else (2, c2 - c1, table)

def check(sid, result):
    table = []
    for name, model in classifiers.items():
        model.check(result, sid)
        table.append(model.to_dict())
    return table
