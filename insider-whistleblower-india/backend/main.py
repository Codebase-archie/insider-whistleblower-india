# backend/main.py
from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
import os

app = FastAPI(title="Insider Whistleblower Anomaly API")

CSV_PATH = r"C:\Users\Archie\insider-whistleblower-india\insider-whistleblower-india\insider-whistleblower-india\backend\utils\merged_output_with_features.csv"

def load_csv():
    if os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH)
    else:
        raise FileNotFoundError(f"CSV file not found at {CSV_PATH}")

@app.get("/alerts")
def get_alerts(
    request: Request,
    symbol: str = Query(...),
    start_date: str = Query(...),
    end_date: str = Query(...)
):
    # Logging
    print(f"Incoming request: symbol={symbol}, start={start_date}, end={end_date}")

    # Reload data
    df = load_csv()

    # Ensure datetime
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Filter
    filtered = df[
        (df["Symbol"] == symbol) &
        (df["date"] >= pd.to_datetime(start_date)) &
        (df["date"] <= pd.to_datetime(end_date))
    ]

    if filtered.empty:
        raise HTTPException(404, "No matching records found")

    # Clean infinities
    filtered = filtered.replace([np.inf, -np.inf], "null")

    # **Convert datetime to string** for JSON
    filtered["date"] = filtered["date"].dt.strftime("%Y-%m-%d")

    # Convert NaN → None
    filtered = filtered.where(pd.notnull(filtered), "null")

    # Return JSON
    return JSONResponse(content=filtered.to_dict(orient="records"))
