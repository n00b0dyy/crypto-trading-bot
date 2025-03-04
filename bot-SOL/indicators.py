import pandas as pd
import ta

def calculate_moving_averages(df, short_period=50, long_period=100, ma_type="EMA"):
    """
    Oblicza dwie średnie kroczące:
    - short_period (np. 50)
    - long_period (np. 100)
    Można wybrać typ średniej: SMA, EMA, WMA, linreg (liniowa regresja)
    """
    if ma_type == "SMA":
        df["short_ma"] = df["close"].rolling(window=short_period).mean()
        df["long_ma"] = df["close"].rolling(window=long_period).mean()
    elif ma_type == "EMA":
        df["short_ma"] = ta.trend.EMAIndicator(df["close"], window=short_period).ema_indicator()
        df["long_ma"] = ta.trend.EMAIndicator(df["close"], window=long_period).ema_indicator()
    elif ma_type == "WMA":
        df["short_ma"] = ta.trend.WMAIndicator(df["close"], window=short_period).wma()
        df["long_ma"] = ta.trend.WMAIndicator(df["close"], window=long_period).wma()
    elif ma_type == "linreg":
        df["short_ma"] = df["close"].rolling(window=short_period).apply(lambda x: ta.trend.linear_regression(x, short_period))
        df["long_ma"] = df["close"].rolling(window=long_period).apply(lambda x: ta.trend.linear_regression(x, long_period))
    else:
        raise ValueError("Nieprawidłowy typ średniej kroczącej. Wybierz SMA, EMA, WMA lub linreg.")

    return df
