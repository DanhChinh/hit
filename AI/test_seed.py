# from models import makePredict
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(random_state=1)
from db import df_get_hsft
from transform import loadTransform3, flatten_transform_df, label_df 
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
# Khởi tạo LabelEncoder
le = LabelEncoder()
scaler = MinMaxScaler()
data, label = loadTransform3()
data_transform = scaler.fit_transform(data).round(3)
label_encoder = le.fit_transform(label)
model.fit(data_transform, label_encoder)

sid = 1869907
size = 380
db, _ = df_get_hsft(sid, size)

profitlist = []

xtest = []
for index, row in db.iterrows():
    sid = row['sid']
    hs, _ = df_get_hsft(sid, 10)
    if len(hs) != 11:
        continue
    ft = flatten_transform_df(hs)
    ft = scaler.transform([ft]).round(3)
    print(ft)
    break

#     xtest.append(ft)
# prds = model.predict(xtest)
# print(prds)