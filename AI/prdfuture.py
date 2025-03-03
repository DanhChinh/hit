import pandas as pd
from pmdarima import auto_arima

def prdfuture(data):
    data_cumsum = pd.Series(data).cumsum()  # Cộng dồn dữ liệu để tạo xu hướng
    model = auto_arima(data_cumsum, seasonal=False, trace=True, suppress_warnings=True)
    return model.predict(n_periods=10)


prdfuture([1,2,3,4,5,6,7,8,9])
