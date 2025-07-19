import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
# from sklearn.linear_model import LogisticRegression
from env import make_data, handle_progress
def isPass(data, label, x_pred):
    model = RandomForestClassifier()
    model.fit(data, label)
    probabilities = model.predict_proba(x_pred)[0]

    # print("Thứ tự các lớp của mô hình:", model.classes_)
    # print("Xác suất dự đoán cho mẫu mới:", probabilities)
    if probabilities[1]> 0.6:
        print(probabilities, "-> pass")
        return True
    print(probabilities, "-> fall")
    return False
class Model:
    def __init__(self,data, label, model, ModelName):
        self.model = model
        self.ModelName = ModelName
        self.filter(data, label)

    def filter(self, data, label):
        x_train, self.x_test, y_train, y_test = train_test_split(
            data, label, 
            train_size=0.19,
            test_size=0.019,
            shuffle=True,
            stratify=label)

        self.model.fit(x_train, y_train)
        y_pred = self.model.predict(self.x_test)
        self.mask = y_pred == y_test
        self.percent = sum(self.mask)/ len(self.mask)
        print(f"Ti le nhan dung cua {self.ModelName}:{self.percent}")

    def predict(self, x_pred):
        if isPass(self.x_test, self.mask, x_pred):
            return self.model.predict(x_pred)[0]
        return None

scaler, data, label= make_data()
classifiers = {
    "KNN": Model(data, label, KNeighborsClassifier(n_neighbors=5), "KNN"),
    "DecisionTree": Model(data, label, DecisionTreeClassifier(), "DecisionTree"),
    "RandomForest": Model(data, label, RandomForestClassifier(), "RandomForest")
}
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
def my_predict(msg):
    x_pred = handle_progress(msg, isEnd=False)
    x_pred = scaler.transform([x_pred])
    x_pred = np.round(x_pred, 1)
    c1 = 0
    c2 = 0
    for idx, (name, model) in enumerate(classifiers.items()):
        y_pred = model.predict(x_pred)
        if y_pred is None:
            continue
        y_pred = int(y_pred)
        print(name, y_pred)
        if y_pred == 1:
            c1+=1
        else:
            c2+=1
    if c1>c2:
        return 1, c1-c2
    return 2, c2-c1