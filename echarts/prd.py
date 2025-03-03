import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from scipy.signal import argrelextrema

# Hàm tính đạo hàm bậc nhất
def first_derivative(data):
    return np.gradient(data)

# Hàm tính đạo hàm bậc hai
def second_derivative(data):
    return np.gradient(first_derivative(data))

# Hàm tìm cực trị
def find_extrema(data):
    # Tìm cực đại
    maxima_indices = argrelextrema(data, np.greater)[0]
    maxima_values = data[maxima_indices]
    
    # Tìm cực tiểu
    minima_indices = argrelextrema(data, np.less)[0]
    minima_values = data[minima_indices]
    
    return maxima_indices, maxima_values, minima_indices, minima_values

# Hàm tìm điểm uốn
def find_inflection_points(data):
    second_deriv = second_derivative(data)
    inflection_indices = np.where(np.diff(np.sign(second_deriv)))[0]
    inflection_values = data[inflection_indices]
    return inflection_indices, inflection_values

# Hàm dự đoán giá trị tiếp theo bằng ARIMA
def predict_future(data, steps=5):
    model = ARIMA(data, order=(1, 1, 1))  # Tham số (p, d, q) có thể điều chỉnh
    model_fit = model.fit()
    predictions = model_fit.forecast(steps=steps)
    return predictions

# Dữ liệu lịch sử (các mảng giá trị tăng giảm)
historical_data = [
    np.array([1, 3, 2, 4, 1]),
    np.array([-2, 0, 3, -1, 2, -3]),
    np.array([5, 2, 6, 3, 7, 4, 8])
]

# Huấn luyện mô hình ARIMA trên dữ liệu lịch sử
def train_arima_model(historical_data):
    # Kết hợp tất cả dữ liệu lịch sử thành một mảng duy nhất
    combined_data = np.concatenate(historical_data)
    
    # Huấn luyện mô hình ARIMA
    model = ARIMA(combined_data, order=(1, 1, 1))  # Tham số (p, d, q) có thể điều chỉnh
    model_fit = model.fit()
    return model_fit

# Huấn luyện mô hình
trained_model = train_arima_model(historical_data)

# Dữ liệu đầu vào (phần đầu của mảng mới)
initial_data = np.array([1, 6, -4, 2])

# Dự đoán các giá trị tiếp theo
future_predictions = trained_model.forecast(steps=5)
full_data = np.concatenate((initial_data, future_predictions))

# Tìm cực trị và điểm uốn
maxima_indices, maxima_values, minima_indices, minima_values = find_extrema(full_data)
inflection_indices, inflection_values = find_inflection_points(full_data)

# In kết quả
print("Dữ liệu đầy đủ (bao gồm dự đoán):", full_data)
print("Cực đại tại các vị trí:", maxima_indices, "với giá trị:", maxima_values)
print("Cực tiểu tại các vị trí:", minima_indices, "với giá trị:", minima_values)
print("Điểm uốn tại các vị trí:", inflection_indices, "với giá trị:", inflection_values)