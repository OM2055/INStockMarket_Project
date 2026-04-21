import yfinance as yf

def fetch_data(symbol):
    try:
        df = yf.download(symbol + ".NS", period="2y", interval="1d", progress=False)

        if df is None or df.empty:
            return None

        # 🔥 Flatten columns if multi-index
        if hasattr(df.columns, "levels"):
            df.columns = df.columns.get_level_values(0)

        df = df.dropna()

        return df

    except Exception as e:
        print(f"Fetch error {symbol}: {e}")
        return None