def compute(df):
    df["dma50"] = df["Close"].rolling(50).mean()
    df["dma200"] = df["Close"].rolling(200).mean()

    latest = df.iloc[-1]

    return {
     "dma50": float(latest["dma50"]),
     "dma200": float(latest["dma200"]),
    }