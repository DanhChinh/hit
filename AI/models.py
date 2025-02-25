from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.svm import SVC
from lightgbm import LGBMClassifier

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


model3 = SVC(
    kernel='rbf',   # Hàm kernel để xử lý dữ liệu phi tuyến tính
    C=1,            # Điều chỉnh độ phức tạp (C lớn hơn có thể overfit)
    gamma='scale'   # Điều chỉnh mức ảnh hưởng của điểm dữ liệu
)


model4 = LGBMClassifier(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=7,
    num_leaves=31,
    subsample=0.8,
    colsample_bytree=0.8
)

models = [model1, model2, model3, model4]

def fit(data, label):
    for model in models:
        model.fit(data, label)

def predict(data):
    predictions = []
    for model in models:
        predictions.append(model.predict_proba(data))
    return predictions
