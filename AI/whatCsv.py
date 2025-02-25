import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Đọc file CSV, sử dụng cột đầu tiên làm index
df = pd.read_csv('q_table.csv', index_col=0)

print("DataFrame gốc:")
print(df)

# Vẽ heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(df, annot=False, cmap='coolwarm', fmt='g')
plt.title("Biểu đồ màu sắc (Heatmap)")
plt.xlabel("Các cột")
plt.ylabel("Các hàng")
plt.show()