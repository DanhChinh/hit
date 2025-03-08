import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress
def get_slope(data):
    """
    Tính độ dốc trung bình của dữ liệu.
    Nếu độ dốc > 0 → Xu hướng tăng.
    Nếu độ dốc < 0 → Xu hướng giảm.
    """
    if len(data) < 2:
        return 0  # Không đủ dữ liệu để tính toán
    slope = (data[-1] - data[0]) / len(data)
    return slope
def get_correlation(data):
    """
    Tính hệ số tương quan r giữa chỉ số và dữ liệu.
    Nếu r > 0.5 → Xu hướng tăng.
    Nếu r < -0.5 → Xu hướng giảm.
    """
    if len(data) < 2:
        return 0  # Không đủ dữ liệu để tính toán

    x = np.arange(len(data))  # Chỉ số x: [0,1,2,...]
    slope, intercept, r_value, p_value, std_err = linregress(x, data)
    return r_value
def draw(arr):
    arr = np.cumsum(np.array(arr))
    print("get_slope:", get_slope(arr))
    print("get_correlation:", get_correlation(arr))
    plt.plot([i for i in range(len(arr))], arr, marker='o', linestyle='-', color='b', label='Dữ liệu')
    plt.show()



arr = [0,1,1,-1,-1,-1]
draw(arr)