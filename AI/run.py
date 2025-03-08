from models import makePredict
from db import df_get_hsft

last_sid = 1869907

for sid in range(last_sid-330, last_sid):
    predictions = makePredict(sid)
    print(f"sid: {sid}, predictions: {predictions}")
