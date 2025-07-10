#!/usr/bin/env python3

import os
import io
import zipfile
import requests
import pandas as pd
import datetime
from bs4 import BeautifulSoup

def fetch_cot_data():
    """
    Downloads and parses the COT disaggregated historical data.
    """
    url = "https://www.cftc.gov/files/dea/history/fut_disagg_txt_2024.zip"
    print("Fetching COT data (disaggregated historical ZIP)...")
    resp = requests.get(url)
    resp.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
        print("Contents of ZIP:", z.namelist())
        with z.open("f_year.txt") as f:
            # Read the first few lines to detect delimiter
            preview = f.read().decode("utf-8")
            f.seek(0)
            # CFTC uses comma delimiter but all headers quoted
            df = pd.read_csv(
                f,
                sep=",",
                engine="python"
            )

    print(f"Total rows in file: {len(df)}")

    # Clean column names if needed
    df.columns = [c.strip().replace('"','') for c in df.columns]
    if "Market_and_Exchange_Names" not in df.columns:
        raise Exception(
            f"Column 'Market_and_Exchange_Names' not found. Available columns:\n{df.columns}"
        )

    # Filter for S&P contracts if available
    sp_rows = df[df["Market_and_Exchange_Names"].str.contains("S&P", case=False, na=False)]
    if sp_rows.empty:
        print("⚠️ WARNING: No S&P contracts found. Saving all contracts instead.")
        sp_rows = df

    # Save CSV
    timestamp = datetime.datetime.now(datetime.UTC).strftime("%Y%m%d_%H%M%S")
    output = f"./data/raw/COT_{timestamp}.csv"
    os.makedirs(os.path.dirname(output), exist_ok=True)
    sp_rows.to_csv(output, index=False)
    print(f"Saved: {output}")
    return sp_rows

def fetch_aaii_sentiment():
    """
    Fetches AAII sentiment data and saves it as CSV.
    """
    url = "https://www.aaii.com/sentimentsurvey/sent_results"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.aaii.com/",
        "Connection": "keep-alive",
    }

    print("Fetching AAII sentiment data...")
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    html = resp.text

    # Save raw HTML for inspection
    timestamp = datetime.datetime.now(datetime.UTC).strftime("%Y%m%d_%H%M%S")
    fname = f"./data/raw/AAII_sentiment_html_{timestamp}.html"
    os.makedirs(os.path.dirname(fname), exist_ok=True)
    with open(fname, "w", encoding="utf-8") as f:
        f.write(html)

    soup = BeautifulSoup(html, "html.parser")
    # Try to find the first table
    table = soup.find("table")
    if not table:
        raise Exception(f"Could not locate sentiment table. HTML saved to {fname}.")

    rows = table.find_all("tr")
    records = []
    for row in rows[1:]:
        cols = row.find_all("td")
        if len(cols) != 4:
            continue
        date = cols[0].get_text(strip=True)
        bullish = cols[1].get_text(strip=True).replace("%","")
        neutral = cols[2].get_text(strip=True).replace("%","")
        bearish = cols[3].get_text(strip=True).replace("%","")
        records.append({
            "Date": date,
            "Bullish": float(bullish),
            "Neutral": float(neutral),
            "Bearish": float(bearish),
        })

    df = pd.DataFrame(records)
    output = f"./data/processed/AAII_sentiment_{timestamp}.csv"
    os.makedirs(os.path.dirname(output), exist_ok=True)
    df.to_csv(output, index=False)
    print(f"Saved: {output}")

def main():
    cot_df = fetch_cot_data()
    fetch_aaii_sentiment()

if __name__ == "__main__":
    main()
