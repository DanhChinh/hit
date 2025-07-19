import time
import random
from rich.live import Live
from rich.table import Table
from rich.text import Text

# Sử dụng lại lớp MyObject từ cuộc trò chuyện trước
class MyObject:
    def __init__(self, sid, name, status, progress_percent):
        self.sid = sid
        self.name = name
        self.status = status
        self.progress_percent = progress_percent # Thêm thuộc tính tiến độ

    def to_dict(self):
        return {
            "SID": self.sid,
            "Tên": self.name,
            "Trạng thái": self.status,
            "Tiến độ (%)": f"{self.progress_percent:.1f}" # Định dạng 1 chữ số thập phân
        }

    def update_status_and_progress(self):
        """Mô phỏng việc cập nhật trạng thái và tiến độ của đối tượng."""
        current_status = self.status
        if current_status == "Đang xử lý":
            if self.progress_percent < 100:
                self.progress_percent += random.uniform(5, 15)
                if self.progress_percent >= 100:
                    self.progress_percent = 100.0
                    self.status = "Hoàn thành"
            else:
                self.status = "Hoàn thành"
        elif current_status == "Chờ":
            if random.random() < 0.5: # 50% cơ hội bắt đầu xử lý
                self.status = "Đang xử lý"
                self.progress_percent = random.uniform(0, 10)
        elif current_status == "Lỗi":
            if random.random() < 0.2: # 20% cơ hội khắc phục lỗi
                self.status = "Đang xử lý"
                self.progress_percent = random.uniform(0, 5)
        elif current_status == "Hoàn thành":
            # Đối tượng hoàn thành có thể trở lại trạng thái chờ sau một thời gian
            if random.random() < 0.05:
                self.status = "Chờ"
                self.progress_percent = 0.0
        elif current_status == "Đã dừng":
            if random.random() < 0.1:
                self.status = "Chờ"
                self.progress_percent = 0.0

# Hàm tạo bảng từ danh sách các đối tượng
def generate_objects_table(objects_list):
    table = Table(title="Trạng thái Các Đối tượng", show_header=True, header_style="bold blue")

    # Thêm các cột dựa trên khóa của đối tượng đầu tiên (đảm bảo nhất quán)
    if not objects_list:
        return table # Trả về bảng rỗng nếu không có đối tượng nào

    # Lấy tiêu đề cột từ các khóa của to_dict()
    header_keys = list(objects_list[0].to_dict().keys())
    for key in header_keys:
        table.add_column(key, justify="left", style="green" if key == "Trạng thái" else None)

    # Thêm các hàng dữ liệu
    for obj in objects_list:
        row_values = []
        obj_dict = obj.to_dict()
        for key in header_keys: # Đảm bảo thứ tự cột
            value = obj_dict[key]
            # Tùy chỉnh màu sắc dựa trên trạng thái
            if key == "Trạng thái":
                if value == "Hoàn thành":
                    row_values.append(Text(value, style="bold green"))
                elif value == "Đang xử lý":
                    row_values.append(Text(value, style="bold yellow"))
                elif value == "Lỗi":
                    row_values.append(Text(value, style="bold red"))
                else:
                    row_values.append(Text(value, style="bold white"))
            elif key == "Tiến độ (%)":
                progress_val = float(value)
                if progress_val >= 100.0:
                    row_values.append(Text(value, style="bold magenta"))
                elif progress_val > 50:
                    row_values.append(Text(value, style="yellow"))
                else:
                    row_values.append(Text(value, style="white"))
            else:
                row_values.append(str(value))
        table.add_row(*row_values)
    return table

# Khởi tạo danh sách các đối tượng ban đầu
objects_data = [
    MyObject("OBJ001", "Thiết bị A", "Chờ", 0.0),
    MyObject("OBJ002", "Cảm biến B", "Đang xử lý", 25.0),
    MyObject("OBJ003", "Camera C", "Lỗi", 0.0),
    MyObject("OBJ004", "Server D", "Đã dừng", 0.0),
    MyObject("OBJ005", "Đèn E", "Chờ", 0.0),
]

print("Bắt đầu mô phỏng cập nhật bảng tự động. Nhấn Ctrl+C để thoát.")

# Sử dụng Live để tự động cập nhật bảng
# refresh_per_second: Tần suất làm mới bảng mỗi giây (ví dụ: 4 lần/giây)
with Live(generate_objects_table(objects_data), refresh_per_second=4, screen=True) as live:
    try:
        while True:
            # Mô phỏng thay đổi thuộc tính của các đối tượng
            # Mỗi lần lặp, chúng ta cập nhật trạng thái của MỘT đối tượng ngẫu nhiên
            obj_to_update = random.choice(objects_data)
            obj_to_update.update_status_and_progress()

            # Cập nhật nội dung Live với bảng mới
            live.update(generate_objects_table(objects_data))

            time.sleep(0.5) # Dừng một chút giữa các lần cập nhật

    except KeyboardInterrupt:
        print("\nĐã dừng mô phỏng.")