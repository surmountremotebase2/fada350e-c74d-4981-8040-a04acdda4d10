from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log
import pandas as pd

class TradingStrategy(Strategy):
    def __init__(self):
        # List of tickers involved in this strategy
        self.tickers = ["TQQQ", "BIL", "QQQ"]
        self.buy_signal = False
        self.hold_days = 0

    @property
    def interval(self):
        # Defines the frequency of data updates
        return "1day"

    @property
    def assets(self):
        # Defines which assets are relevant for this strategy
        return self.tickers

    def IBS(self, close, high, low):
        """Calculate the Internal Bar Strength (IBS)."""
        return (close - low) / (high - low)
    
    def run(self, data):
        # Initialize TQQQ allocation to 0, and BIL (assumed safe asset) allocation to 1
        allocation = {"TQQQ": 0, "BIL": 1}

        # Assuming data["ohlcv"] is a DataFrame. Adjusting for given data structure
        spy_ohlcv = data["ohlcv"]["QQQ"]

        # Ensure we have at least two days of data for SPY to compare
        if len(spy_ohlcv) >= 2:
            # Define "yesterday" and "today" based on the latest two data points
            yesterday = spy_ohlcv.iloc[-2]
            today = spy_ohlcv.iloc[-1]
            today_date = pd.to_datetime(today['date'])

            # Date condition for special handling (Dec 20 - Jan 6)
            if today_date.month == 12 and today_date.day >= 20 or today_date.month == 1 and today_date.day <= 6:
                # Log and reset signals around year-end
                self.buy_signal = False
                self.hold_days = 0
                
            elif today_date.weekday() == 0:  # 0 represents Monday
                ibs_today = self.IBS(today['close'], today['high'], today['low'])
                # Buy signal conditions not related to the special date range
                if today['close'] < yesterday['close'] and ibs_today < 0.5:
                    self.buy_signal = True

            # Execution of buy or hold signals depending on conditions
            if self.buy_signal:
                if self.hold_days >= 7 or today['close'] > yesterday['high']:
                    # Sell signal: reset state and adjust allocation
                    self.buy_signal = False
                    self.hold_days = 0
                else:
                    # Holding strategy
                    allocation = {"TQQQ": 1, "BIL": 0}
                    self.hold_days += 1

            if self.buy_signal and self.hold_days == 0:
                # Initial buy action
                allocation = {"TQQQ": 1, "BIL": 0}
                self.hold_days = 1

        return TargetAllocation(allocation)