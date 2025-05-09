import requests, json, os
def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
def load_json( path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return {}
def get_db_data():
    try:
        response = requests.get('https://thuhuyen.fun/xg79/get_data.php')
        response.raise_for_status()  # Kiểm tra lỗi HTTP

        data = response.json()  # Giải mã JSON

        if data.get('success'):
            print('Dữ liệu đã được lấy thành công')
            return (data['data'])

        else:
            print('Lỗi:', data.get('message'))
            return []

    except requests.exceptions.RequestException as e:
        print('Lỗi kết nối:', e)
        return []
def simple_data():
    db_data = get_db_data()
    data = []
    for dt in db_data:
        sid = dt['sid']
        progress = json.loads(dt['progress'])[:40]
        result = 1 if (int(dt['d1']) + int(dt['d3']) + int(dt['d3'])) > 10 else 2
        record = {"sid": sid, "progress": progress, "result": result}
        data.append(record)
    save_json('data.json', data)
    return data

def get_percent(A, B):
    if A+B>0:
        return round(A/(A+B),2)
    return 0.5






