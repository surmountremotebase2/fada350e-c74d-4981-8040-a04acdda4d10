from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define which tickers you're interested in monitoring
        self.tickers = ["TSLA", "AMZN", "MSFT"]
        # No additional data requirements beyond OHLCV for this simple strategy
        self.data_list = []

    @property
    def interval(self):
        # Daily intervals to check the 50-day SMA
        return "1day"

    @property
    def assets(self):
        # The assets this strategy will handle
        return self.tickers

    @property
    def data(self):
        # Required data for the strategy; in this case, only price data is needed
        return self.data_list

    def run(self, data):
        allocation_dict = {}
        # Loop through each ticker to analyze data and set target allocation
        for ticker in self.tickers:
            # Fetch the daily close prices for the calculation
            d = data["ohlcv"]
            # Calculate the 50-day simple moving average
            sma_50 = SMA(ticker, d, 50)
            if sma_50 is not None and len(sma_50) > 0:
                # Fetch the current close price
                current_price = d[-1][ticker]["close"]
                # Check if the current price is above the 50-day SMA for bullish signal
                if current_price > sma_50[-1]:
                    # Allocate a significant portion to the bullish stock,
                    # here we choose 30% as an indicative value for demonstration purposes.
                    allocation_dict[ticker] = 0.30
                else:
                    # If not bullish, do not allocate to this stock
                    allocation_dict[ticker] = 0.0
            else:
                # In case of insufficient data or error calculating SMA,
                # default to no allocation for safety.
                allocation_dict[ticker] = 0.0

        # Ensure the allocations are normalized to not exceed 1 in total
        total_allocation = sum(allocation_dict.values())
        if total_allocation > 1:
            # Adjust allocations proportionally if the sum exceeds 1
            allocation_dict = {k: v/total_allocation for k, v in allocation_dict.items()}

        return TargetAllocation(allocation_dict)