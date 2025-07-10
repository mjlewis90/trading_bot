import pandas as pd

df = pd.read_csv("./data/raw/SPY_20250709_172547.csv", index_col=0)
print(df.head())
print("\nIndex name:", df.index.name)

