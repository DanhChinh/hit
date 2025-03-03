from db import readTable

def unique():
    import sqlite3

    # Kết nối đến cơ sở dữ liệu SQLite
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Câu truy vấn SQL để xóa các bản ghi trùng lặp
    # Chỉ giữ lại bản ghi đầu tiên cho mỗi giá trị trong column_name
    cursor.execute("""
        DELETE FROM rounds
        WHERE rowid NOT IN (
            SELECT MIN(rowid)
            FROM rounds
            GROUP BY sid
        );
    """)

    # Lưu thay đổi
    conn.commit()

    # Đóng kết nối
    conn.close()

    print("Đã xóa các hàng trùng lặp.")

# prfs = df['prf'].to_numpy()

# total=0
# prf_plus = []
# for prf in prfs:
#     total += prf/1000000000
#     prf_plus.append(total)

# print(prfs)
# slope = (prf_plus[-1] - prf_plus[0]) / len(prf_plus)  # Tính độ dốc trung bình

# if slope > 0:
#     print("Xu hướng tăng 📈")
# elif slope < 0:
#     print("Xu hướng giảm 📉")
# else:
#     print("Không có xu hướng rõ ràng")

# import matplotlib.pyplot as plt
# import numpy as np



# # Vẽ biểu đồ
# plt.plot(prf_plus, marker='o', linestyle='-', color='b', label="Giá trị")

# # Thêm tiêu đề và nhãn
# plt.title("Biểu đồ Line của mảng dữ liệu")
# plt.xlabel("Chỉ số")
# plt.ylabel("Giá trị")

# # Hiển thị chú thích
# plt.legend()

# # Hiển thị biểu đồ
# plt.show()
df = readTable()
print(df)
df = readTable()
print(df)