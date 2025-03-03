from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn import tree
from sklearn.ensemble import HistGradientBoostingClassifier

import numpy as np
from db import df_get_hsft
from transform import loadTransform3, flatten_transform_df, label_df 
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
from sklearn.preprocessing import LabelEncoder
# Khởi tạo LabelEncoder
le = LabelEncoder()

# Chuyển đổi y thành số nguyên


model1 = RandomForestClassifier()
model2 = XGBClassifier()
model3 = GaussianNB()
model5 = OneVsRestClassifier(estimator=SVC(gamma='scale'))
model6 = tree.DecisionTreeClassifier()
model7 = HistGradientBoostingClassifier(max_iter=100)

models = [model1, model2, model3, model5, model6, model7]


data, label = loadTransform3()
data_transform = scaler.fit_transform(data).round(3)
label_encoder = le.fit_transform(label)

for model in models:
    model.fit(data_transform, label_encoder)



def makePredict(sid):
    size = 10 
    hs, _ = df_get_hsft(sid, size)
    if len(hs)!= size+1:
        return []
    ft = flatten_transform_df(hs)
    ft = scaler.transform([ft]).round(3)
    predictions = []
    for model in models:
        predictions.append(model.predict(ft)[0])
    predictions =  le.inverse_transform(predictions).tolist()
    # print(predictions)
    for i in range(len(predictions)):
        predictions[i] = predictions[i].split("_")
    # print(predictions)
    predictions = (np.array(predictions) == "True")
    # print(predictions)
    return predictions.tolist()

# makePredict(1865362)