#!/usr/bin/env python3
"""
train_model.py

Loads feature dataset, trains RandomForestClassifier,
and saves model and feature metadata.
"""

import pandas as pd
import glob
import os
from datetime import datetime, timezone
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

DATA_DIR = "./data"
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
MODEL_DIR = "./models"


def load_latest_features():
    files = sorted(glob.glob(os.path.join(PROCESSED_DIR, "features_*.csv")))
    if not files:
        raise Exception("No feature files found.")
    latest = files[-1]
    print(f"Loading features: {latest}")
    return pd.read_csv(latest)


def main():
    df = load_latest_features()

    # Create target: 1 if next day's return > 0, else 0
    df["target"] = (df["return_1d"].shift(-1) > 0).astype(int)

    # Drop rows without target (last row)
    df = df.dropna(subset=["target"])

    # Split data
    X = df.drop(["date", "Close", "target"], axis=1).fillna(0)
    y = df["target"]

    # Save feature names
    feature_names = X.columns.tolist()
    os.makedirs(MODEL_DIR, exist_ok=True)
    with open(os.path.join(MODEL_DIR, "feature_names.txt"), "w") as f:
        for col in feature_names:
            f.write(col + "\n")
    print(f"Saved feature names to ./models/feature_names.txt")

    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Evaluate
    preds = model.predict(X)
    report = classification_report(y, preds)
    print("Classification Report:")
    print(report)

    # Save model
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_path = os.path.join(MODEL_DIR, f"rf_model_{timestamp}.joblib")
    joblib.dump(model, out_path)
    print(f"Model saved to {out_path}")


if __name__ == "__main__":
    main()
