import pandas as pd

def filter_timeframe(df: pd.DataFrame, start_time: str, end_time: str) -> pd.DataFrame:
    """
    Filter DataFrame rows where the time part of 'datetime' is between start_time and end_time (inclusive).
    start_time, end_time: strings in 'HH:MM' 24-hour format.
    """
    times = df['datetime'].dt.time
    start = pd.to_datetime(start_time, format='%H:%M').time()
    end = pd.to_datetime(end_time, format='%H:%M').time()
    mask = (times >= start) & (times <= end)
    return df[mask]
