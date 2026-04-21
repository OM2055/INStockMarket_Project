import os
import pandas as pd
from engine.scanner import run
from core.model import train, rank

def load_symbols():
    try:
        df = pd.read_csv("data/symbols.csv")

        if "symbol" not in df.columns:
            raise ValueError("CSV must contain 'symbol' column")

        symbols = df["symbol"].dropna().unique().tolist()

        print(f"✅ Loaded {len(symbols)} symbols from CSV")
        return symbols

    except Exception as e:
        print(f"❌ Error loading symbols: {e}")
        return []


def main():
    symbols = load_symbols()

    if not symbols:
        print("❌ No symbols found")
        return

    df = run(symbols)

    print("ROWS:", len(df))
    print(df.head())

    if df.empty:
        print("❌ No data, exiting")
        return

    model = train(df)
    ranked = rank(df, model)

    os.makedirs("output", exist_ok=True)
    ranked.to_csv("output/stocks.csv", index=False)

    print("\n🔥 TOP STOCKS:")
    print(ranked.head())


if __name__ == "__main__":
    main()