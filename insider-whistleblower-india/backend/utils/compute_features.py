import pandas as pd
import numpy as np

# Load your merged CSV
df = pd.read_csv(r"C:\Users\Archie\insider-whistleblower-india\insider-whistleblower-india\insider-whistleblower-india\backend\utils\merged_output_with_features.csv", parse_dates=["date"])

# 🧹 CLEANUP START
df["Quantity Traded"] = df["Quantity Traded"].str.replace(",", "").astype(float)
df["vol_ma_5"] = df["vol_ma_5"].replace([np.inf, -np.inf], "null")
df["vol_spike"] = df["vol_spike"].replace([np.inf, -np.inf], "null")
df = df.fillna(value="null")
df["DATE OF ALLOTMENT/ACQUISITION TO"] = pd.to_datetime(df["DATE OF ALLOTMENT/ACQUISITION TO"], dayfirst=True, errors="coerce")
# 🧹 CLEANUP END

# Recompute features if needed
# Force numeric, invalid values become NaN
df["Open"] = pd.to_numeric(df["Open"], errors="coerce")
df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
df["Volume"] = pd.to_numeric(df["Volume"], errors="coerce")
df["price_pct_change"] = (df["Close"] - df["Open"]) / df["Open"] * 100
df["vol_ma_5"] = df.groupby("SYMBOL")["Volume"].transform(lambda x: x.rolling(5).mean())
df["vol_spike"] = df["Volume"] / df["vol_ma_5"]

# Save cleaned + feature-enhanced CSV
df.to_csv("merged_output_with_features.csv", index=False)
print("✅ Cleaned data saved successfully!")

