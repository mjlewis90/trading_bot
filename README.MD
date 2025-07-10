# 🟢 Trading Bot (MVP)

This project is a **proof-of-concept trading bot** that demonstrates how to:

- Fetch and process market data
- Engineer trading features
- Train a machine learning model
- Generate trade signals
- Visualize and explore predictions interactively

The bot is designed around **S&P 500 price data**, CFTC Commitments of Traders (COT) reports, and AAII Sentiment Survey data. While currently focused on SPX/ETF indices, the design can be extended to other instruments in the future.

> **Note:**  
> This is a Minimum Viable Product (MVP). It is **not production-grade** and is for **educational and demonstration purposes only**.

---

## ✨ Features

✅ Download historical market data  
✅ Fetch COT and sentiment data  
✅ Generate engineered features (moving averages, volatility, sentiment spreads)  
✅ Train a Random Forest classifier to predict bullish/bearish signals  
✅ Export signals with prediction probabilities  
✅ Interactive command-line trade explorer  
✅ Visual signal plotting with `mplfinance`

---

## 🛠 Installation

Clone the repository:

git clone https://github.com/mjlewis90/trading_bot.git
cd trading_bot

Install dependencies (Python 3.12 recommended):
pip install -r requirements.txt

Or install manually
pip install pandas numpy scikit-learn matplotlib mplfinance rich joblib requests

(Optional) Install Git LFS if working with large models or data:
brew install git-lfs
git lfs install

## Workflow Overview

Below is a step-by-step workflow and description of each script:

# fetch_market_data.py
Description:
Downloads historical SPY and VIX price data via Yahoo Finance and saves CSVs in ./data/raw/.

Run:
python fetch_market_data.py

# fetch_sentiment_data.py
Description:
Fetches:

CFTC Commitments of Traders reports

AAII Sentiment Survey

Saves raw data and cleaned AAII CSVs.

Run:
python fetch_sentiment_data.py

# generate_features.py
Description:

Loads price data, COT data, and sentiment data

Computes moving averages, returns, volatility, net commercial positions, and bull-bear spreads

Merges into a unified feature dataset

Run: