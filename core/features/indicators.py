def compute(df):
    close = df["Close"]

    delta = close.diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = -delta.clip(upper=0).rolling(14).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    ema12 = close.ewm(span=12).mean()
    ema26 = close.ewm(span=26).mean()

    macd = ema12 - ema26
    signal = macd.ewm(span=9).mean()

    return {
        "rsi": float(rsi.iloc[-1]),
        "macd": float(macd.iloc[-1]),
        "macd_signal": float(signal.iloc[-1]),
    }