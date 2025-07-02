# GC Stats Toolbox

A Python toolbox for analyzing price activity and statistical patterns in futures/crypto/stock OHLCV data, with a focus on multi-timeframe studies and systematic hypothesis testing.

## Project Structure

```
.
├── gcstats/                # Main Python package (reusable modules)
│   ├── analysis.py
│   ├── experiments.py
│   ├── io.py
│   └── utils.py
├── scripts/                # Standalone analysis scripts
│   ├── analyze_timeframe.py
│   └── run_strong_hourly_close_experiment.py
├── data/
│   ├── raw/                # Raw OHLCV data (5m, 1h, etc.)
│   └── processed/          # Processed results and outputs
├── requirements.txt        # Python dependencies
├── setup.py                # Package installer
└── README.md
```

## Installation

1. Clone the repo and `cd` into the project root.
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. (Recommended) Install as an editable package:
   ```sh
   pip install -e .
   ```

## Usage

### 1. Analyze a Specific Timeframe (e.g., 09:00–09:20)

```sh
python -m scripts.analyze_timeframe data/raw/your_5min_file.csv
```

### 2. Run the Strong Hourly Close Pivot Experiment

This experiment tests the probability of price reversion after a strong hourly breakout, using 5-minute candles for intra-hour price action.

**Command:**
```sh
python -m scripts.run_strong_hourly_close_experiment data/raw/your_hourly_file.csv data/raw/your_5min_file.csv [data/processed/output.csv]
```
- The third argument is optional. If provided, results are saved as a CSV.

**What it does:**
- Detects strong closes on the hourly chart (close > previous high or < previous low).
- In the next hour, checks (using 5-min data):
  - If/when price returns to the previous hour's high/low (pivot), and in which 20-min segment (0–20, 20–40, 40–60).
  - After the pivot is hit, how often price returns to the next hour's open (TP1) and the strong close hour's high/low (TP2).
- Results are broken down by hour of day and segment, and can be output as a table or CSV.

## Example Output

```
| Hour   | Segment   |   Pivot Hits |   TP1 Hits | TP1 %   |   TP2 Hits | TP2 %   |
|--------|-----------|--------------|------------|---------|------------|---------|
| 09:00  | 00-20     |         1297 |       1020 | 78.6%   |       1297 | 100.0%  |
| 09:00  | 20-40     |          324 |         80 | 24.7%   |        324 | 100.0%  |
| ...    | ...       |          ... |        ... | ...     |        ... | ...     |
```

## Data Format

- **5-min and hourly data** should be CSV files with columns:
  - `datetime` (or `date` and `time`), `open`, `high`, `low`, `close`, `volume`
  - Example row: `23/06/2025;23:05;3365.5;3367.9;3364.9;3365.5;471`

## Customization
- Add your own scripts to `scripts/` or reusable functions to `gcstats/`.
- See `gcstats/experiments.py` for how to build new statistical tests.

## License
MIT
