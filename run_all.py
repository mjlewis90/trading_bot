#!/usr/bin/env python3
"""
run_all.py

Runs the full workflow:
1. Fetch market data
2. Fetch sentiment data
3. Generate features
4. Train model
5. Predict signals
6. Backtest predictions
7. Optionally visualize signals
"""

import subprocess
import sys

# List of core scripts to run in order
scripts = [
    "fetch_market_data.py",
    "fetch_sentiment_data.py",
    "generate_features.py",
    "train_model.py",
    "predict_signals.py",
    "backtest.py"
]

def run_script(script):
    print(f"\n🚀 Running: {script}\n{'-'*60}")
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        print(f"\n❌ {script} failed with exit code {result.returncode}. Aborting pipeline.")
        sys.exit(result.returncode)
    print(f"\n✅ {script} completed successfully.\n{'='*60}")

def main():
    print("🔄 Starting Trading Bot Full Workflow")
    for script in scripts:
        run_script(script)

    # Ask if user wants to visualize
    choice = input("\n🎨 Do you want to visualize the signals? (y/n): ").strip().lower()
    if choice == "y":
        start_date = input("Enter start date (YYYY-MM-DD) or leave blank for all dates: ").strip()
        end_date = input("Enter end date (YYYY-MM-DD) or leave blank for all dates: ").strip()

        cmd = [sys.executable, "visualize_signals.py"]
        if start_date:
            cmd += ["--start", start_date]
        if end_date:
            cmd += ["--end", end_date]

        print(f"\n📊 Launching visualization with parameters: {cmd}")
        result = subprocess.run(cmd)
        if result.returncode != 0:
            print(f"\n⚠️ visualize_signals.py failed with exit code {result.returncode}.")
        else:
            print("\n✅ Visualization completed.")

    print("\n🎉 All steps completed successfully.")

if __name__ == "__main__":
    main()
