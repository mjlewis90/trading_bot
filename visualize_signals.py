#!/usr/bin/env python3
"""
visualize_signals.py

Plots trading signals over time with optional date filtering.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import argparse
import glob
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="Visualize trading signals.")
    parser.add_argument("--file", type=str, help="CSV file with signals")
    parser.add_argument("--start", type=str, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, help="End date (YYYY-MM-DD)")
    args = parser.parse_args()

    # Automatically pick latest signals file if --file not specified
    if args.file:
        signals_file = args.file
    else:
        files = sorted(glob.glob("./signals/signals_*.csv"))
        if not files:
            print("❌ No signals CSV files found in ./signals/. Exiting.")
            return
        signals_file = files[-1]
        print(f"Auto-selected most recent signals file: {signals_file}")

    print(f"Loading: {signals_file}")
    df = pd.read_csv(signals_file)

    # Convert 'date' to datetime
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    # Apply date filtering if specified
    if args.start:
        start_date = pd.to_datetime(args.start)
        df = df[df["date"] >= start_date]
        print(f"Filtering from {start_date.date()}...")
    if args.end:
        end_date = pd.to_datetime(args.end)
        df = df[df["date"] <= end_date]
        print(f"Filtering to {end_date.date()}...")

    if df.empty:
        print("No data to plot after filtering.")
        return

    # Separate bullish and bearish signals
    bullish = df[df["prediction"] == 1]
    bearish = df[df["prediction"] == 0]

    fig, ax1 = plt.subplots(figsize=(14, 8))

    ax1.plot(df["date"], df["Close"], label="Close Price", color="black", linewidth=1)

    ax1.scatter(bullish["date"], bullish["Close"], marker="^", color="green", label="Bullish Signal")
    ax1.scatter(bearish["date"], bearish["Close"], marker="v", color="red", label="Bearish Signal")

    ax1.set_xlabel("Date")
    ax1.set_ylabel("Price")
    ax1.set_title("Trading Signals")

    # Rotate x-axis dates
    ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.xticks(rotation=45)

    ax1.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
