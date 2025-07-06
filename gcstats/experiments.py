import pandas as pd
from typing import Dict, Any, Optional
from tabulate import tabulate
import numpy as np
import os

def strong_candle_experiment(df: pd.DataFrame, timeframe_minutes: int = 20) -> Dict[str, float]:
    """
    Run the strong closed candle experiment for both bullish and bearish cases.
    Returns statistics as a dict.
    """
    n_candles = timeframe_minutes // 5  # assuming 5-min candles
    bullish_total = bearish_total = 0
    bullish_tp1 = bullish_tp2 = 0
    bearish_tp1 = bearish_tp2 = 0
    event_count = 0

    for i in range(1, len(df) - n_candles):
        prev = df.iloc[i - 1]
        curr = df.iloc[i]
        # Bullish strong close
        if curr['close'] > prev['high']:
            print(f"[Bullish] Strong close at index {i}, datetime {curr['datetime']}")
            pivot = prev['high']
            strong_open = curr['open']
            strong_high = curr['high']
            # Look ahead n_candles for pivot hit
            for j in range(1, n_candles + 1):
                next_candle = df.iloc[i + j]
                if next_candle['low'] <= pivot <= next_candle['high']:
                    bullish_total += 1
                    event_count += 1
                    print(f"  [Bullish] Pivot hit at index {i + j}, datetime {next_candle['datetime']}")
                    # After pivot hit, check for TP1 and TP2
                    after_pivot = df.iloc[i + j:]
                    # TP1: return to strong_open
                    if any((after_pivot['low'] <= strong_open) & (after_pivot['high'] >= strong_open)):
                        bullish_tp1 += 1
                        print(f"    [Bullish] TP1 hit after pivot.")
                    # TP2: return to strong_high
                    if any((after_pivot['low'] <= strong_high) & (after_pivot['high'] >= strong_high)):
                        bullish_tp2 += 1
                        print(f"    [Bullish] TP2 hit after pivot.")
                    break
        # Bearish strong close
        elif curr['close'] < prev['low']:
            print(f"[Bearish] Strong close at index {i}, datetime {curr['datetime']}")
            pivot = prev['low']
            strong_open = curr['open']
            strong_low = curr['low']
            for j in range(1, n_candles + 1):
                next_candle = df.iloc[i + j]
                if next_candle['low'] <= pivot <= next_candle['high']:
                    bearish_total += 1
                    event_count += 1
                    print(f"  [Bearish] Pivot hit at index {i + j}, datetime {next_candle['datetime']}")
                    after_pivot = df.iloc[i + j:]
                    # TP1: return to strong_open
                    if any((after_pivot['low'] <= strong_open) & (after_pivot['high'] >= strong_open)):
                        bearish_tp1 += 1
                        print(f"    [Bearish] TP1 hit after pivot.")
                    # TP2: return to strong_low
                    if any((after_pivot['low'] <= strong_low) & (after_pivot['high'] >= strong_low)):
                        bearish_tp2 += 1
                        print(f"    [Bearish] TP2 hit after pivot.")
                    break
        if event_count > 0 and event_count % 100 == 0:
            print(f"Processed {event_count} events so far...")

    print("\nExperiment complete.")
    print(f"Total bullish events: {bullish_total}")
    print(f"Total bearish events: {bearish_total}")
    print(f"Bullish TP1 hits: {bullish_tp1}")
    print(f"Bullish TP2 hits: {bullish_tp2}")
    print(f"Bearish TP1 hits: {bearish_tp1}")
    print(f"Bearish TP2 hits: {bearish_tp2}")

    return {
        'bullish_total': bullish_total,
        'bullish_tp1': bullish_tp1,
        'bullish_tp2': bullish_tp2,
        'bullish_tp1_pct': bullish_tp1 / bullish_total * 100 if bullish_total else 0,
        'bullish_tp2_pct': bullish_tp2 / bullish_total * 100 if bullish_total else 0,
        'bearish_total': bearish_total,
        'bearish_tp1': bearish_tp1,
        'bearish_tp2': bearish_tp2,
        'bearish_tp1_pct': bearish_tp1 / bearish_total * 100 if bearish_total else 0,
        'bearish_tp2_pct': bearish_tp2 / bearish_total * 100 if bearish_total else 0,
    }

