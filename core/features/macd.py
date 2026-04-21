def compute(df):
    if df is None or df.empty:
        return {}

    ema12 = df["Close"].ewm(span=12).mean()
    ema26 = df["Close"].ewm(span=26).mean()

    macd = ema12 - ema26
    signal = macd.ewm(span=9).mean()

    return {
        "macd": float(macd.iloc[-1]),
        "macd_signal": float(signal.iloc[-1])
    }