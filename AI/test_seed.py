from db import df_get_hsft
sid = 1869907
size = 380
db, _ = df_get_hsft(sid, size)
print(db)