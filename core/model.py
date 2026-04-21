from sklearn.ensemble import RandomForestRegressor

def train(df):
    if df is None or df.empty:
        raise ValueError("Empty dataframe — scanner failed")

    df = df.copy()

    if "target" not in df.columns:
        df["target"] = df["momentum"]

    X = df.drop(columns=["symbol", "target"], errors="ignore")
    X = X.select_dtypes(include=["number"]).fillna(0)

    y = df["target"].fillna(0)

    model = RandomForestRegressor(n_estimators=100, max_depth=5)
    model.fit(X, y)

    print("✅ Model trained")

    return model


def rank(df, model):
    X = df.drop(columns=["symbol", "target"], errors="ignore")
    X = X.select_dtypes(include=["number"]).fillna(0)

    df["score"] = model.predict(X)
    return df.sort_values(by="score", ascending=False)