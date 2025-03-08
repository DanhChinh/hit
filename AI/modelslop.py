from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn import tree
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.preprocessing import MinMaxScaler
from transform import loadTransform3, flatten_transform_df, label_df
from db import df_get_hsft
import numpy as np
scaler = MinMaxScaler()
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()

models = {
    "RandomForest": RandomForestClassifier,
    "XGBoost": XGBClassifier,
    "DecisionTree": tree.DecisionTreeClassifier,
    "HistGradientBoosting": HistGradientBoostingClassifier
}


data, label = loadTransform3()
data_transform = scaler.fit_transform(data).round(3)
label_encoder = le.fit_transform(label)

class MODEL:
    def __init__(self, model_name):
        self.model_name = model_name
        self.model = None
    def predict(self, data):
        return self.model.predict(data)
    def findBestModel(self, xtest):
        arr = []
        model = models[self.model_name]()
        for x in xtest:
            if model.predict([x]) == 1:
                return


models = [MODEL("RandomForest"), MODEL("XGBoost"), MODEL("DecisionTree"), MODEL("HistGradientBoosting")]
def makePredict(sid):
    sizeOfdt = 10
    xtest = []
    for i in range(sid-30, sid+1):
        x, _ = df_get_hsft(i, sizeOfdt)
        if len(x)== sizeOfdt+1:
            x = flatten_transform_df(x)
            x = scaler.transform([x]).round(3)
            xtest.append(x)
    if len(xtest)<5:
        return []
    xtest = np.array(xtest)
    xpredict = xtest[-1]
    xtest = xtest[:-1]

    predictions = []
    for model in models:
        model.findBestModel(xtest)
        predictions.append(model.predict([xpredict])[0])
    predictions =  le.inverse_transform(predictions).tolist()
    # print(predictions)
    for i in range(len(predictions)):
        predictions[i] = predictions[i].split("_")
    # print(predictions)
    predictions = (np.array(predictions) == "True")
    # print(predictions)
    return predictions.tolist()




    # predictions = []
    # for model in models:
    #     predictions.append(model.predict(ft)[0])
    # predictions =  le.inverse_transform(predictions).tolist()
    # return predictions

makePredict(1865362)