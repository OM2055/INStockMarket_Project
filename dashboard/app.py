import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("🚀 NSE AI Quant Dashboard")

try:
    df = pd.read_csv("output/stocks.csv")
except:
    st.error("Run pipeline first")
    st.stop()

# Top Picks
st.subheader("🔥 Top 10 Stocks")
st.dataframe(df.head(10))

# Stock Selector
stock = st.selectbox("Select Stock", df["symbol"])

if stock:
    row = df[df["symbol"] == stock].iloc[0]

    col1, col2, col3 = st.columns(3)

    col1.metric("Price", round(row["price"], 2))
    col2.metric("RSI", round(row["rsi"], 2))
    col3.metric("Score", round(row["score"], 2))

    st.write("### Full Data")
    st.write(row)