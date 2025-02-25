from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.naive_bayes import GaussianNB
import numpy as np

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

def model_fit(data, label):
    for model in models:
        model.fit(data, label)

def model_makestate(data):
    pb1 =  np.round(model1.predict_proba([data])[0], 1)
    pb2 =  np.round(model2.predict_proba([data])[0], 1)
    pb3 =  np.round(model3.predict_proba([data])[0], 1)
    return f"{pb1}_{pb2}_{pb3}"
def model_makestate_all(data):
    pb1s = np.round(model1.predict_proba(data), 1)
    pb2s = np.round(model2.predict_proba(data), 1)
    pb3s = np.round(model3.predict_proba(data), 1)
    return pb1s, pb2s, pb3s