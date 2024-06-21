from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the tickers we are interested in: SPY for the S&P 500 ETF, SHY for the 1-3 Year Treasury Bond ETF
        self.tickers = ["SPY", "SHY"]

    @property
    def interval(self):
        # Weekly interval for RSI calculation
        return "1week"

    @property
    def assets(self):
        # Assets involved in the trading strategy
        return self.tickers

    @property
    def data(self):
        # No additional data required beyond what is provided by default
        return []

    def run(self, data):
        # Calculate the weekly RSI for SPY
        spy_rsi = RSI("SPY", data["ohlcv"], 10)  # Using a period of 14 weeks for RSI

        # Initialize allocation_dict dict with no allocation
        allocation_dict = {"SPY": 0.0, "SHY": 0.0}

        if spy_rsi is not None:
            current_rsi = spy_rsi[-1]  # Get the most recent RSI value

            # If RSI > 70, move 100% to SHY
            if current_rsi > 80:
                allocation_dict["SHY"] = 1.0
            # If RSI < 60, move 100% to SPY
            elif current_rsi < 80:
                allocation_dict["SPY"] = 1.0
            # If RSI is between 60 and 70, maintain the current allocation
            # This scenario should ideally be handled based on the prior state (not moving out of SPY unless RSI > 70),
            # but due to limitations of not having prior state access in this example code, we'll allocate to SPY.
            # Implementers may need to adjust this logic based on actual capabilities to track prior allocations or states.
            else:
                allocation_dict["SPY"] = 1.0

        return TargetAllocation(allocation_dict)