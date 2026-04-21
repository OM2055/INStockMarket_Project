from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
from core.data_fetcher import fetch_data
from core.feature_engine import compute_all


def process(symbol):
    try:
        df = fetch_data(symbol)

        if df is None or df.empty:
            print(f"❌ No data: {symbol}")
            return None

        features = compute_all(df, symbol)

        # 🔥 CRITICAL FIX: validate features
        if not features or not isinstance(features, dict):
            print(f"❌ Empty features: {symbol}")
            return None

        # Optional: ensure at least price exists
        if "price" not in features:
            print(f"❌ Missing price: {symbol}")
            return None

        print(f"✅ Success: {symbol}")
        return features

    except Exception as e:
        print(f"🔥 ERROR in {symbol}: {e}")
        return None


def run(symbols):
    results = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(process, s): s for s in symbols}

        for future in as_completed(futures):
            symbol = futures[future]

            try:
                res = future.result()

                # 🔥 STRICT CHECK before append
                if res and isinstance(res, dict) and len(res) > 0:
                    results.append(res)
                else:
                    print(f"⚠️ Skipped: {symbol}")

            except Exception as e:
                print(f"🔥 Future error {symbol}: {e}")

    df = pd.DataFrame(results)

    print("\n📊 FINAL SCAN RESULT")
    print("COLUMNS:", df.columns)
    print("ROWS:", len(df))

    return df