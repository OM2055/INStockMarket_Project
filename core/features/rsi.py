import pandas as pd

def compute(df, period=14):
    if df is None or df.empty:
        return {}

    delta = df["Close"].diff()

    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    return {"rsi": float(rsi.iloc[-1])}