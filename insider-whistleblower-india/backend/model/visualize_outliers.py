import pandas as pd
import matplotlib.pyplot as plt
import joblib

# Load your merged dataset
df = pd.read_csv(r"C:\Users\Archie\insider-whistleblower-india\insider-whistleblower-india\insider-whistleblower-india\backend\utils\merged_output.csv", parse_dates=["date"])

# Recompute features if needed
df["price_pct_change"] = (df["Close"] - df["Open"]) / df["Open"] * 100
df["vol_ma_5"] = df.groupby("SYMBOL")["Volume"].transform(lambda x: x.rolling(5, min_periods=1).mean())
df["vol_spike"] = df["Volume"] / df["vol_ma_5"]

# Load the trained anomaly model
model = joblib.load("backend/model/anomaly_model.joblib")

# Predict anomalies
df["anomaly"] = model.predict(df[["price_pct_change", "vol_spike"]])

# Plot
plt.figure(figsize=(10, 6))
plt.scatter(df[df["anomaly"] == 1]["price_pct_change"],
            df[df["anomaly"] == 1]["vol_spike"],
            c='blue', alpha=0.5, label="Normal")

plt.scatter(df[df["anomaly"] == -1]["price_pct_change"],
            df[df["anomaly"] == -1]["vol_spike"],
            c='red', alpha=0.7, label="Outlier")

plt.xlabel("Price % Change")
plt.ylabel("Volume Spike")
plt.legend()
plt.title("Anomaly Detection: Outliers in Market Data")
plt.grid(True)
plt.show()
