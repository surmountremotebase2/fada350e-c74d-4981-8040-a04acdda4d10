from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD, EMA
from surmount.data import Asset
import pandas as pd
import numpy as np

class TradingStrategy(Strategy):
    def __init__(self):
        self.symbol = "SPY"
        self.fast_length = 12
        self.slow_length = 26
        self.signal_length = 9
        self.lwma_length = 55  # For LWMA, using EMA as a placeholder
        self.initial_cash = 100000  # This may not be directly utilizable here
        self.start_date = "2020-01-01"  # Placeholder for backtesting setup
        self.end_date = "2023-01-01"  # Placeholder for backtesting setup
        
    @property
    def assets(self):
        return [self.symbol]
    
    @property
    def interval(self):
        return "1day"  # Daily resolution

    def lwma_calculator(self, prices, period):
        """Calculate the LWMA or use EMA if LWMA is not available.
        (This example falls back to EMA for demonstration.)
        """
        weights = np.arange(1, period + 1)
        return prices.ewm(span=period).mean()  # Fallback to EMA

    def run(self, data):
        # Initialize target allocation with no allocation.
        allocation = {self.symbol: 0}

        if len(data["ohlcv"]) < self.slow_length + self.signal_length:
            # Not enough data for MACD calculation
            return TargetAllocation(allocation)

        close_prices = pd.Series([d[self.symbol]["close"] for d in data["ohlcv"]])
        
        # Calculate MACD using specified lengths.
        macd_values = MACD(self.symbol, data["ohlcv"], self.fast_length, self.slow_length)["MACD"]

        # LWMA or alternative for entry/exit signal.
        lwma_prices = self.lwma_calculator(close_prices, self.lwma_length)

        current_price = close_prices.iloc[-1]
        macd_current = macd_values[-1]
        lwma_current = lwma_prices.iloc[-1]

        # Check current holdings to avoid re-buying.
        current_holdings = data["holdings"].get(self.symbol, 0)

        # Entry condition: MACD positive and price above LWMA (using current holdings to avoid re-buying).
        if macd_current > 0 and current_price > lwma_current and current_holdings == 0:
            allocation[self.symbol] = 1  # Invest 100% of the portfolio in SPY
        # Exit condition: MACD negative or price below LWMA.
        elif macd_current < 0 or current_price < lwma_current:
            allocation[self.symbol] = 0  # Sell SPY

        return TargetAllocation(allocation)

    # Note: Implementing the sophisticated volume analysis and scheduling logic as described
    # requires additional infrastructure support for scheduling tasks and accessing historical
    # volume data beyond the strategy logic itself.