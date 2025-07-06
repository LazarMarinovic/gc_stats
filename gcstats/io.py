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

    # Ako ima 'date' i 'time', koristi ih za kreiranje 'datetime'
    if 'date' in df.columns and 'time' in df.columns:
        try:
            df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='%d.%m.%Y %H:%M')
        except ValueError:
            df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='%d/%m/%Y %H:%M')
        df = df.drop(['date', 'time'], axis=1)

    # Ako ima već datetime kolonu
    elif 'datetime' in df.columns:
        # Samo automatski parsiraj bez specificiranja formata
        df['datetime'] = pd.to_datetime(df['datetime'], errors='raise', format='mixed')

    else:
        raise ValueError("CSV mora imati 'datetime' ili 'date' i 'time' kolone.")

    df = df[['datetime', 'open', 'high', 'low', 'close', 'volume']]
    return df
