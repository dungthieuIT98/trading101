import numpy as np
import pandas as pd


class Indicator:

    def __init__(self, df: pd.DataFrame):

        self.df = df.copy()
    @staticmethod
    def ema(series: pd.Series, period: int) -> pd.Series:
        return series.ewm(span=period, min_periods=period, adjust=False).mean()
    @staticmethod
    def rsi(series: pd.Series, period: int = 14) -> pd.Series:
        delta = series.diff().to_numpy()
        up = np.where(delta > 0, delta, 0)
        down = np.where(delta < 0, -delta, 0)
        ma_up = pd.Series(up).ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
        ma_down = pd.Series(down).ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
        rs = ma_up / ma_down
        rsi = 100 - 100 / (1 + rs)
        rsi[:period] = np.nan
        return rsi
    @staticmethod
    def macd(series: pd.Series, fast=12, slow=26, signal=9):
        fast_ema = series.ewm(span=fast, min_periods=fast, adjust=False).mean()
        slow_ema = series.ewm(span=slow, min_periods=slow, adjust=False).mean()
        macd_line = fast_ema - slow_ema
        signal_line = macd_line.ewm(span=signal, min_periods=signal, adjust=False).mean()
        hist = macd_line - signal_line
        macd_line[:slow] = np.nan
        signal_line[:slow+signal-1] = np.nan
        hist[:slow+signal-1] = np.nan
        return macd_line, signal_line, hist

    # =========================
    #         BOLLINGER
    # =========================

    @staticmethod
    def bollinger(series: pd.Series, period=20, dev=2):
        ma = series.rolling(period, min_periods=period).mean()
        std = series.rolling(period, min_periods=period).std()
        upper = ma + dev * std
        lower = ma - dev * std
        ma[:period] = np.nan
        upper[:period] = np.nan
        lower[:period] = np.nan
        return ma, upper, lower

    # =========================
    #     MAIN RUNNER
    # =========================

    def compute_all(self) -> pd.DataFrame:
        df = self.df

        # RSI
        df["rsi_12"] = self.rsi(df["close"], 12)
        df["rsi_24"] = self.rsi(df["close"], 24)
        # MACD
        df["macd"], df["macd_signal"], df["macd_hist"] = self.macd(df["close"])

        # Moving Averages
        df["ema_20"] = self.ema(df["close"], 20)
        df["ema_50"] = self.ema(df["close"], 50)
        df['ema_90'] = self.ema(df['close'], 90)

        # Bollinger Bands
        df["bb_mid"], df["bb_upper"], df["bb_lower"] = self.bollinger(df["close"])
        return df
