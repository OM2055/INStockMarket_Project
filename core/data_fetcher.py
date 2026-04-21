import yfinance as yf
import pandas as pd
import os

def fetch_data(symbol):
    try:
        df = yf.download(symbol + ".NS", period="1y", interval="1d")

        if df.empty:
            return None

        df.reset_index(inplace=True)

        # SAVE HISTORY
        os.makedirs("output/history", exist_ok=True)
        df.to_csv(f"output/history/{symbol}.csv", index=False)

        return df

    except Exception as e:
        print(f"Fetch error {symbol}: {e}")
        return None