from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the tickers to monitor and trade
        self.spy_ticker = "SPY"  # SPY for monitoring
        self.shy_ticker = "SHY"  # SHY for trading
    
    @property
    def interval(self):
        return "1day"  # Use daily data

    @property
    def assets(self):
        # Only need to monitor SPY for trading signals but trade SHY based on SPY's RSI
        return [self.spy_ticker, self.shy_ticker]  

    def run(self, data):
        # Initialize allocation to SHY as 0
        allocation = {self.shy_ticker: 0.0}
        
        # Calculate the 14-day RSI for SPY
        rsi_values = RSI(self.spy_ticker, data["ohlcv"], 14)
        
        if rsi_values:
            latest_rsi = rsi_values[-1]  # Get the most recent RSI value

            # Check the RSI conditions to decide on the allocation
            if latest_rsi > 80:
                # If RSI > 80, allocate 100% to SHY
                allocation[self.shy_ticker] = 1.0
            elif latest_rsi < 25 or (rsi_values[-2] < 30 and latest_rsi >= 30):
                # If RSI < 25 or if it crosses over 30 (i.e., was below 30 and now 30 or above),
                # allocate 0% to SHY implying staying or moving back to cash or other assets
                allocation[self.shy_ticker] = 0.0
            # Else keep the previous allocation (not changing allocation if conditions don't match)

        return TargetAllocation(allocation)