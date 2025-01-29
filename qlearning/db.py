import sqlite3
import threading
import pandas as pd
import numpy as np





def createTable():
    conn = sqlite3.connect("database.db")
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
def addData(sid, mB, mW, uB, uW, xx1, xx2, xx3, rs18, prf):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO rounds (sid, mB, mW, uB, uW, xx1, xx2, xx3, rs18, prf) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (sid, mB, mW, uB, uW, xx1, xx2, xx3, rs18, prf))
    conn.commit()  # Lưu thay đổi
    conn.close()

def readTable():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rounds")
    # rows = cursor.fetchall()  # Lấy tất cả dữ liệu
    # for row in rows:
    #     print(row)
    # conn.close()
    #
    df = pd.read_sql("SELECT * FROM rounds", conn)
    conn.close()
    return df 
def readHs(sid):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rounds WHERE sid BETWEEN? AND?", (sid-5, sid))
    rows = cursor.fetchall()
    conn.close()
    # print(np.array(rows))
    if len(rows)!=6:
        return []
    
    return np.array(rows)
def readLine(sid):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rounds WHERE sid =?", (sid,))
    row = cursor.fetchone()
    conn.close()
    return row
# thread = threading.Thread(target=db_task)
# thread.start()
# thread.join()


