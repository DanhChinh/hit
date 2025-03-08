from db import readTable
from datetime import datetime

df = readTable().head(15)
print(df)
