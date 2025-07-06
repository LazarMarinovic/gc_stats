import pandas as pd
import os

INPUT_PATH = "data/processed/hourly.csv"
OUTPUT_PATH = "data/processed/4h.csv"

# Učitaj 1h candle-ove
df = pd.read_csv(INPUT_PATH, sep=";")

# Pretvori kolone 'date' i 'time' u jedan datetime objekat ako su odvojene
if "date" in df.columns and "time" in df.columns:
    df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"], dayfirst=True)
elif "datetime" in df.columns:
    df["datetime"] = pd.to_datetime(df["datetime"], dayfirst=True)
else:
    raise ValueError("CSV mora imati 'datetime' ili 'date' i 'time' kolone")

df = df.set_index("datetime")

# Resample na 4h
df_4h = df.resample("4H").agg({
    "open": "first",
    "high": "max",
    "low": "min",
    "close": "last",
    "volume": "sum"
})

# Ukloni nepotpune redove
df_4h = df_4h.dropna().reset_index()

# Snimi fajl
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
df_4h.to_csv(OUTPUT_PATH, sep=";", index=False)

print(f"✅ 4h candle-ovi sačuvani u '{OUTPUT_PATH}'")
