from core.features import price
from core.features import technicals


def compute_all(df, symbol):
    data = {"symbol": symbol}

    data.update(price.compute(df))
    data.update(technicals.compute(df))

    return data