import numpy as np

# Tạo dữ liệu ví dụ
array_2d_1 = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12], [13, 14]])
array_2d_2 = np.array([[10, 20], [30, 40], [50, 60], [70, 80], [90, 100], [110, 120], [130, 140]])
array_1d = np.array([100, 200, 300, 400, 500, 600, 700])

# Số lượng mẫu
n_samples = array_2d_1.shape[0]

# Tạo tập chỉ số ngẫu nhiên
random_indices = np.random.choice(n_samples, size=int(0.3 * n_samples), replace=False)

# Tách dữ liệu thành hai phần
# Phần 1: 30% dữ liệu ngẫu nhiên
array_2d_1_part1 = array_2d_1[random_indices]
array_2d_2_part1 = array_2d_2[random_indices]
array_1d_part1 = array_1d[random_indices]

# Phần 2: 70% dữ liệu còn lại
array_2d_1_part2 = np.delete(array_2d_1, random_indices, axis=0)
array_2d_2_part2 = np.delete(array_2d_2, random_indices, axis=0)
array_1d_part2 = np.delete(array_1d, random_indices)

# In kết quả
print("Phần 1 (30% dữ liệu ngẫu nhiên):")
print("array_2d_1_part1:\n", array_2d_1_part1)
print("array_2d_2_part1:\n", array_2d_2_part1)
print("array_1d_part1:\n", array_1d_part1)

print("\nPhần 2 (70% dữ liệu còn lại):")
print("array_2d_1_part2:\n", array_2d_1_part2)
print("array_2d_2_part2:\n", array_2d_2_part2)
print("array_1d_part2:\n", array_1d_part2)