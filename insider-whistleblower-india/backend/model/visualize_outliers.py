import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv(r"C:\Users\Archie\insider-whistleblower-india\insider-whistleblower-india\insider-whistleblower-india\backend\utils\merged_output.csv", parse_dates=["date"])

# Compute features
df["price_pct_change"] = (df["Close"] - df["Open"]) / df["Open"] * 100
df["vol_ma_5"] = df.groupby("SYMBOL")["Volume"].transform(lambda x: x.rolling(5, min_periods=1).mean())
df["vol_spike"] = df["Volume"] / df["vol_ma_5"]

# Flag anomalies
df["anomaly"] = ((abs(df["price_pct_change"]) > 5) & (df["vol_spike"] > 2))

# Interactive scatter plot
fig = px.scatter(
    df, 
    x="vol_spike", 
    y="price_pct_change",
    color="anomaly",
    symbol="anomaly",
    hover_data=["date", "SYMBOL", "Open", "Close", "Volume"],
    title="Interactive Volume Spike vs Price % Change",
)

# Add guideline shapes
fig.add_hline(y=5, line_dash="dash", line_color="green")
fig.add_hline(y=-5, line_dash="dash", line_color="green")
fig.add_vline(x=2, line_dash="dash", line_color="orange")

fig.update_layout(legend_title="Anomaly Flagged")
fig.show()

# Load insider/bulk data
INSIDER_FILE_ID = "1kpgPjxMCXjA7zw2qKr7jsONrMs0hHRXO"
BULK_FILE_ID = "1s3tcbLKhRA-qcTWfPdlpRRVe59zvjZEF"
insider = pd.read_csv(f"https://drive.google.com/uc?id={INSIDER_FILE_ID}&export=download")
bulk = pd.read_csv(f"https://drive.google.com/uc?id={BULK_FILE_ID}&export=download")

# Parse dates
insider.columns = insider.columns.str.strip()
bulk.columns = bulk.columns.str.strip()
insider['date'] = pd.to_datetime(insider['DATE OF ALLOTMENT/ACQUISITION FROM'], errors='coerce', dayfirst=True)
bulk['date'] = pd.to_datetime(bulk['Date'], errors='coerce', dayfirst=True)

# Flag insider/bulk match
df["insider_match"] = df.apply(
    lambda row: ((insider["SYMBOL"] == row["SYMBOL"]) & (insider["date"] == row["date"])).any(), axis=1
)

df["bulk_match"] = df.apply(
    lambda row: ((bulk["Symbol"] == row["SYMBOL"]) & (bulk["date"] == row["date"])).any(), axis=1
)

# Display anomalies with insider/bulk info
anomalies = df[df["anomaly"]]
print(anomalies[["date", "SYMBOL", "price_pct_change", "vol_spike", "insider_match", "bulk_match"]].head(10))

# Optionally save
anomalies.to_csv("flagged_anomalies_with_matches.csv", index=False)
print("✅ Flagged anomalies with insider/bulk matches saved to flagged_anomalies_with_matches.csv")