def strong_hourly_close_experiment(hourly_df: pd.DataFrame, five_min_df: pd.DataFrame, print_every: int = 10, csv_output: Optional[str] = None) -> Dict[str, Any]:
    """
    For each strong close on the hourly chart, use 5-min data in the NEXT hour to check:
    - When price hits the pivot (2 hours ago high/low), and in which 20-min segment (0-20, 20-40, 40-60)
    - After pivot is hit, if/when price returns to TP1 (next hour open) and/or TP2 (strong close hour high/low) within the next hour
    Prints a live-updating table of stats by hour and segment.
    Optionally outputs the final table to a CSV file.
    """
    stats = {}
    segments = [(0, 20), (20, 40), (40, 60)]
    segment_labels = ["00-20", "20-40", "40-60"]
    event_count = 0

    hourly_df = hourly_df.copy()
    five_min_df = five_min_df.copy()
    hourly_df['datetime'] = pd.to_datetime(hourly_df['datetime'])
    five_min_df['datetime'] = pd.to_datetime(five_min_df['datetime'])
    hourly_df = hourly_df.sort_values('datetime').reset_index(drop=True)
    five_min_df = five_min_df.sort_values('datetime').reset_index(drop=True)

    for i in range(2, len(hourly_df)):
        candle2 = hourly_df.iloc[i-2]  # pivot candle
        candle1 = hourly_df.iloc[i-1]  # strong close candle
        candle0 = hourly_df.iloc[i]    # test candle (next hour)
        hour_of_day = candle0['datetime'].hour
        hour_start = candle0['datetime']
        hour_end = hour_start + pd.Timedelta(hours=1)
        # Bullish strong close
        if candle1['close'] > candle2['high']:
            pivot = candle2['high']
            tp1 = candle0['open']
            tp2 = candle1['high']
            direction = 'bullish'
        # Bearish strong close
        elif candle1['close'] < candle2['low']:
            pivot = candle2['low']
            tp1 = candle0['open']
            tp2 = candle1['low']
            direction = 'bearish'
        else:
            continue
        # Get all 5-min candles in the test hour (candle0)
        mask = (five_min_df['datetime'] >= hour_start) & (five_min_df['datetime'] < hour_end)
        hour_5m = five_min_df[mask].reset_index(drop=True)
        if hour_5m.empty:
            continue
        # Find when (if) price hits the pivot, and in which segment
        pivot_hit_idx = None
        segment_idx = None
        for idx, row in hour_5m.iterrows():
            if row['low'] <= pivot <= row['high']:
                pivot_hit_idx = idx
                minute = row['datetime'].minute
                for s, (start, end) in enumerate(segments):
                    if start <= minute < end:
                        segment_idx = s
                        break
                break
        if pivot_hit_idx is None or segment_idx is None:
            continue
        if hour_of_day not in stats:
            stats[hour_of_day] = [{"total": 0, "tp1": 0, "tp2": 0} for _ in segments]
        stats[hour_of_day][segment_idx]["total"] += 1
        # Only count TP1/TP2 if hit after the pivot candle (not in the same candle)
        after_pivot = hour_5m.iloc[pivot_hit_idx + 1:]
        if not after_pivot.empty:
            if any((after_pivot['low'] <= tp1) & (after_pivot['high'] >= tp1)):
                stats[hour_of_day][segment_idx]["tp1"] += 1
            if any((after_pivot['low'] <= tp2) & (after_pivot['high'] >= tp2)):
                stats[hour_of_day][segment_idx]["tp2"] += 1
        event_count += 1
        if event_count % print_every == 0:
            print("\n--- Live Stats Table ---")
            print(_format_stats_table(stats, segment_labels))
    print("\n--- Final Stats Table ---")
    print(_format_stats_table(stats, segment_labels))
    # Output to CSV if requested
    if csv_output:
        _output_stats_to_csv(stats, segment_labels, csv_output)
        print(f"\nStats table saved to {csv_output}")
    return stats

def _format_stats_table(stats, segment_labels):
    # Aggregate stats for each (block_label, segment)
    agg = {}
    for block_label in stats:
        for seg_idx, seg in enumerate(segment_labels):
            key = (block_label, seg)
            s = stats[block_label][seg_idx]
            if key not in agg:
                agg[key] = {"total": 0, "tp1": 0, "tp2": 0}
            agg[key]["total"] += s["total"]
            agg[key]["tp1"] += s["tp1"]
            agg[key]["tp2"] += s["tp2"]
    rows = []
    for (block_label, seg) in sorted(agg.keys()):
        s = agg[(block_label, seg)]
        total = s["total"]
        tp1 = s["tp1"]
        tp2 = s["tp2"]
        tp1_pct = (tp1 / total * 100) if total else 0
        tp2_pct = (tp2 / total * 100) if total else 0
        rows.append([
            block_label, seg, total, tp1, f"{tp1_pct:.1f}%", tp2, f"{tp2_pct:.1f}%"
        ])
    headers = ["Hour", "Segment", "Pivot Hits", "TP1 Hits", "TP1 %", "TP2 Hits", "TP2 %"]
    return tabulate(rows, headers=headers, tablefmt="github")

