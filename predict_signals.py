#!/usr/bin/env python3
"""
predict_signals.py

Loads features and trained model, outputs predictions with probabilities.
"""

import pandas as pd
import glob
import os
from datetime import datetime, timezone
import joblib

DATA_DIR = "./data"
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
MODELS_DIR = "./models"
SIGNALS_DIR = "./signals"

def load_latest_model():
    files = sorted(glob.glob(os.path.join(MODELS_DIR, "rf_model_*.joblib")))
    if not files:
        raise Exception("No trained model found.")
    latest = files[-1]
    print(f"Loading: {latest}")
    return joblib.load(latest)

def load_feature_names():
    path = os.path.join(MODELS_DIR, "feature_names.txt")
    with open(path) as f:
        return [line.strip() for line in f.readlines()]

def load_latest_features():
    files = sorted(glob.glob(os.path.join(PROCESSED_DIR, "features_*.csv")))
    if not files:
        raise Exception("No features found.")
    latest = files[-1]
    print(f"Loading: {latest}")
    return pd.read_csv(latest, parse_dates=["date"])

def main():
    df = load_latest_features()
    model = load_latest_model()
    feature_names = load_feature_names()
    
    X = df[feature_names]
    preds = model.predict(X)
    probs = model.predict_proba(X)[:, 1]  # Probability of class 1
    
    df["prediction"] = preds
    df["probability"] = probs
    
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_path = os.path.join(SIGNALS_DIR, f"signals_{timestamp}.csv")
    df.to_csv(out_path, index=False)
    print(f"Signals saved to {out_path}")

if __name__ == "__main__":
    main()
