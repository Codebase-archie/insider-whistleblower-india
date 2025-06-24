# Insider Trading Pattern Detector + Whistleblower Dashboard (India Edition)

🚀 Project Summary
A machine learning-powered platform to detect anomalous insider trading patterns on Indian stock exchanges (NSE/BSE). It combines large trade data (bulk/block deals) with price movement data (Bhavcopy/yfinance) to flag suspicious activity. Includes a FastAPI backend and a React + Tailwind dashboard frontend.

⚡ Tech Stack
- **Backend:** FastAPI, scikit-learn, pandas
- **Frontend:** React, TailwindCSS, Recharts
- **ML:** IsolationForest for anomaly detection
- **Deployment:** Vercel (frontend), Render/Heroku (backend)

📊 Data Sources
- [NSE Bulk Deals](https://www.nseindia.com/report-detail/display-bulk-and-block-deals)
- [NSE Bhavcopy](https://www.nseindia.com/all-reports)
- [Insider Trading](https://www.nseindia.com/companies-listing/corporate-filings-insider-trading) 

📁 Folder Structure
```plaintext
insider-whistleblower-india/
├── backend/
│   ├── main.py
│   ├── model/
│   │   └── insider_anomaly_model.pkl
│   ├── utils/
│   │   └── merge_utils.py
│   ├── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadFile.js
│   │   │   ├── FlaggedTable.js
│   │   │   ├── TradeTimeline.js
│   │   ├── App.js
│   ├── public/
│   ├── package.json
│   ├── tailwind.config.js
│   ├── README.md
├── data/
│   ├── bulk_deals/
│   ├── bhavcopy/
│   └── merged_sample.csv
├── notebooks/
│   └── merge_and_model.ipynb
├── docs/
│   └── screenshots/
├── .gitignore
├── README.md

INSIDER_FILE_ID = "1kpgPjxMCXjA7zw2qKr7jsONrMs0hHRXO"
BULK_FILE_ID = "1s3tcbLKhRA-qcTWfPdlpRRVe59zvjZEF"