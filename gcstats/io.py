import pandas as pd
from pathlib import Path

def load_ohlcv(filepath: str | Path) -> pd.DataFrame:
    """
    Load OHLCV data from a CSV file with format:
    - 'datetime;open;high;low;close;volume'
    - or 'date;time;open;high;low;close;volume'
    Auto-detects format and parses accordingly.
    Also supports files without headers (first row is data).
    """
    try:
        df = pd.read_csv(filepath, sep=';')
    except Exception as e:
        raise ValueError(f"Failed to read CSV: {e}")

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

    # If columns are missing, try to read as headerless and assign columns
    else:
        # Try to infer by number of columns
        df2 = pd.read_csv(filepath, sep=';', header=None)
        if df2.shape[1] == 7:
            df2.columns = ['date', 'time', 'open', 'high', 'low', 'close', 'volume']
            try:
                df2['datetime'] = pd.to_datetime(df2['date'] + ' ' + df2['time'], format='%d.%m.%Y %H:%M')
            except ValueError:
                df2['datetime'] = pd.to_datetime(df2['date'] + ' ' + df2['time'], format='%d/%m/%Y %H:%M')
            df2 = df2.drop(['date', 'time'], axis=1)
        elif df2.shape[1] == 6:
            df2.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume']
            df2['datetime'] = pd.to_datetime(df2['datetime'], errors='raise', format='mixed')
        else:
            raise ValueError("CSV must have 6 or 7 columns if no header is present.")
        df = df2

    df = df[['datetime', 'open', 'high', 'low', 'close', 'volume']]
    return df
