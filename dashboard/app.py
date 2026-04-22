import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import time

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

df = df.dropna(how="all")

# -------------------------
# SIGNALS
# -------------------------
def generate_signal(row):
    if row.get("rsi", 0) > 55 and row.get("price", 0) > row.get("dma50", 0):
        return "BUY"
    elif row.get("rsi", 0) < 45:
        return "SELL"
    return "HOLD"

df["signal"] = df.apply(generate_signal, axis=1)

# -------------------------
# INDEX SYMBOLS (VALID ONLY)
# -------------------------
index_map = {
    "Nifty 50": "^NSEI",
    "Bank Nifty": "^NSEBANK",
    "Nifty IT": "^CNXIT",
    "Nifty FMCG": "^CNXFMCG",
    "Nifty Auto": "^CNXAUTO"
}

# -------------------------
# GET TRADING DAYS
# -------------------------
def get_trading_days(n=5):
    days = []
    current = datetime.today()

    while len(days) < n:
        if current.weekday() < 5:
            days.append(current.date())
        current -= timedelta(days=1)

    return sorted(days, reverse=True)

# =========================================================
# LAYOUT (2x3)
# =========================================================

# -------- ROW 1 --------
col1, col2 = st.columns(2)

# =========================
# MARKET HIGHLIGHT (FIXED)
# =========================
with col1:
    st.subheader("📊 Market Highlight")

    trading_days = get_trading_days(5)

    selected_day = st.selectbox(
        "Select Trading Day",
        trading_days,
        format_func=lambda x: x.strftime("%d-%B-%Y (%A)")
    )

    data_rows = []

    for name, symbol in index_map.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(
                start=selected_day,
                end=selected_day + timedelta(days=1)
            )

            if not hist.empty:
                high = float(hist["High"].iloc[0])
                low = float(hist["Low"].iloc[0])
            else:
                high = None
                low = None

        except:
            high = None
            low = None

        data_rows.append({
            "Index": name,
            "Low": low,
            "High": high
        })

    market_df = pd.DataFrame(data_rows)

    st.dataframe(market_df, width="stretch")


# =========================
# TOP SIGNALS
# =========================
with col2:
    st.subheader("📈 Top Signals")

    st.markdown("**🟢 BUY**")
    st.dataframe(df[df["signal"]=="BUY"].head(10), width="stretch")

    st.markdown("**🔴 SELL**")
    st.dataframe(df[df["signal"]=="SELL"].head(10), width="stretch")


st.markdown("---")

# -------- ROW 2 --------
col3, col4 = st.columns(2)

# Analysis
with col3:
    st.subheader("🔍 Analysis")

    stock = st.selectbox("Select Stock", df["symbol"].unique())

    if stock:
        row = df[df["symbol"] == stock].iloc[0]

        st.metric("Price", round(row.get("price", 0), 2))
        st.metric("RSI", round(row.get("rsi", 0), 2))
        st.metric("Signal", row.get("signal"))

# Price Chart
with col4:
    st.subheader("📊 Price Chart")

    chart_stock = st.selectbox("Select Stock", df["symbol"].unique(), key="chart")

    if chart_stock:
        try:
            ticker = yf.Ticker(f"{chart_stock}.NS")
            hist = ticker.history(period="3mo")

            if not hist.empty:
                st.line_chart(hist["Close"])
            else:
                st.info("No chart data")
        except:
            st.error("Chart error")


st.markdown("---")

# -------- ROW 3 --------
col5, col6 = st.columns(2)

# Full Data
with col5:
    st.subheader("📦 Full Data")
    st.dataframe(df, width="stretch")

# News
with col6:
    st.subheader("📰 Smart News")

    news_stock = st.selectbox("Select Stock", df["symbol"].unique(), key="news")

    if news_stock:
        try:
            ticker = yf.Ticker(f"{news_stock}.NS")
            news = ticker.news

            cutoff = datetime.now() - timedelta(days=30)

            if news:
                for item in news[:10]:
                    ts = item.get("providerPublishTime")
                    if not ts:
                        continue

                    news_date = datetime.fromtimestamp(ts)
                    if news_date < cutoff:
                        continue

                    st.markdown(f"**{item.get('title','')}**")
                    st.markdown(f"[Read more]({item.get('link','#')})")
                    st.markdown("---")
            else:
                st.info("No news")

        except:
            st.error("News error")