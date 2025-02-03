# from sklearn.preprocessing import MinMaxScaler
import joblib
# from db import readTable
import sys
import numpy as np

def stop():
    sys.exit()
# scaler = MinMaxScaler()
# # Đọc mô hình đã lưu

scaler = joblib.load("scaler.pkl")


models = []
for i in range(10):
    filePath = f"./models/model_{i}.joblib"
    model, _ = joblib.load(filePath)
    model_name = type(model).__name__
    print(f"{filePath} {model_name} {_}")
    models.append(model) 

# df = readTable()
# df.drop(columns=['id', 'sid'], inplace=True)
# df = df.to_numpy()
# # print(df)
# scaler.fit(df)

# print(df)
# stop()


def predict(record):
    record = scaler.transform([record]).round(3)[0]
    print("record", record)
    
    record = np.array(record)
    record[3:6] = np.sort(record[3:6])

    # print("record", record)
    mB = 0
    mW = 0
    for model in models:
        prd = model.predict([record])[0]
        if prd :
            mB += 1
        else:
            mW += 1

    if mB > mW:
        return True, mB - mW
    return False, mW - mB




record = [430703065,  453526209,  1118,  1327,    6,    3,    4, 13, -43513109]
prd = predict(record)
print(prd)