import sqlite3
import pandas as pd
def readTable():
    conn = sqlite3.connect("./qlearning/database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rounds")
    # rows = cursor.fetchall()  # Lấy tất cả dữ liệu
    # for row in rows:
    #     print(row)
    # conn.close()
    #
    df = pd.read_sql("SELECT * FROM rounds", conn)
    print(df)
    conn.close()

readTable()