import streamlit as st

def show_signals(df):
    required_cols = ["rsi", "macd", "macd_signal", "supertrend"]

    for col in required_cols:
        if col not in df.columns:
            st.warning(f"Missing column: {col}")
            return

    signals = df[
        (df["rsi"] > 50) &
        (df["macd"] > df["macd_signal"]) &
        (df["supertrend"] == 1)
    ]

    st.subheader("🚀 Buy Signals")

    if signals.empty:
        st.info("No signals found")
    else:
        st.dataframe(signals, use_container_width=True)