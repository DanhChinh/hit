from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.ensemble import HistGradientBoostingClassifier
from db import readTable
import numpy as np
import time
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
from scipy.stats import linregress

modelDict = {
    "RandomForestClassifier":RandomForestClassifier,
    "XGBClassifier": XGBClassifier,
    "HistGradientBoostingClassifier": HistGradientBoostingClassifier
}

def get_correlation(data):
    """
    Tính hệ số tương quan r giữa chỉ số và dữ liệu.
    Nếu r > 0.5 → Xu hướng tăng.
    Nếu r < -0.5 → Xu hướng giảm.
    """
    if len(data) < 2:
        return 0  # Không đủ dữ liệu để tính toán

    x = np.arange(len(data))  # Chỉ số x: [0,1,2,...]
    slope, intercept, r_value, p_value, std_err = linregress(x, data)
    return r_value
def makeData():
    df = readTable()
    l = len(df)
    data = []
    label = []
    for i in range(30, l):
        dt = df["prf"].iloc[max(0, i-30):i].tolist()
        data.append(dt)
        row = df.iloc[i]
        im = row['mB']> row['mW']
        iu = row['uB']> row['uW']
        rs = row['rs18']>10
        label.append(f"{im}_{iu}_{rs}")
    xpredict = df["prf"].iloc[max(0, l-30):l].tolist()

    return scaler.fit_transform(data).round(3), le.fit_transform(label), scaler.transform([xpredict]).round(3)
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
def findBestModelList(data_train, data_test, label_train, label_test):
    label_test_decoder = le.inverse_transform(label_test)
    modelList = []
    for model_name in ["RandomForestClassifier", "XGBClassifier", "HistGradientBoostingClassifier"]:
        best_model = None
        max_correlation = -1
        for i in range(3):
            model = modelDict[model_name]()
            model.fit(data_train, label_train)
            predictions = model.predict(data_test)
            predictions_decoder =  le.inverse_transform(predictions)#.tolist()
            profit_list = []
            for i in range(len(label_test_decoder)):
                profit = compare_labels(predictions_decoder[i], label_test_decoder[i])
                profit_list.append(profit)
            profit_list_cummsum = np.cumsum(profit_list)
            correlation = get_correlation(profit_list_cummsum)
            if correlation> max_correlation:
                max_correlation = correlation
                best_model = model
        modelList.append(best_model)
    return modelList

def predict():
    st_time = time.time()
    data, label_encoder, xpredict = makeData() #label type 0,1,2,3
    data_train, data_test, label_train, label_test = split_data(data, label_encoder, 10)
    bestModelList = findBestModelList(data_train, data_test, label_train, label_test)
    predictions = []
    for model in bestModelList:
        prd = model.predict(xpredict)
        predictions.append(prd[0])
    predictions =  le.inverse_transform(predictions).tolist()
    print( time.time() - st_time)
    for i in range(len(predictions)):
        predictions[i] = predictions[i].split("_")
    # print(predictions)
    predictions = (np.array(predictions) == "True")
    # print(predictions)
    return predictions.tolist()

