#!/usr/bin/env python3
"""
backtest.py

Backtests the trading signals produced by predict_signals.py.
"""

import pandas as pd
import glob
import os
from datetime import datetime

# CONFIGURATION
SIGNALS_DIR = "./signals"
PROBABILITY_THRESHOLD = 0.70   # Only take trades with >= this probability
HOLD_DAYS = 5                  # How many days to hold each trade
TRANSACTION_COST = 0.001       # 0.1% per trade

def load_latest_signals():
    """Load the most recent signals CSV."""
    files = sorted(glob.glob(os.path.join(SIGNALS_DIR, "signals_*.csv")))
    if not files:
        raise Exception("No signals files found.")
    latest = files[-1]
    print(f"Loading signals from: {latest}")
    df = pd.read_csv(latest)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    return df

def main():
    df = load_latest_signals()

    results = []
    cumulative_return = 1.0
    profitable_trades = 0
    total_trades = 0

    for i in range(len(df) - HOLD_DAYS):
        row = df.iloc[i]

        # Skip if probability is too low
        if pd.isna(row["prediction"]) or row["probability"] < PROBABILITY_THRESHOLD:
            continue

        # Determine exit row
        exit_row = df.iloc[i + HOLD_DAYS]

        # Compute return: (exit - entry) / entry
        ret = (exit_row["Close"] - row["Close"]) / row["Close"]

        # If prediction == 0, assume bearish, inverse the return
        if row["prediction"] == 0:
            ret = -ret

        # Subtract transaction cost
        ret -= TRANSACTION_COST

        # Track cumulative return
        cumulative_return *= (1 + ret)

        # Count profitable trades
        if ret > 0:
            profitable_trades += 1

        total_trades += 1

        results.append({
            "entry_date": row["date"],
            "exit_date": exit_row["date"],
            "prediction": row["prediction"],
            "probability": row["probability"],
            "entry_close": row["Close"],
            "exit_close": exit_row["Close"],
            "return_pct": ret * 100
        })

    # Summarize results
    avg_return = (sum(r["return_pct"] for r in results) / len(results)) if results else 0
    cumulative_pct = (cumulative_return - 1) * 100 if results else 0
    win_rate = (profitable_trades / total_trades * 100) if total_trades > 0 else 0

    print("\n📈 Backtest Summary:")
    print(f"Total trades: {total_trades}")
    print(f"Profitable trades: {profitable_trades} ({win_rate:.2f}%)")
    print(f"Average return per trade: {avg_return:.2f}%")
    print(f"Cumulative return: {cumulative_pct:.2f}%")

    # Save detailed results
    out_df = pd.DataFrame(results)
    from datetime import timezone
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_path = os.path.join(SIGNALS_DIR, f"backtest_results_{timestamp}.csv")
    out_df.to_csv(out_path, index=False)
    print(f"\nDetailed results saved to {out_path}")

if __name__ == "__main__":
    main()
