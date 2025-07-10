#!/usr/bin/env python3
"""
generate_features.py

Loads market data, COT data, and AAII sentiment data,
merges them by date, and computes example features.
"""

import pandas as pd
import glob
import os
from datetime import datetime, timezone

DATA_DIR = "./data"
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")


def load_latest_csv(pattern):
    """Load the latest CSV file matching a pattern"""
    files = sorted(glob.glob(pattern))
    if not files:
        raise Exception(f"No files found for pattern: {pattern}")
    latest = files[-1]
    print(f"Loading: {latest}")
    return pd.read_csv(latest)


def load_price_data():
    """Load price data from SPY CSV with multi-row header handling"""
    spy_path = sorted(glob.glob(os.path.join(RAW_DIR, "SPY_*.csv")))[-1]
    print(f"Loading SPY data: {spy_path}")

    # Read first two rows to build column names
    header = pd.read_csv(spy_path, nrows=2, header=None)

    # Flatten multi-row header
    cols = []
    for i in range(header.shape[1]):
        top = str(header.iloc[0, i]).strip()
        bottom = str(header.iloc[1, i]).strip()
        if top == "nan":
            cols.append(bottom)
        elif bottom == "nan":
            cols.append(top)
        else:
            cols.append(f"{top}_{bottom}")

    # Load data skipping the first 2 header rows
    df = pd.read_csv(spy_path, skiprows=2, names=cols)

    # Remove any rows where first column is "Date" or empty
    df = df[df.iloc[:, 0].notnull()]
    df = df[df.iloc[:, 0] != "Date"]

    # Rename first column to "date"
    df = df.rename(columns={df.columns[0]: "date"})

    # Parse dates
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    # Rename Close_SPY to Close
    close_cols = [c for c in df.columns if "Close" in c]
    if not close_cols:
        raise Exception(f"No Close column found. Columns: {df.columns}")
    df = df.rename(columns={close_cols[0]: "Close"})

    return df


def load_cot_data():
    """Load the latest COT CSV"""
    df = load_latest_csv(os.path.join(RAW_DIR, "COT_*.csv"))
    if "Market_and_Exchange_Names" in df.columns:
        spx = df[df["Market_and_Exchange_Names"].str.contains("S&P", na=False)]
        if not spx.empty:
            df = spx
    df["Report_Date_as_YYYY-MM-DD"] = pd.to_datetime(df["Report_Date_as_YYYY-MM-DD"])
    return df


def load_aaii_data():
    """Load the latest AAII sentiment CSV"""
    df = load_latest_csv(os.path.join(PROCESSED_DIR, "AAII_sentiment_*.csv"))

    # Try to auto-detect date column
    date_cols = [c for c in df.columns if "date" in c.lower() or "Date" in c]
    if not date_cols:
        raise Exception(
            f"No date column found in AAII sentiment data. Available columns: {df.columns}"
        )
    date_col = date_cols[0]
    df["date"] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=["date"])

    # Standardize column names
    df = df.rename(
        columns={
            "Bullish": "bullish",
            "Bearish": "bearish",
            "Neutral": "neutral"
        }
    )
    return df


def compute_price_features(df):
    """Compute basic price-derived features"""
    df = df.sort_values("date").copy()
    df["return_1d"] = df["Close"].pct_change()
    df["ma_10"] = df["Close"].rolling(window=10).mean()
    df["ma_20"] = df["Close"].rolling(window=20).mean()
    df["volatility_10d"] = df["Close"].rolling(window=10).std()
    return df


def compute_cot_features(df):
    """Compute net commercial positions"""
    df["net_commercial"] = (
        df["Prod_Merc_Positions_Long_All"] - df["Prod_Merc_Positions_Short_All"]
    )
    cot_features = df[
        ["Report_Date_as_YYYY-MM-DD", "net_commercial"]
    ].rename(columns={"Report_Date_as_YYYY-MM-DD": "date"})
    return cot_features


def compute_aaii_features(df):
    """Compute bull-bear spread"""
    df["bull_bear_spread"] = df["bullish"] - df["bearish"]
    return df[["date", "bullish", "bearish", "neutral", "bull_bear_spread"]]


def main():
    price_df = load_price_data()
    cot_df = load_cot_data()
    aaii_df = load_aaii_data()

    price_df = compute_price_features(price_df)
    cot_features = compute_cot_features(cot_df)
    aaii_features = compute_aaii_features(aaii_df)

    # Merge all on date
    df = price_df.merge(cot_features, on="date", how="left")
    df = df.merge(aaii_features, on="date", how="left")

    # Drop rows without Close
    df = df.dropna(subset=["Close"])

    # Save output
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_path = os.path.join(PROCESSED_DIR, f"features_{timestamp}.csv")
    df.to_csv(out_path, index=False)
    print(f"Features saved to {out_path}")


if __name__ == "__main__":
    main()
