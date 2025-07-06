import pandas as pd
from pathlib import Path

def load_ohlcv(filepath: str | Path) -> pd.DataFrame:
    """
    Load OHLCV data from a CSV file with format:
    - 'datetime;open;high;low;close;volume'
    - or 'date;time;open;high;low;close;volume'
    Auto-detects format and parses accordingly.
    """
    df = pd.read_csv(filepath, sep=';')

    # If there is 'date' and 'time', use them to create 'datetime'
    if 'date' in df.columns and 'time' in df.columns:
        try:
            df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='%d.%m.%Y %H:%M')
        except ValueError:
            df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='%d/%m/%Y %H:%M')
        df = df.drop(['date', 'time'], axis=1)

    # If datetime column already exists
    elif 'datetime' in df.columns:
        # Automaticaly parse without specified format
        df['datetime'] = pd.to_datetime(df['datetime'], errors='raise', format='mixed')

    else:
        raise ValueError("CSV must have 'datetime' or 'date' and 'time' columns.")

    df = df[['datetime', 'open', 'high', 'low', 'close', 'volume']]
    return df
