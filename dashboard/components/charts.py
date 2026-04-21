import streamlit as st
import pandas as pd
import os

def show_price_chart(stock):
    st.subheader("📈 Price Chart")

    file_path = f"output/history/{stock}.csv"

    if not os.path.exists(file_path):
        st.warning(f"No history found for {stock}")
        return

    try:
        df = pd.read_csv(file_path)

        if df.empty or "Close" not in df.columns:
            st.warning("Invalid chart data")
            return

        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date")

        st.line_chart(df.set_index("Date")["Close"])

    except Exception as e:
        st.error(f"Chart error: {e}")