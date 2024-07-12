from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        # Initialize your tickers and their allocations here. 
        # The allocations should sum up to 1 (or 100% of the portfolio).
        # Example: self.tickers_allocation = {"AAPL": 0.2, "GOOGL": 0.2, "MSFT": 0.2, "AMZN": 0.2, "FB": 0.2}
        # You will replace these tickers and allocations with the ones you decide later.
        self.tickers_allocation = {"TICKER1": 0.2, "TICKER2": 0.2, "TICKER3": 0.2, "TICKER4": 0.2, "TICKER5": 0.2}

    @property
    def assets(self):
        # This will dynamically create a list of assets based on your ticker_allocation keys.
        return list(self.tickers_allocation.keys())

    @property
    def interval(self):
        # Define the interval for your strategy. You can adjust this based on the desired frequency.
        # Common intervals include "1day", "1hour", "30min", etc.
        return "1day"

    @property
    def data(self):
        # Include any additional data you might need. 
        # This example doesn't require additional data fields, but you can add as needed.
        return []

    def run(self, data):
        # This method doesn't need to check conditions since it's a Buy and Hold strategy.
        # It simply returns the predefined allocations for each ticker.
        return TargetAllocation(self.tickers_allocation)