import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pmdarima import auto_arima

# Tạo dữ liệu chuỗi thời gian giả lập

def predict_the_chain(data, save_path):
    data = pd.Series(data).cumsum()  # Cộng dồn dữ liệu để tạo xu hướng

    # Vẽ đồ thị chuỗi thời gian

    # Sử dụng auto_arima để tìm mô hình ARIMA tốt nhất
    model = auto_arima(data, seasonal=False, trace=True, suppress_warnings=True)

    # In ra tóm tắt kết quả mô hình
    # print(model.summary())

    # Dự báo trong 10 bước tiếp theo
    forecast = model.predict(n_periods=10)
    # print('Dự báo:', forecast)

    # Vẽ dự báo
    plt.plot(data, label='Dữ liệu thực tế')
    plt.plot(np.arange(n, n + 10), forecast, label='Dự báo', color='red')
    plt.savefig(save_path)

predict_the_chain([1,2,3,4,5,6,7,8,9], "./../src/img/prdfuture.png")
