import joblib
import numpy as np

scaler = joblib.load("scaler.pkl")
models = []
for i in range(9):
    filePath = f"./models/model_{i}.joblib"
    model, _ = joblib.load(filePath)
    model_name = type(model).__name__
    print(f"{filePath} {model_name} {_}")
    models.append(model) 


def predict(record):
    record = scaler.transform([record]).round(3)[0]
    print("record", record)
    
    record = np.array(record)
    record[3:6] = np.sort(record[3:6])

    F = 0
    T = 0
    for model in models:
        prd = model.predict_proba([record])[0]
        if prd[0]>0.65:
            F+=1
        elif prd[0]<0.35:
            T+=1
        else:
            pass
    if T>F:
        return True, T-F 
    return False, F-T

record = [430703065,  453526209,  1118,  1327,    6,    3,    4, 13, -43513109]
prd = predict(record)
print(prd)