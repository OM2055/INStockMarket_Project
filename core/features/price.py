def compute(df):
    if df is None or df.empty:
        return {}

    try:
        # 🔥 Fix multi-index columns (VERY IMPORTANT)
        if isinstance(df.columns, tuple) or hasattr(df.columns, "levels"):
            df.columns = df.columns.get_level_values(0)

        # Ensure columns exist
        required_cols = ["Close", "High", "Low"]
        for col in required_cols:
            if col not in df.columns:
                return {}

        # 🔥 Always extract scalar safely
        price = float(df["Close"].iloc[-1])
        high_52w = float(df["High"].tail(252).max())
        low_52w = float(df["Low"].tail(252).min())
        high_104w = float(df["High"].tail(504).max())
        low_104w = float(df["Low"].tail(504).min())

        return {
            "price": price,
            "high_52w": high_52w,
            "low_52w": low_52w,
            "high_104w": high_104w,
            "low_104w": low_104w,
        }

    except Exception as e:
        print("PRICE FEATURE ERROR:", e)
        return {}