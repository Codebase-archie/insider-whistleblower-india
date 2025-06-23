import pandas as pd

df = pd.read_csv("merged_output.csv", parse_dates=["date"])
df["price_pct_change"] = (df["Close"] - df["Open"]) / df["Open"] * 100
df["vol_ma_5"] = df.groupby("SYMBOL")["Volume"].transform(lambda x: x.rolling(5).mean())
df["vol_spike"] = df["Volume"] / df["vol_ma_5"]

print(df[["date","SYMBOL","price_pct_change","vol_spike"]].head())

# Optionally, save the enhanced data
df.to_csv("merged_output_with_features.csv", index=False)
print("✅ Saved merged_output_with_features.csv with new features.")
