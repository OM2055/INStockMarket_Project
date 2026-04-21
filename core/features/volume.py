def compute(df):
    return {
        "volume": float(df["Volume"].iloc[-1]),
        "avg_volume": float(df["Volume"].rolling(20).mean().iloc[-1]),
    }