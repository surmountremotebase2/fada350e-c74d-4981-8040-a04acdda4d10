from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD, MA
from surmount.logging import log
import pandas as pd

class TradingStrategy(Strategy):
    def __init__(self):
        # Initialization parameters
        self.start_date = "2020-01-01"
        self.end_date = "2023-01-01"
        self.initial_cash = 100000
        self.symbol = "SPY"
        self.resolution = "1day"  # Assuming daily resolution is represented like this
        self.weekly_volumes = []
        
        # MACD indicator parameters
        self.fast_period = 12
        self.serror_period = 26
        self.signal_period = 9
        
        # LWMA indicator period (assuming surmount has an LWMA or this represents a generic MA with 'linear' type)
        self.MA_period = 55

    @property
    def assets(self):
        return [self.symbol]

    @property
    def interval(self):
        return self.resolution

    def run(self, data):
        # Ensure there's enough data for indicators
        if len(data["ohlcv"]) < max(self.fast_period, self.slow_period, self.lwma_period):
            return TargetAllocation({})
        
        # Prepare data for indicators
        closes = pd.Series([i[self.symbol]["close"] for i in data["ohlcv"]])

        # Computing MACD with the given parameters
        macd_vals = MACD(self.symbol, data["ohlcv"], self.fast_period, self.slow_period)
        
        # Computing 55-period LWMA
        lwma_vals = LWMA(self.symbol, data["ohlcv"], self.lwma_period)
        
        current_price = closes.iloc[-1]
        allocation = {}
        
        # Check for trade signals
        if macd_vals['MACD'][-1] > macd_vals['signal'][-1] and current_price > lwma_vals[-1]:
            # Entry condition met
            allocation[self.symbol] = 1.0
            log(f"Buying {self.symbol}")
        elif (macd_vals['MACD'][-1] < macd_vals['signal'][-1] or current_price < lwma_vals[-1]):
            # Exit condition met
            allocation[self.symbol] = 0
            log(f"Selling {self.symbol}")
        
        return TargetAllocation(allocation)

    def end_of_week_check(self):
        # Assuming there's a predefined method to access historical data
        # This method would ideally be scheduled to run weekly after market opening
        # and should populate the weekly_volumes list with the weekly summed volume.
        pass

    def calculate_weekly_volume(self, historical_data):
        # Assuming historical_data is a dataframe or a similar structure
        # This is a helper method, likely called within end_of_week_check
        weekly_volume = historical_data['volume'].resample('W').sum()
        self.weekly_volumes.append(weekly_volume)
        # Keeping only the last 5 weeks of data
        self.weekly_volumes = self.weekly_volumes[-5:]