import pandas as pd
import numpy as np


def compute(df):
    data = {}

    try:
        if df is None or df.empty:
            return {}

        required = ["Close", "High", "Low", "Volume"]
        if not all(col in df.columns for col in required):
            return {}

        close = df["Close"]
        high = df["High"]
        low = df["Low"]
        volume = df["Volume"]

        # ==============================
        # 📊 MOVING AVERAGES
        # ==============================
        dma50 = close.rolling(50).mean()
        dma200 = close.rolling(200).mean()

        data["dma50"] = float(dma50.iloc[-1])
        data["dma200"] = float(dma200.iloc[-1])

        # ==============================
        # 🚀 MOMENTUM
        # ==============================
        momentum = close.pct_change(20)
        data["momentum"] = float(momentum.iloc[-1])

        # ==============================
        # 📉 RSI
        # ==============================
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        data["rsi"] = float(rsi.iloc[-1])

        # ==============================
        # 📊 MACD
        # ==============================
        ema12 = close.ewm(span=12).mean()
        ema26 = close.ewm(span=26).mean()
        macd = ema12 - ema26
        signal = macd.ewm(span=9).mean()

        data["macd"] = float(macd.iloc[-1])
        data["macd_signal"] = float(signal.iloc[-1])

        # ==============================
        # 📦 VOLUME + VVPAT (Proxy)
        # ==============================
        data["volume"] = float(volume.iloc[-1])
        data["volume_avg"] = float(volume.rolling(20).mean().iloc[-1])

        # VVPAT-style: price * volume (proxy accumulation)
        vwap_like = (close * volume).cumsum() / volume.cumsum()
        data["vvpat"] = float(vwap_like.iloc[-1])

        # ==============================
        # 📈 DMS (Directional Movement)
        # ==============================
        plus_dm = high.diff()
        minus_dm = low.diff() * -1

        plus_dm[plus_dm < 0] = 0
        minus_dm[minus_dm < 0] = 0

        tr = pd.concat([
            high - low,
            (high - close.shift()).abs(),
            (low - close.shift()).abs()
        ], axis=1).max(axis=1)

        atr = tr.rolling(14).mean()

        plus_di = 100 * (plus_dm.rolling(14).mean() / atr)
        minus_di = 100 * (minus_dm.rolling(14).mean() / atr)

        data["plus_di"] = float(plus_di.iloc[-1])
        data["minus_di"] = float(minus_di.iloc[-1])

        # ==============================
        # 🔥 SUPERTREND (IMPROVED)
        # ==============================
        period = 10
        multiplier = 3

        hl2 = (high + low) / 2
        atr = tr.rolling(period).mean()

        upperband = hl2 + (multiplier * atr)
        lowerband = hl2 - (multiplier * atr)

        supertrend = [True] * len(df)

        for i in range(1, len(df)):
            if close.iloc[i] > upperband.iloc[i - 1]:
                supertrend[i] = True
            elif close.iloc[i] < lowerband.iloc[i - 1]:
                supertrend[i] = False
            else:
                supertrend[i] = supertrend[i - 1]

        data["supertrend"] = int(supertrend[-1])

        return data

    except Exception as e:
        print("TECH ERROR:", e)
        return {}