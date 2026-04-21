import pandas as pd

def compute(df, period=10, multiplier=3):
    if df is None or df.empty:
        return {}

    hl2 = (df["High"] + df["Low"]) / 2
    atr = (df["High"] - df["Low"]).rolling(period).mean()

    upperband = hl2 + multiplier * atr
    lowerband = hl2 - multiplier * atr

    trend = df["Close"] > upperband

    return {
        "supertrend": int(trend.iloc[-1])
    }