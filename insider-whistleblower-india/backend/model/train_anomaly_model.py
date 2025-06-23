import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

# Load your merged data
df = pd.read_csv(r"C:\Users\Archie\insider-whistleblower-india\insider-whistleblower-india\insider-whistleblower-india\backend\utils\merged_output.csv", parse_dates=["date"])

# Feature engineering
df["price_pct_change"] = (df["Close"] - df["Open"]) / df["Open"] * 100
df["vol_ma_5"] = df.groupby("SYMBOL")["Volume"].transform(lambda x: x.rolling(5, min_periods=1).mean())
df["vol_spike"] = df["Volume"] / df["vol_ma_5"]

# Drop rows with NaN in features (e.g., first few rows without rolling mean)
features = df[["price_pct_change", "vol_spike"]].dropna()

# Train IsolationForest
print("🔹 Training IsolationForest...")
model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
model.fit(features)

# Create backend/model directory if not exists
os.makedirs("backend/model", exist_ok=True)

# Save model
model_path = "backend/model/anomaly_model.joblib"
joblib.dump(model, model_path)

print(f"✅ Model saved to {model_path}")
