import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Parameters
start_time = datetime(2024, 1, 1, 0, 0)
num_candles = 200  # 200 x 4h = ~33 dana

data = []
current_time = start_time
price = 1000

for _ in range(num_candles):
    open_price = price
    high = open_price + np.random.uniform(5, 20)
    low = open_price - np.random.uniform(5, 20)
    close = np.random.uniform(low, high)
    volume = np.random.randint(100, 1000)

    data.append([
        current_time.strftime('%Y-%m-%d %H:%M'),
        round(open_price, 2),
        round(high, 2),
        round(low, 2),
        round(close, 2),
        volume
    ])

    current_time += timedelta(hours=4)
    price = close  # next open = current close

df = pd.DataFrame(data, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])

# Save to processed/
df.to_csv("data/processed/4h.csv", sep=';', index=False)
print("✅ Generated 4h.csv with", len(df), "candles.")
