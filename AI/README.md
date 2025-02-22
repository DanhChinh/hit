#chay truong trinh an tren window
pythonw.exe app.py
start python -m flask run

sudo systemctl stop flaskapp.service



#chay truong trinh an tren linux
nohup python app.py &
screen -S flask-app
python app.py
# Nhấn Ctrl+A sau đó nhấn D để thoát khỏi session mà không dừng chương trình.

