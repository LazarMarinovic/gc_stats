import sys
from pathlib import Path
from gcstats.io import load_ohlcv
from gcstats.experiments import strong_hourly_close_experiment

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python -m scripts.run_strong_hourly_close_experiment <hourly_data.csv> <five_min_data.csv> [output.csv]")
        sys.exit(1)
    hourly_path = Path(sys.argv[1])
    five_min_path = Path(sys.argv[2])
    csv_output = sys.argv[3] if len(sys.argv) > 3 else None
    hourly_df = load_ohlcv(hourly_path)
    five_min_df = load_ohlcv(five_min_path)
    strong_hourly_close_experiment(hourly_df, five_min_df, print_every=10, csv_output=csv_output) 