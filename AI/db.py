import sqlite3
import threading
import pandas as pd
import numpy as np





def createTable(file_path="database.db"):
    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rounds (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sid INTEGER,
        mB INTEGER,
        mW INTEGER,
        uB INTEGER,
        uW INTEGER,
        xx1 INTEGER,
        xx2 INTEGER,
        xx3 INTEGER,
        rs18 INTEGER,
        prf INTEGER
    )
    """)
    conn.commit()
    conn.close()
def addData(arr, file_path="database.db"):
    [sid ,mB, mW, uB, uW, xx1, xx2, xx3, rs18, prf] = arr
    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO rounds (sid, mB, mW, uB, uW, xx1, xx2, xx3, rs18, prf) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (sid, mB, mW, uB, uW, xx1, xx2, xx3, rs18, prf))
    conn.commit() 
    conn.close()

def readTable(file_path="database.db"): #limit 1500
    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rounds")
    # df = pd.read_sql("SELECT * FROM rounds ORDER BY id DESC LIMIT 1500", conn)
    df = pd.read_sql("SELECT * FROM rounds", conn)
    conn.close()
    return df 



def df_get_hsft(sid_value, size = 10):
    conn = sqlite3.connect('database.db')
    # Truy vấn lấy các dòng có `sid` trong khoảng từ `sid-5` đến `sid`
    query_state = f"SELECT * FROM rounds WHERE sid BETWEEN {sid_value - size} AND {sid_value}"
    query_reward = f"SELECT * FROM rounds WHERE sid = {sid_value+1}"
    state = pd.read_sql(query_state, conn)
    reward = pd.read_sql(query_reward, conn)
    # Đóng kết nối
    conn.close()
    return state, reward

