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

---

## Workflow Overview

Below is a step-by-step workflow and description of each script:

### fetch_market_data.py

Description:  
Downloads historical SPY and VIX price data via Yahoo Finance and saves CSVs in ./data/raw/.

Run:
python fetch_market_data.py

### fetch_sentiment_data.py

Description:   
Fetches CFTC Commitments of Traders reports
AAII Sentiment Survey
Saves raw data and cleaned AAII CSVs.

Run:
python fetch_sentiment_data.py

### generate_features.py

Description:  
Loads price data, COT data, and sentiment data  
Computes moving averages, returns, volatility, net commercial positions, and bull-bear spreads  
Merges into a unified feature dataset  

Run:
python generate_features.py

Output:
./data/processed/features_<timestamp>.csv

### train_model.py

Description:  
Loads features  
Trains a Random Forest classifier to predict bullish/bearish signals  
Saves the trained model and feature names  

Run:
python train_model.py

Output:
Model artifact:  ./models/rf_model<timestamp>.joblib
Feature artifact: ./models/feature_names.txt

### predict_signals.py

Description:  
Loads the latest feature CSV and trained model  
Generates predicted signals and probabilities  
Saves signals to CSV  

Run:
python predict_signals.py

Output:
./signals/signals<timestamp>.csv

### cli_trading_bot.py

Description:  
Interactive command-line explorer  
Load signals and filter by:  
     Minimum prediction probability  
     Date ranges  
Inspect individual trade details  

Run:
python cli_trading_bot.py

### visualize_signals.py

Description:  
Plot historical price charts with bullish/bearish signals overlayed  
Optionally filter by date range  

Run:
python visualize_signals.py --start YYYY-MM-DD --end YYYY-MM-DD

Example:
python visualize_signals.py --start 2024-01-01 --end 2025-07-10


## Recommended Workflow

1  Fetch raw market and sentiment data  
2  Generate features  
3  Train the model  
4  Predict signals  
5  Explore signals via CLI and visualization  


## Functional Description

| Script                    | Purpose                                                  |
| ------------------------- | -------------------------------------------------------- |
| `fetch_market_data.py`    | Download SPY/VIX price data                              |
| `fetch_sentiment_data.py` | Fetch COT and AAII sentiment                             |
| `generate_features.py`    | Create merged feature set                                |
| `train_model.py`          | Train Random Forest model                                |
| `predict_signals.py`      | Generate predictions and probabilities                   |
| `cli_trading_bot.py`      | Interactive terminal exploration of signals              |
| `visualize_signals.py`    | Generate visual candlestick charts with signals overlaid |


## Future Improvements

This MVP can be extended in several ways:

✅ Integrate live data feeds (e.g., Interactive Brokers, Alpaca)
✅ Support arbitrary tickers beyond SPY (ORCL, AAPL, etc.)
✅ Add backtesting capability
✅ Automate daily retraining and signal generation
✅ Deploy as a web app or dashboard
✅ Incorporate additional features (macro indicators, earnings, options data)


## DISCLAIMER!!

This project is for educational demonstration only.
It should not be used for live trading or considered financial advice.


## License
MIT License


Enjoy exploring the data and let me know whats fucked up!
--Mike

