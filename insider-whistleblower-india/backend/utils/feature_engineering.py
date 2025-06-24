import pandas as pd
import numpy as np

# Load CSV
df = pd.read_csv("merged_output.csv", parse_dates=["date"])

# Feature engineering
df["price_pct_change"] = (df["Close"] - df["Open"]) / df["Open"] * 100
df["vol_ma_5"] = df.groupby("SYMBOL")["Volume"].transform(lambda x: x.rolling(5).mean())
df["vol_spike"] = df["Volume"] / df["vol_ma_5"]

# Replace problematic values for JSON compliance
df = df.replace([np.inf, -np.inf], None)
df = df.where(pd.notnull(df), None)

# Print sample JSON-compliant output
print(df[["date", "SYMBOL", "price_pct_change", "vol_spike"]].head().to_dict(orient="records"))

# Save to CSV
df.to_csv("merged_output_with_features.csv", index=False)
print("✅ Saved merged_output_with_features.csv with new features.")
