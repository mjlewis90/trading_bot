#!/usr/bin/env python3
"""
run_all.py

Runs the full trading bot pipeline in order:
1. fetch_market_data.py
2. fetch_sentiment_data.py
3. generate_features.py
4. train_model.py
5. predict_signals.py
6. backtest.py
7. visualize_signals.py (optional)

Includes:
- cleanup of old outputs
- config loading from config.yaml
- logging
"""

import os
import subprocess
import sys
import shutil
import yaml
from datetime import datetime
from rich.console import Console

console = Console()


def clean_output_dirs():
    for folder in ["./data/processed", "./signals", "./models"]:
        shutil.rmtree(folder, ignore_errors=True)
        os.makedirs(folder, exist_ok=True)
    console.print("[green]✅ Output directories cleaned.[/green]")


def run_script(script, extra_args=None):
    """
    Run a Python script as a subprocess.
    """
    cmd = [sys.executable, script]
    if extra_args:
        cmd += extra_args
    console.print(f"\n🚀 [bold yellow]Running:[/bold yellow] {script}")
    console.print("------------------------------------------------------------")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        console.print(f"[red]❌ {script} failed. Exiting.[/red]")
        sys.exit(1)
    console.print(f"\n✅ [green]{script} completed successfully.[/green]")
    console.print("=" * 60)


def load_config():
    if not os.path.exists("config.yaml"):
        console.print("[red]❌ config.yaml not found. Please create it.[/red]")
        sys.exit(1)
    with open("config.yaml") as f:
        config = yaml.safe_load(f)
    return config


def main():
    console.print("\n🔄 [bold cyan]Starting BIG MIKE's Trading Bot Full Workflow[/bold cyan]\n")

    # Clean output folders
    clean_output_dirs()

    # Load configuration
    config = load_config()
    start_date = config.get("start_date", "")
    end_date = config.get("end_date", "")
    min_prob = config.get("min_probability", "0.5")

    # Run all pipeline steps
    run_script("fetch_market_data.py")
    run_script("fetch_sentiment_data.py")
    run_script("generate_features.py")
    run_script("train_model.py")
    run_script("predict_signals.py")
    run_script("backtest.py")

    # Optionally run visualization
    console.print("\n🎨 Do you want to visualize the signals? (y/n): ", end="")
    choice = input().strip().lower()
    if choice == "y":
        console.print("Enter start date (YYYY-MM-DD) or leave blank for all dates:", end=" ")
        vis_start = input().strip()
        console.print("Enter end date (YYYY-MM-DD) or leave blank for all dates:", end=" ")
        vis_end = input().strip()

        viz_args = []
        if vis_start:
            viz_args += ["--start", vis_start]
        if vis_end:
            viz_args += ["--end", vis_end]

        console.print(
            f"\n📊 Launching visualization with parameters: {viz_args if viz_args else '(no filters)'}"
        )
        run_script("visualize_signals.py", viz_args)
    else:
        console.print("\n👍 Skipping visualization.\n")

    # Summarize run
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    with open("run_summary.txt", "w") as f:
        f.write(f"Run completed at {timestamp}\n")
        f.write(f"Min probability threshold: {min_prob}\n")
        f.write(f"Date range: {start_date or 'ALL'} to {end_date or 'ALL'}\n")

    console.print(
        "\n✅ [bold green]All steps completed successfully. Run summary saved to run_summary.txt.[/bold green]\n"
    )


if __name__ == "__main__":
    main()
