#!/usr/bin/env python3
"""
Script: fetch_market_data.py
Purpose:
    - Download SPY, VIX, and Put/Call Ratio historical data
    - Save as timestamped CSVs
"""

import os
import pandas as pd
import yfinance as yf
from datetime import datetime, timezone 

# Create output directory
DATA_DIR = "./data/raw"
os.makedirs(DATA_DIR, exist_ok=True)

def fetch_yfinance_data(ticker, start_date="2015-01-01", end_date=None, interval="1d"):
    """
    Fetch historical data using yfinance
    Args:
        ticker (str): e.g., "SPY"
        start_date (str): format "YYYY-MM-DD"
        end_date (str): format "YYYY-MM-DD" or None
        interval (str): e.g., "1d"
    Returns:
        pd.DataFrame
    """
    print(f"Fetching {ticker} data...")
    data = yf.download(
        tickers=ticker,
        start=start_date,
        end=end_date,
        interval=interval,
        auto_adjust=False,
        progress=False
    )
    if data.empty:
        raise ValueError(f"No data returned for {ticker}")
    return data

def save_data(df, name_prefix):
    """
    Save DataFrame to CSV with timestamp
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = f"{DATA_DIR}/{name_prefix}_{timestamp}.csv"
    df.to_csv(filename)
    print(f"Saved: {filename}") 

def main():
    try:
        # Fetch SPY OHLCV
        spy_df = fetch_yfinance_data("SPY")
        save_data(spy_df, "SPY")

        # Fetch VIX
        vix_df = fetch_yfinance_data("^VIX")
        save_data(vix_df, "VIX")

        # Fetch Put/Call Ratio (CBOE)
        # Note: Yahoo Finance uses "^PCR" but often unavailable
        # Instead, as example, use VIX again or another proxy; you may swap to actual PCR data source later
        # Example uses VIX as placeholder
        # If you have a Put/Call dataset or other source, load it similarly
        # e.g., pcr_df = fetch_yfinance_data("^PCR")
        # save_data(pcr_df, "PutCallRatio")
        print("Note: Put/Call Ratio data requires a dedicated provider or custom data ingestion.")

    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    main()
