from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.naive_bayes import GaussianNB
import numpy as np
from db import df_get_hsft
from transform import loadTransform3, flatten_transform_df, label_df 
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
from sklearn.preprocessing import LabelEncoder
# Khởi tạo LabelEncoder
le = LabelEncoder()

# Chuyển đổi y thành số nguyên


model1 = RandomForestClassifier(
    n_estimators=200,      # Số lượng cây (tăng lên để có mô hình ổn định)
    max_depth=None,        # Không giới hạn độ sâu (hoặc thử max_depth=10-30)
    min_samples_split=10,  # Giảm overfitting bằng cách tăng số mẫu tối thiểu để chia nhánh
    min_samples_leaf=4,    # Giảm overfitting bằng cách đặt số mẫu tối thiểu ở lá
    bootstrap=True,        # Sử dụng bootstrap sampling để tăng tính tổng quát
    random_state=42
)

model2 = XGBClassifier(
    n_estimators=300,    # Số lượng cây (nhiều hơn để tổng quát tốt)
    max_depth=6,         # Giới hạn độ sâu của cây để tránh overfitting
    learning_rate=0.05,  # Giảm tốc độ học để tổng quát hóa tốt hơn
    subsample=0.8,       # Chỉ lấy 80% dữ liệu mỗi lần để tránh overfitting
    colsample_bytree=0.8 # Chỉ lấy 80% đặc trưng mỗi lần để tránh overfitting
)

model3 = GaussianNB()

models = [model1, model2, model3]


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
    predictions =  le.inverse_transform(predictions)
    for i in range(len(predictions)):
        predictions[i] = predictions[i].split("_")
    return predictions

