st.subheader("📈 Smart Buy Signals")

signals = df[
    (df["rsi"] > 50) &
    (df["macd"] > df["macd_signal"]) &
    (df["supertrend"] == 1) &
    (df["plus_di"] > df["minus_di"]) &
    (df["volume"] > df["volume_avg"])
]

st.dataframe(signals)