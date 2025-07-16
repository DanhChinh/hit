from collections import defaultdict
import json
import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors
# Đọc file CSV

def handle_progress(progress, isEnd = True):
    progress_arr = json.loads(progress)
    if isEnd and len(progress_arr) != 49:
        return None
    pair = progress_arr[34]
    # data = []
    # for pair in sublist:
    #     data.extend([pair[0]['bc'], pair[1]['bc'], pair[0]['v'],pair[1]['v']])
    return [pair[0]['bc']- pair[1]['bc'], pair[0]['v']-pair[1]['v']]

def make_data():
    df = pd.read_csv("data.csv")
    data_perfect = []
    label_perfect = []
    for index, row in df.iterrows():
        formater = handle_progress(row['progress'])
        if formater:
            data_perfect.append(formater)
            rs18 = row['d1']+row['d2']+row['d3']
            label_perfect.append(1 if rs18>10 else 0)


    data = np.array(data_perfect)
    label = np.array(label_perfect)

    # scaler = RobustScaler()
    # data_scaled = scaler.fit_transform(data)
    # data = np.round(data, 1)
    return data, label

def split_array(arr, ratio=0.7, shuffle=False):
    """
    Tách mảng thành 2 phần theo tỉ lệ cho trước (mặc định 7:3).
    
    Parameters:
        arr (list hoặc np.array): Mảng đầu vào.
        ratio (float): Tỉ lệ phần đầu tiên (0 < ratio < 1).
        shuffle (bool): Nếu True thì trộn ngẫu nhiên trước khi chia.

    Returns:
        tuple: (phần 1, phần 2)
    """
    
    arr = np.array(arr)
    if shuffle:
        np.random.shuffle(arr)

    split_idx = int(len(arr) * ratio)
    return arr[:split_idx], arr[split_idx:]


def filtered():
    X, y = make_data()
    scaler = RobustScaler()
    X = scaler.fit_transform(X) 
    knn = KNeighborsClassifier(n_neighbors=8)
    knn.fit(X, y)
    y_pred = knn.predict(X)

    # Chỉ giữ những mẫu dự đoán đúng
    mask = y_pred == y
    X_filtered = X[mask]
    y_filtered = y[mask]
    return scaler, X_filtered, y_filtered




def is_pass_filtered(scaler, x_new_raw, X_filtered, y_filtered, k=8, threshold_factor=2.0):
    """
    Kiểm tra xem một mẫu mới có 'đáng tin' hay không dựa vào khoảng cách đến hàng xóm gần nhất.
    
    Args:
        scaler: Bộ chuẩn hóa đã được huấn luyện (RobustScaler, v.v.)
        x_new_raw: Mẫu mới (dạng list hoặc array chưa scale)
        X_filtered: Dữ liệu đã được lọc (được scale)
        y_filtered: Nhãn tương ứng
        k: Số lượng hàng xóm (default: 8)
        threshold_factor: Hệ số nhân cho std khi xác định ngưỡng
    
    Returns:
        (label, distance, threshold, is_reliable): tuple
    """

    # 1. Train lại mô hình KNN
    knn_filtered = KNeighborsClassifier(n_neighbors=k)
    knn_filtered.fit(X_filtered, y_filtered)

    # 2. Chuẩn hóa mẫu mới
    x_new_scaled = scaler.transform([x_new_raw])

    # 3. Dự đoán nhãn
    y_new_pred = knn_filtered.predict(x_new_scaled)[0]

    # 4. Tính ngưỡng khoảng cách tự động
    nn = NearestNeighbors(n_neighbors=2)  # n=2 để bỏ chính nó
    nn.fit(X_filtered)
    distances_all, _ = nn.kneighbors(X_filtered)
    nearest_distances = distances_all[:, 1]  # khoảng cách đến hàng xóm gần nhất (bỏ chính nó)

    mean_dist = nearest_distances.mean()
    std_dist = nearest_distances.std()
    threshold = mean_dist + threshold_factor * std_dist

    # 5. Tính khoảng cách của mẫu mới đến hàng xóm gần nhất
    distances_new, _ = knn_filtered.kneighbors(x_new_scaled)
    distance_to_nearest = distances_new[0][0]

    is_reliable = distance_to_nearest <= threshold

    print(f"📌 Mẫu mới (scaled): {x_new_scaled}")
    print(f"✅ Nhãn dự đoán: {y_new_pred}")
    print(f"📏 Khoảng cách đến hàng xóm gần nhất: {distance_to_nearest:.4f}")
    print(f"📊 Ngưỡng khoảng cách tin cậy (auto): {threshold:.4f}")
    if not is_reliable:
        print("⚠️ Mẫu có thể không đáng tin (quá xa tập tin cậy)")
        return None

    return y_new_pred




