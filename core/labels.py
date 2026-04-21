def create_target(df):
    df["future_return"] = df["Close"].shift(-50) / df["Close"] - 1
    return df["future_return"].iloc[-1]