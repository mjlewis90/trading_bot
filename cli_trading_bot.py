#!/usr/bin/env python3
"""
cli_trading_bot.py

Enhanced CLI with filtering, color-coded predictions, and export.
"""

import pandas as pd
import glob
import os
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich import box
from datetime import datetime, timezone

DATA_DIR = "./signals"

console = Console()

def load_latest_signal_file():
    files = sorted(glob.glob(os.path.join(DATA_DIR, "signals_*.csv")))
    if not files:
        console.print("[red]No signal files found.[/red]")
        exit(1)
    latest = files[-1]
    console.print(f"[cyan]Loading:[/cyan] {latest}")
    return pd.read_csv(latest)

def main():
    df = load_latest_signal_file()

    # Parse date
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    # Prompt for filters
    min_prob = Prompt.ask("Enter minimum probability threshold (e.g., 0.70)", default="0.50")
    min_prob = float(min_prob)

    min_date_str = Prompt.ask("Enter minimum date (YYYY-MM-DD) or leave blank for all dates", default="")
    if min_date_str:
        min_date = pd.to_datetime(min_date_str)
        df = df[df["date"] >= min_date]

    df = df[df["probability"] >= min_prob]

    if df.empty:
        console.print("[yellow]No signals matching filters.[/yellow]")
        return

    # Sort by probability
    df = df.sort_values("probability", ascending=False)

    console.rule("[bold green]📊 Trading Bot Overview")
    console.print(f"Loaded {len(df)} rows from {df['date'].min().date()} to {df['date'].max().date()}")
    console.print(f"Columns: {', '.join(df.columns)}")

    # Export filtered signals
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    export_path = os.path.join(DATA_DIR, f"filtered_signals_{timestamp}.csv")
    df.to_csv(export_path, index=False)
    console.print(f"[green]Filtered signals exported to [bold]{export_path}[/bold][/green]")

    # Display top 10 signals
    table = Table(show_header=True, header_style="bold magenta", box=box.SIMPLE_HEAVY)
    table.add_column("#", style="dim")
    table.add_column("Date")
    table.add_column("Prediction")
    table.add_column("Confidence")

    top_preds = df.head(10)
    for i, (_, row) in enumerate(top_preds.iterrows(), start=1):
        prob_str = f"{row['probability']*100:.2f}%"
        pred_color = "[green]Bullish[/green]" if int(row["prediction"]) == 1 else "[red]Bearish[/red]"

        table.add_row(
            str(i),
            row["date"].strftime("%Y-%m-%d"),
            pred_color,
            prob_str
        )

    console.print(table)

    while True:
        choice = Prompt.ask("Enter the trade # to view details (or 'q' to quit)", default="q")
        if choice.lower() == "q":
            break
        try:
            idx = int(choice) - 1
            if idx < 0 or idx >= len(top_preds):
                console.print("[yellow]Invalid selection.[/yellow]")
                continue
            row = top_preds.iloc[idx]
            console.rule(f"Details for {row['date'].strftime('%Y-%m-%d')}")
            console.print(row.to_frame())
        except ValueError:
            console.print("[yellow]Please enter a valid number.[/yellow]")

if __name__ == "__main__":
    main()
