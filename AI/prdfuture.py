import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

import random

# Giả sử đây là bộ dữ liệu mẫu, ví dụ về doanh thu hàng tháng trong 12 tháng
data = [1,2,1,-1,1,2,-1,1,2,1,-1,1,2,-1,1,2,1,-1,1,2,-1,1,2,1,-1,1,2,-1]

# Chuyển dữ liệu thành một chuỗi thời gian (time series)
data_series = pd.Series(data)

# Chia dữ liệu thành tập huấn luyện (training) và tập kiểm tra (test)
train_data = data_series[:-3]
test_data = data_series[-3:]
# Huấn luyện mô hình ARIMA
model = ARIMA(train_data, order=(1, 0, 0))  # Chọn tham số (p=1, d=0, q=0) cho ARIMA
model_fit = model.fit()

# Dự báo 3 tháng tiếp theo
forecast = model_fit.forecast(steps=10)

# In ra kết quả dự báo
print("Dự báo 3 tháng tiếp theo:", forecast)

# Vẽ đồ thị dự báo so với dữ liệu thực tế
plt.plot(train_data, label='Dữ liệu huấn luyện')
plt.plot(range(len(train_data), len(train_data) + len(forecast)), forecast, label='Dự báo', color='red')
plt.plot(range(len(train_data), len(train_data) + len(test_data)), test_data, label='Dữ liệu thực tế', color='green')
plt.title('Dự báo với ARIMA')
plt.legend()
plt.show()
