from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the tickers to monitor and trade
        self.spy_ticker = "SPY"  # SPY for monitoring
        self.shy_ticker = "SHY"  # SHY for trading
        self.tqqq_ticker = "TQQQ"  # TQQQ for trading
        self.uvxy_ticker = "UVXY"  # UVXY for trading

    @property
    def interval(self):
        return "1day"  # Use daily data

    @property
    def assets(self):
        # Only need to monitor SPY for trading signals but trade SHY based on SPY's RSI
        return [self.spy_ticker, self.shy_ticker, self.tqqq_ticker, self.uvxy_ticker]  

    def run(self, data):
        # Initialize allocation to SPY as 100%
        allocation = {self.spy_ticker: 100.0, self.shy_ticker: 0.0, self.tqqq_ticker: 0.0, self.uvxy_ticker: 0.0}
        
        # Calculate the 10-day RSI for TQQQ
        rsi_values = RSI(self.tqqq_ticker, data["ohlcv"], 10)
        
        if rsi_values:
            latest_rsi = rsi_values[-1]  # Get the most recent RSI value

            # Check the RSI conditions to decide on the allocation
            if latest_rsi >= 80:
                # If RSI >= 80, allocate 50% to SHY and 50% to UVXY
                allocation[self.uvxy_ticker] = 50.0
                allocation[self.shy_ticker] = 50.0
                allocation[self.spy_ticker] = 0.0
            elif latest_rsi < 20:
                # If RSI < 80, allocate 100% to SPY
                allocation[self.spy_ticker] = 0.0
                allocation[self.uvxy_ticker] = 0.0
                allocation[self.shy_ticker] = 0.0
                allocation[self.tqqq_ticker] = 100.0

        return TargetAllocation(allocation)