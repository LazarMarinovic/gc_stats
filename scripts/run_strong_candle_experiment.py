import sys
from pathlib import Path
from gcstats.io import load_ohlcv
from gcstats.experiments import strong_candle_experiment

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_strong_candle_experiment.py <path_to_raw_data>")
        sys.exit(1)
    data_path = Path(sys.argv[1])
    df = load_ohlcv(data_path)
    results = strong_candle_experiment(df)
    print("Strong Candle Experiment Results:")
    for k, v in results.items():
        print(f"{k}: {v}") 