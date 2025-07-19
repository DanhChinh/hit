import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
# from sklearn.linear_model import LogisticRegression
from env import make_data, handle_progress
from drawtable import draw_table
def isPass(data, label, x_pred):
    model = RandomForestClassifier()
    model.fit(data, label)
    probabilities = model.predict_proba(x_pred)[0]
    return round(probabilities[1], 2)
class Model:
    def __init__(self,data, label, model, model_name):
        self.model = model
        self.label_percent = 0
        self.model_name = model_name
        self.filter(data, label)
        self.hs = []
        self.sid = None
        self.predict = None
        self.percent = 0

    def filter(self, data, label):
        while self.label_percent<0.1:
            x_train, self.x_test, y_train, y_test = train_test_split(
                data, label, 
                train_size=0.19,
                test_size=0.019,
                shuffle=True,
                stratify=label)

            self.model.fit(x_train, y_train)
            y_pred = self.model.predict(self.x_test)
            self.mask = y_pred == y_test
            self.label_percent = round(sum(self.mask)/ len(self.mask), 2)
            print(f"Ti le nhan dung cua {self.model_name}:{self.label_percent}")

    def make_predict(self, x_pred):
        self.sid = sid
        self.probability = isPass(self.x_test, self.mask, x_pred)
        if self.probability >=0.6:
            self.predict =  self.make_predict(x_pred)[0]
        else:
            self.predict = None
        return self.predict
    def check(self, result):
        if self.sid is None:
            print(f"{self.model_name} is not sid")
            return
        if self.sid != sid:
            print(f"{self.model_name} != sid")
            return
        if self.predict is None:
            print(f"{self.model_name} is not predict")
            return
        if self.predict == result:
            self.hs.append(1)
        else:
            self.hs.append(0)
        self.percent = round(sum(self.hs)/len(self.hs) ,2)
    def to_dict(self):
        """
        Trả về các thuộc tính của đối tượng dưới dạng một từ điển.
        Tên các khóa trong từ điển được đặt theo yêu cầu của bạn.
        """
        return {
            "sid": self.sid,
            "name": self.model_name,
            "lb_perc": self.label_percent,
            "predict": self.predict,
            "percent": self.percent,
            "hs": self.hs
        }
    

scaler, data, label= make_data()
    # "KNN": Model(data, label, KNeighborsClassifier(n_neighbors=5), "KNN"),
    # "DecisionTree": Model(data, label, DecisionTreeClassifier(), "DecisionTree"),
classifiers = {
}
sid = None
for i in range(10):
    classifiers[f"RandomForest_{i}"] = Model(data, label, RandomForestClassifier(), f"RandomForest_{i}")
def showModels():
    for idx, (name, model) in enumerate(classifiers.items()):
        print(name, "id:", id(model))
def reloadModel(name):
    if name == "KNN": 
        classifiers['KNN'] = Model(data, label, KNeighborsClassifier(n_neighbors=5), "KNN")
    elif name == 'DecisionTree':
        classifiers["DecisionTree"] = Model(data, label, DecisionTreeClassifier(), "DecisionTree")
    else:
        classifiers["RandomForest"] = Model(data, label, RandomForestClassifier(), "RandomForest")
    # classifiers[name].filter(data, label)
def my_predict(progress):
    x_pred = handle_progress(progress, isEnd=False)
    x_pred = scaler.transform([x_pred])
    x_pred = np.round(x_pred, 1)
    c1 = 0
    c2 = 0
    for idx, (name, model) in enumerate(classifiers.items()):
        y_pred = model.make_predict(x_pred)
        print(f"{model.sid} {model.model_name:15} {model.probability:5} {model.percent:5} {'' if y_pred is None else y_pred}")
        if y_pred is None:
            continue
        y_pred = int(y_pred)
        if y_pred == 1:
            c1+=1
        else:
            c2+=1
    if c1>c2:
        return 1, c1-c2
    return 2, c2-c1
def check(result):
    for idx, (name, model) in enumerate(classifiers.items()):
        model.check(result)


table_data = []
for idx, (name, model) in enumerate(classifiers.items()):
    table_data.append(model.to_dict())
draw_table(table_data)