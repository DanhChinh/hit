import time
from blessed import Terminal

term = Terminal()

def draw_table(data):
    # In tiêu đề bảng
    print(term.clear) # Xóa toàn bộ terminal
    for key, value in data[0].items():
        print(f"{key}", end=f"{'':15}")
    print()
    print("-" * 50)    
    for item in data:
        for key, value in item.items():
            print(f"{value}", end=f"{'':15}")
        print()

def update_row(row_number, new_data):
    # row_number là chỉ số dòng trong bảng (tính từ 0 cho dòng dữ liệu đầu tiên)
    with term.location(0, row_number + 2): # +2 vì có 2 dòng tiêu đề (tiêu đề cột và gạch ngang)
        print(term.clear_eol + f"{new_data['id']}\t{new_data['ten']}\t{new_data['trang_thai']}")

# Dữ liệu ban đầu

# draw_table(data)

# # Mô phỏng cập nhật dữ liệu
# time.sleep(2)
# print("\n" * 2 + "Dang cap nhat du lieu...")
# time.sleep(1)

# # Cập nhật sản phẩm B
# updated_b = {'id': 2, 'ten': 'San pham B', 'trang_thai': 'Hoan tat'}
# update_row(1, updated_b) # Cập nhật dòng thứ 2 (chỉ số 1)

# time.sleep(2)

# # Cập nhật sản phẩm A
# updated_a = {'id': 1, 'ten': 'San pham A', 'trang_thai': 'Ket thuc'}
# update_row(0, updated_a) # Cập nhật dòng thứ 1 (chỉ số 0)

# time.sleep(2)
# print("\n" * 2 + "Hoan tat.")