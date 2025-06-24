from collections import defaultdict
import requests
import json
import numpy
def get_data_from_webdb():
    url = 'https://thuhuyen.fun/xg79/get_data.php'
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Gây lỗi nếu mã HTTP != 200

        data = response.json()
        return data.get("data", None)

    except requests.exceptions.RequestException as e:
        print("Lỗi kết nối:", e)
        return None



import pandas as pd

# Đọc file CSV
df = pd.read_csv("data.csv")

def handle_progress(progress, isEnd = True):
    progress_arr = json.loads(progress)
    if isEnd and len(progress_arr) != 49:
        return 0, 0, 0, 0
    sublist = progress_arr[37:40]

    sum_bc = defaultdict(int)
    sum_v = defaultdict(int)
    count = defaultdict(int)

    for pair in sublist:
        for item in pair:
            eid = item["eid"]
            sum_bc[eid] += item["bc"]
            sum_v[eid] += item["v"]
            count[eid] += 1

    # for eid in sum_bc:
    #     avg_bc = sum_bc[eid] / count[eid]
    #     avg_v = sum_v[eid] / count[eid]
    #     print(f"[eid={eid}] Trung bình bc: {avg_bc}, Trung bình v: {avg_v}")
    return int(sum_bc[1] / 3), int(sum_v[1] / 3000000), int(sum_bc[2] / 3), int(sum_v[2] / 3000000)




data_perfect = []
for index, row in df.iterrows():
    avg_bc1, avg_v1, avg_bc2, avg_v2 = handle_progress(row['progress'])
    if avg_bc1:
        data_perfect.append([avg_bc1, avg_v1, avg_bc2, avg_v2])


data = numpy.array(data_perfect)



import numpy as np
from sklearn.preprocessing import RobustScaler

scaler = RobustScaler()
data_scaled = scaler.fit_transform(data)
data_rounded = np.round(data_scaled, 1)

for i in data_rounded:
    print(i)