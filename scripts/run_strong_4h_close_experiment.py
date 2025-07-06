import sys
from pathlib import Path
from gcstats.io import load_ohlcv
from gcstats.experiments import strong_4h_close_experiment

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python -m scripts.run_strong_4h_close_experiment <4h_data.csv> <five_min_data.csv> [output.csv]")
        sys.exit(1)

    fourh_path = Path(sys.argv[1])
    five_min_path = Path(sys.argv[2])
    csv_output = sys.argv[3] if len(sys.argv) > 3 else None

    fourh_df = load_ohlcv(fourh_path)
    five_min_df = load_ohlcv(five_min_path)

    strong_4h_close_experiment(fourh_df, five_min_df, print_every=10, csv_output=csv_output)
