from db import readTable
import os, json

def load_q_table(file_path = 'q_table.json'):
    """Tải Q-Table từ file JSON."""
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    else:
        return {}




def fix_id():
    import sqlite3
    import pandas as pd
    import numpy as np

    # Kết nối đến database SQLite
    conn = sqlite3.connect('database.db')

    # Đọc dữ liệu vào DataFrame
    df = pd.read_sql("SELECT * FROM rounds", conn)

    # Tìm giá trị ID lớn nhất hiện có (bỏ qua NaN)
    max_id = df['id'].dropna().max()

    # Chuyển giá trị FLOAT thành INTEGER (loại trừ NaN)
    df['id'] = df['id'].apply(lambda x: int(x) if isinstance(x, float) and not np.isnan(x) else x)

    # Thay NaN bằng ID tăng dần
    counter = max_id + 1  # Bắt đầu từ ID lớn nhất hiện có + 1
    def replace_nan(x):
        global counter
        if pd.isna(x):  # Nếu là NaN, thay bằng giá trị tiếp theo
            x = counter
            counter += 1  # Tăng giá trị cho dòng tiếp theo
        return x

    df['id'] = df['id'].apply(replace_nan)

    # Ghi lại vào database (cập nhật bảng)
    df.to_sql('rounds', conn, if_exists='replace', index=False)

    # Đóng kết nối database
    conn.close()

    print("✅ Hoàn thành xử lý ID!")


def delete_sid():
    import sqlite3
    import pandas as pd
# Kết nối database
    conn = sqlite3.connect('database.db')

    # Đọc dữ liệu
    df = pd.read_sql("SELECT * FROM rounds", conn)

    # Xóa các dòng có `sid` trùng nhau, chỉ giữ lại dòng đầu tiên
    df = df.drop_duplicates(subset=['sid'], keep='first')

    # Ghi lại vào database
    df.to_sql('rounds', conn, if_exists='replace', index=False)

    # Đóng kết nối
    conn.close()


