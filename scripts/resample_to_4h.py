import pandas as pd
import os

INPUT_PATH = "data/processed/hourly.csv"
OUTPUT_PATH = "data/processed/4h.csv"

# Load 1h candles
df = pd.read_csv(INPUT_PATH, sep=";")


# Join columns 'date' and 'time' into one datetime object
if "date" in df.columns and "time" in df.columns:
    df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"], dayfirst=True)
elif "datetime" in df.columns:
    df["datetime"] = pd.to_datetime(df["datetime"], dayfirst=True)
else:
    raise ValueError("CSV must have 'datetime' or 'date' and 'time' columns")

df = df.set_index("datetime")

# Resample on 4h
df_4h = df.resample("4H").agg({
    "open": "first",
    "high": "max",
    "low": "min",
    "close": "last",
    "volume": "sum"
})

# Remove unnecessary columns
df_4h = df_4h.dropna().reset_index()

# Record file
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
df_4h.to_csv(OUTPUT_PATH, sep=";", index=False)

print(f"✅ 4h candles saved into '{OUTPUT_PATH}'")
