from db import readTable
import os, json

def load_q_table(file_path = 'q_table.json'):
    """Tải Q-Table từ file JSON."""
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    else:
        return {}

q_table = load_q_table()

print("len of state:", len(q_table))
df = readTable()
print(df)