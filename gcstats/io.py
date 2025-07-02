import pandas as pd
from pathlib import Path

def load_ohlcv(filepath: str | Path) -> pd.DataFrame:
    """
    Load OHLCV data from a CSV file with format:
    date;time;open;high;low;close;volume
    Returns a DataFrame with a combined datetime column.
    """
    df = pd.read_csv(filepath, sep=';', names=[
        'date', 'time', 'open', 'high', 'low', 'close', 'volume'
    ])
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='%d/%m/%Y %H:%M')
    df = df.drop(['date', 'time'], axis=1)
    df = df[['datetime', 'open', 'high', 'low', 'close', 'volume']]
    return df
