import pandas as pd
import yfinance as yf
import os
import gc

# ─── CONFIG ─────────────────────────────────────────────────────────────────────
INSIDER_FILE = r"C:\Users\Archie\Documents\insider_whistleblower\insider_trading.csv"
BULK_FILE    = r"C:\Users\Archie\Documents\insider_whistleblower\bulk_deals.csv"
START_DATE   = "2024-06-20"
END_DATE     = "2025-06-20"

OHLC_CSV     = "all_ohlc.csv"
FINAL_CSV    = "merged_output.csv"
CHUNK_SIZE   = 200_000   # Adjust to your available RAM

# ─── 1) LOAD & CLEAN INSIDER + BULK ────────────────────────────────────────────
print("🔹 Loading insider trading data...")
insider = pd.read_csv(INSIDER_FILE).rename(columns=str.strip)
insider['date']   = pd.to_datetime(
    insider.pop('DATE OF ALLOTMENT/ACQUISITION FROM'),
    errors='coerce', dayfirst=True
)
insider['SYMBOL'] = insider['SYMBOL'].str.strip()
print(f"✅ Insider rows: {len(insider)}")

print("🔹 Loading bulk deals data...")
bulk = pd.read_csv(BULK_FILE).rename(columns=str.strip)
bulk['date']      = pd.to_datetime(
    bulk.pop('Date'),
    errors='coerce', dayfirst=True
)
bulk['SYMBOL']    = bulk['Symbol'].str.strip()
print(f"✅ Bulk rows: {len(bulk)}")

# ─── 2) BUILD SYMBOL LIST BEFORE MERGE ─────────────────────────────────────────
symbols = pd.concat([insider['SYMBOL'], bulk['SYMBOL']]) \
            .dropna().unique().tolist()
print(f"🔹 Will fetch OHLC for {len(symbols)} symbols")

# ─── 3) PRE‐MERGE INSIDER + BULK ───────────────────────────────────────────────
print("🔹 Pre‐merging insider + bulk...")
ib = pd.merge(insider, bulk, on="date", how="outer", suffixes=("_insider","_bulk"))

# Unify symbol column
ib['SYMBOL'] = ib['SYMBOL_insider'].combine_first(ib['SYMBOL_bulk']).str.strip()
print(f"✅ Insider+Bulk combined rows: {len(ib)}")

# Build set of valid keys for filtering
ib_keys = set(zip(ib['date'], ib['SYMBOL']))

# ─── 4) FETCH & WRITE OHLC TO DISK ─────────────────────────────────────────────
if os.path.exists(OHLC_CSV):
    os.remove(OHLC_CSV)

print("🔹 Fetching OHLC and writing to disk...")
header_written = False
for sym in symbols:
    yf_sym = f"{sym}.NS"
    df = yf.download(yf_sym, start=START_DATE, end=END_DATE, interval="1d", progress=False)
    if df.empty or df.isna().all().all():
        print(f"  ⚠️ Skipping {yf_sym}")
        continue

    # Bring Date into columns
    df = df.reset_index()

    # Add SYMBOL column
    df['SYMBOL'] = sym

    # Select only the needed columns
    df = df[['Date','Open','High','Low','Close','Volume','SYMBOL']]

    # Write or append to CSV
    mode = 'w' if not header_written else 'a'
    df.to_csv(OHLC_CSV, mode=mode, index=False, header=not header_written)
    header_written = True

    del df
    gc.collect()
    print(f"  ✅ Wrote OHLC for {yf_sym}")

if not header_written:
    print("❌ No OHLC data fetched—exiting.")
    exit()

# ─── 5) STREAM‐MERGE & WRITE OUTPUT ────────────────────────────────────────────
if os.path.exists(FINAL_CSV):
    os.remove(FINAL_CSV)

print("🔹 Streaming merge in chunks...")
matched_keys = set()

for chunk in pd.read_csv(OHLC_CSV, parse_dates=['Date'], chunksize=CHUNK_SIZE):
    # Rename Date for merge
    chunk = chunk.rename(columns={'Date':'date'})

    # Filter by keys to reduce merge workload
    chunk['__key'] = list(zip(chunk['date'], chunk['SYMBOL']))
    chunk = chunk[chunk['__key'].isin(ib_keys)]
    if chunk.empty:
        continue

    # Track matched keys
    matched_keys.update(chunk['__key'].tolist())
    chunk.drop(columns='__key', inplace=True)

    # Inner merge to get only matching rows
    merged_chunk = pd.merge(
        ib, chunk,
        on=['date','SYMBOL'], how='inner'
    )

    # Append to final CSV
    mode = 'w' if not os.path.exists(FINAL_CSV) else 'a'
    merged_chunk.to_csv(FINAL_CSV, mode=mode, index=False, header=(mode=='w'))

    print(f"  • Processed {len(chunk)} OHLC rows → wrote {len(merged_chunk)} merged rows")
    del chunk, merged_chunk
    gc.collect()

# ─── 6) APPEND UNMATCHED INSIDER+​​BULK ROWS ────────────────────────────────────
print("🔹 Appending unmatched insider+bulk rows...")
ib['__key'] = list(zip(ib['date'], ib['SYMBOL']))
unmatched = ib[~ib['__key'].isin(matched_keys)].drop(
    columns=['SYMBOL_insider','SYMBOL_bulk','__key']
)
if not unmatched.empty:
    unmatched.to_csv(FINAL_CSV, mode='a', index=False, header=False)
    print(f"  ✅ Appended {len(unmatched)} unmatched rows")

print(f"🎯 Done! Final merged file: {FINAL_CSV}")