def _output_stats_to_csv(stats, segment_labels, csv_output):
    # Aggregate stats for each (block_label, segment)
    agg = {}
    for block_label in stats:
        for seg_idx, seg in enumerate(segment_labels):
            key = (block_label, seg)
            s = stats[block_label][seg_idx]
            if key not in agg:
                agg[key] = {"total": 0, "tp1": 0, "tp2": 0}
            agg[key]["total"] += s["total"]
            agg[key]["tp1"] += s["tp1"]
            agg[key]["tp2"] += s["tp2"]
    rows = []
    for (block_label, seg) in sorted(agg.keys()):
        s = agg[(block_label, seg)]
        total = s["total"]
        tp1 = s["tp1"]
        tp2 = s["tp2"]
        tp1_pct = (tp1 / total * 100) if total else 0
        tp2_pct = (tp2 / total * 100) if total else 0
        rows.append([
            block_label, seg, total, tp1, tp1_pct, tp2, tp2_pct
        ])
    headers = ["Hour", "Segment", "Pivot Hits", "TP1 Hits", "TP1 %", "TP2 Hits", "TP2 %"]
    df = pd.DataFrame(rows, columns=headers)
    os.makedirs(os.path.dirname(csv_output), exist_ok=True)
    df.to_csv(csv_output, index=False)

def strong_4h_close_experiment(fourh_df: pd.DataFrame, five_min_df: pd.DataFrame, print_every: int = 10, csv_output: Optional[str] = None) -> Dict[str, Any]:
    """
    Same as strong_hourly_close_experiment, but uses 4h candles as input.
    Detects strong close on 4h candle and analyzes how 5m candles react at next 4h.
    Aggregates stats by hour of day (e.g., '08:00') and segment.
    """
    stats = {}
    segments = [(0, 59), (60, 119), (120, 179), (180, 239)]
    segment_labels = ["00–59", "60–119", "120–179", "180-239"]
    event_count = 0

    fourh_df = fourh_df.copy()
    five_min_df = five_min_df.copy()
    fourh_df['datetime'] = pd.to_datetime(fourh_df['datetime'])
    five_min_df['datetime'] = pd.to_datetime(five_min_df['datetime'])
    fourh_df = fourh_df.sort_values('datetime').reset_index(drop=True)
    five_min_df = five_min_df.sort_values('datetime').reset_index(drop=True)

    for i in range(2, len(fourh_df)):
        candle2 = fourh_df.iloc[i - 2]
        candle1 = fourh_df.iloc[i - 1]
        candle0 = fourh_df.iloc[i]
        block_start = candle0['datetime']
        block_end = block_start + pd.Timedelta(hours=4)
        # Use hour of day as key (e.g., '08:00')
        hour_of_day = block_start.strftime("%H:00")

        if candle1['close'] > candle2['high']:
            pivot = candle2['high']
            tp1 = candle0['open']
            tp2 = candle1['high']
            direction = 'bullish'
        elif candle1['close'] < candle2['low']:
            pivot = candle2['low']
            tp1 = candle0['open']
            tp2 = candle1['low']
            direction = 'bearish'
        else:
            continue

        mask = (five_min_df['datetime'] >= block_start) & (five_min_df['datetime'] < block_end)
        block_5m = five_min_df[mask].reset_index(drop=True)
        if block_5m.empty:
            continue

        pivot_hit_idx = None
        segment_idx = None
        for idx, row in block_5m.iterrows():
            if row['low'] <= pivot <= row['high']:
                pivot_hit_idx = idx
                minute_offset = int((row['datetime'] - block_start).total_seconds() // 60)
                for s, (start, end) in enumerate(segments):
                    if start <= minute_offset < end:
                        segment_idx = s
                        break
                break

        if pivot_hit_idx is None or segment_idx is None:
            continue

        if hour_of_day not in stats:
            stats[hour_of_day] = [{"total": 0, "tp1": 0, "tp2": 0} for _ in segments]
        stats[hour_of_day][segment_idx]["total"] += 1

        after_pivot = block_5m.iloc[pivot_hit_idx + 1:]
        if not after_pivot.empty:
            if any((after_pivot['low'] <= tp1) & (after_pivot['high'] >= tp1)):
                stats[hour_of_day][segment_idx]["tp1"] += 1
            if any((after_pivot['low'] <= tp2) & (after_pivot['high'] >= tp2)):
                stats[hour_of_day][segment_idx]["tp2"] += 1

        event_count += 1
        if event_count % print_every == 0:
            print("\n--- Live Stats Table ---")
            print(_format_stats_table(stats, segment_labels))

    print("\n--- Final Stats Table ---")
    print(_format_stats_table(stats, segment_labels))
    if csv_output:
        _output_stats_to_csv(stats, segment_labels, csv_output)
        print(f"\nStats table saved to {csv_output}")
    return stats

