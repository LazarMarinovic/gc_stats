import sys
from pathlib import Path
from gcstats.io import load_ohlcv
from gcstats.analysis import filter_timeframe

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_timeframe.py <path_to_raw_data>")
        sys.exit(1)
    data_path = Path(sys.argv[1])
    df = load_ohlcv(data_path)
    filtered = filter_timeframe(df, "09:00", "09:20")
    print(filtered)
