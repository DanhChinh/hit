import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.decomposition import PCA

from env import filtered, is_pass_filtered

# ---------------- Hàm vẽ kết quả phân loại ----------------
def plot_per_classifier(X_train, X_test, y_train, y_test, classifiers):
    if X_train.shape[1] > 2:
        X_all = np.vstack((X_train, X_test))
        X_all_2d = PCA(n_components=2).fit_transform(X_all)
        X_test_2d = X_all_2d[len(X_train):]
        print("🔷 Dữ liệu > 2 chiều → dùng PCA để trực quan.")
    else:
        X_test_2d = X_test
        print("🔷 Dữ liệu đã là 2 chiều → không dùng PCA.")

    num_models = len(classifiers)
    fig, axes = plt.subplots(num_models, 2, figsize=(14, 5 * num_models))
    if num_models == 1:
        axes = np.expand_dims(axes, axis=0)

    for idx, (name, model) in enumerate(classifiers.items()):
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred) * 100
        print(f"✅ {name} - Accuracy: {acc:.2f}%")

        # Vẽ scatter
        ax_s = axes[idx, 0]
        ax_s.scatter(X_test_2d[:, 0], X_test_2d[:, 1], c=y_pred, cmap='tab10', s=20)
        ax_s.set_title(f'{name} - Dự đoán (Acc: {acc:.2f}%)')
        ax_s.set_xlabel('Dim 1')
        ax_s.set_ylabel('Dim 2')
        ax_s.grid(True)

        # Vẽ cộng dồn
        point = np.where(y_pred == y_test, 1, -1)
        cum_point = np.cumsum(point)

        ax_c = axes[idx, 1]
        ax_c.plot(cum_point, label='Cộng dồn điểm đúng/sai')
        ax_c.axhline(0, color='gray', linestyle='--')
        ax_c.set_title(f'{name} - Cộng dồn đúng/sai')
        ax_c.set_xlabel('Mẫu')
        ax_c.set_ylabel('Tổng điểm')
        ax_c.grid(True)
        ax_c.legend()

    fig.tight_layout()
    fig.suptitle("So sánh các thuật toán phân loại", fontsize=18, y=1.02)
    # plt.show()


# ---------------- Hàm dự đoán mẫu mới ----------------
def predict_new_point(x_new, scaler, classifiers, X_train, X_test, y_train):
    if scaler:
        x_new_scaled = scaler.transform([x_new])
    else:
        x_new_scaled = [x_new]

    # Kiểm tra lọc
    y_new_pred = is_pass_filtered(scaler, x_new, X, true_labels)
    if y_new_pred is None:
        return

    print(f"🎯 Mẫu mới vượt qua lọc. Tiến hành dự đoán bằng các mô hình...")

    # PCA nếu cần
    if X_train.shape[1] > 2:
        X_all = np.vstack((X_train, X_test, x_new_scaled))
        X_all_2d = PCA(n_components=2).fit_transform(X_all)
        X_test_2d = X_all_2d[len(X_train):-1]
        x_new_2d = X_all_2d[-1]
    else:
        X_test_2d = X_test
        x_new_2d = x_new_scaled[0]

    # Vẽ điểm mới trên từng mô hình
    num_models = len(classifiers)
    fig, axes = plt.subplots(num_models, 1, figsize=(10, 5 * num_models))
    if num_models == 1:
        axes = [axes]

    for idx, (name, model) in enumerate(classifiers.items()):
        model.fit(X_train, y_train)
        y_pred_test = model.predict(X_test)
        y_pred_new = model.predict([x_new_scaled[0]])[0]

        print(f"🔍 {name}: dự đoán mẫu mới là → {y_pred_new}")

        ax = axes[idx]
        ax.scatter(X_test_2d[:, 0], X_test_2d[:, 1], c=y_pred_test, cmap='tab10', s=20, label='Tập test')
        ax.scatter(x_new_2d[0], x_new_2d[1], c='red', s=120, marker='X', label='Mẫu mới')
        ax.set_title(f'{name} - Nhãn dự đoán mẫu mới: {y_pred_new}')
        ax.set_xlabel('Dim 1')
        ax.set_ylabel('Dim 2')
        ax.grid(True)
        ax.legend()

    fig.tight_layout()
    fig.suptitle("Dự đoán và vị trí mẫu mới trên các mô hình", fontsize=18, y=1.02)
    plt.show()


#thu x,y->split-> filter(x_train)->filter(x_test)->percent


scaler, X_filtered, y_filtered = filtered()
classifiers = {
    "KNN": KNeighborsClassifier(n_neighbors=5),
    "DecisionTree": DecisionTreeClassifier(),
    "RandomForest": RandomForestClassifier()
}

plot_data = {}
def load_polot_data():
    X_train, X_test, y_train, y_test = train_test_split(X_filtered, y_filtered, test_size=0.2)
    for idx, (name, model) in enumerate(classifiers.items()):
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred) * 100
        print(f"✅ {name} - Accuracy: {acc:.2f}%")

        # Danh sách điểm để scatter
        scatter_points = []
        for i in range(len(X_test)):
            scatter_points.append({
                "x": float(X_test[i][0]),
                "y": float(X_test[i][1]),
                "pred": int(y_pred[i]),
                "true": int(y_test[i])
            })

        # Cộng dồn điểm đúng/sai
        point = np.where(y_pred == y_test, 1, -1)
        cum_point = np.cumsum(point).tolist()  # chuyển sang list JSON-compatible

        # Ghi vào dict kết quả
        plot_data[name] = {
            "accuracy": round(acc, 2),
            "scatter": scatter_points,
            "cumsum": cum_point
        }






# Vẽ kết quả phân loại
# plot_per_classifier(X_train, X_test, y_train, y_test, classifiers)

# Dự đoán và vẽ điểm mới
# x_new = [100, 110233242 - 192246358]  # bạn có thể thay bằng bất kỳ giá trị nào
# predict_new_point(x_new, scaler, classifiers, X_train, X_test, y_train)
