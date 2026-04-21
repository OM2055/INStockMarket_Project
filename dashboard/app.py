import streamlit as st
import pandas as pd

from components.charts import show_price_chart

st.set_page_config(layout="wide")

st.title("🚀 NSE AI Quant Dashboard")

# -------------------------
# LOAD DATA
# -------------------------
try:
    df = pd.read_csv("output/stocks.csv")
except Exception as e:
    st.error(f"Run pipeline first\n{e}")
    st.stop()

if df is None or df.empty:
    st.error("❌ No data available")
    st.stop()

# -------------------------
# CLEAN DATA
# -------------------------
df = df.dropna(how="all")

for col in ["price", "rsi", "dma50"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# -------------------------
# GENERATE SIGNALS
# -------------------------
def generate_signal(row):
    if row.get("rsi", 0) > 55 and row.get("price", 0) > row.get("dma50", 0):
        return "BUY"
    elif row.get("rsi", 0) < 45:
        return "SELL"
    else:
        return "HOLD"

df["signal"] = df.apply(generate_signal, axis=1)

# -------------------------
# COLOR FUNCTION
# -------------------------
def highlight_signal(row):
    if row["signal"] == "BUY":
        return ["background-color: #d4edda"] * len(row)
    elif row["signal"] == "SELL":
        return ["background-color: #f8d7da"] * len(row)
    else:
        return ["background-color: #fff3cd"] * len(row)

# -------------------------
# MARKET OVERVIEW
# -------------------------
st.subheader("🔥 Market Overview")

try:
    from st_aggrid import AgGrid, GridOptionsBuilder

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination()
    gb.configure_default_column(filter=True, sortable=True)

    AgGrid(df, gridOptions=gb.build(), height=350)

except:
    # fallback if AgGrid fails
    st.dataframe(df.style.apply(highlight_signal, axis=1), use_container_width=True)

# -------------------------
# BUY SIGNALS
# -------------------------
st.subheader("🚀 Buy Signals")

buy_df = df[df["signal"] == "BUY"]

if buy_df.empty:
    st.warning("No BUY signals found")
else:
    st.dataframe(buy_df.style.apply(highlight_signal, axis=1), use_container_width=True)

# -------------------------
# STOCK ANALYSIS
# -------------------------
st.subheader("🔍 Stock Analysis")

stock = st.selectbox("Select Stock", df["symbol"].unique())

if stock:
    row = df[df["symbol"] == stock].iloc[0]

    col1, col2, col3 = st.columns(3)

    col1.metric("Price", round(row.get("price", 0), 2))
    col2.metric("RSI", round(row.get("rsi", 0), 2))
    col3.metric("Signal", row.get("signal", "N/A"))

    # Indicators
    st.subheader("📊 Indicators")

    col4, col5, col6 = st.columns(3)

    col4.metric("MACD", round(row.get("macd", 0), 2))
    col5.metric("Signal", round(row.get("macd_signal", 0), 2))
    col6.metric("Supertrend", row.get("supertrend", "N/A"))

    # Chart
    show_price_chart(stock)

    # Full Data
    st.subheader("📦 Full Data")
    st.dataframe(pd.DataFrame(row).T, use_container_width=True)