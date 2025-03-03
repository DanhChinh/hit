import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# Tạo dữ liệu giả lập cho ví dụ (Chuỗi thời gian hàng tháng)
np.random.seed(42)
n = 100  # Số lượng điểm dữ liệu
data = np.random.randn(n)  # Dữ liệu ngẫu nhiên
print(data)
data = pd.Series(data).cumsum()  # Cộng dồn dữ liệu để tạo xu hướng
print(data)
# Vẽ đồ thị chuỗi thời gian
plt.plot(data)
plt.title('Dữ liệu chuỗi thời gian')
plt.show()

# Phân tích ACF và PACF để xác định các tham số p, d, q
plot_acf(data)
plot_pacf(data)
plt.show()

# Mô hình ARIMA (p, d, q)
# Ở đây ta giả sử p=1, d=1, q=1 từ kết quả phân tích ACF và PACF
model = ARIMA(data, order=(1, 1, 1))
model_fit = model.fit()

# In ra tóm tắt kết quả mô hình
print(model_fit.summary())

# Dự báo trong 10 bước tiếp theo
forecast = model_fit.forecast(steps=10)
print('Dự báo:', forecast)

# Vẽ dự báo
plt.plot(data, label='Dữ liệu thực tế')
plt.plot(np.arange(n, n + 10), forecast, label='Dự báo', color='red')
plt.legend()
plt.show()
