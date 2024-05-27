from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the ticker symbol for the asset we're interested in
        self.ticker = "AAPL"

    @property
    def assets(self):
        # The list of assets this strategy will manage
        return [self.ticker]

    @property
    def interval(self):
        # The time interval for analysis; can be adjusted based on strategy requirements
        return "1day"

    def run(self, data):
        # Define thresholds for RSI to determine buy and sell signals
        oversold_threshold = 30
        overbought_threshold = 70
        
        # Calculate the RSI for the asset
        rsi_values = RSI(self.ticker, data["ohlcv"], length=14)
        
        allocation_dict = {}
        
        if len(rsi_values) > 0:
            # Get the most recent RSI value
            latest_rsi = rsi_values[-1]
            
            log(f"Latest RSI for {self.ticker}: {latest_rsi}")
            
            # Determine the target allocation based on RSI values
            if latest_rsi < oversold_threshold:
                # RSI indicates oversold conditions; consider buying by setting allocation to 1 (or 100% of portfolio)
                allocation_dict[self.ticker] = 1.0
            elif latest_rsi > overbought_threshold:
                # RSI indicates overbought conditions; consider selling or avoiding purchase by setting allocation to 0
                allocation_dict[self.ticker] = 0.0
            else:
                # RSI indicates neutral conditions; here, you can decide how to allocate; below line assumes holding/no change
                allocation_dict[self.ticker] = 0.0 # Adjust as suited for neutral conditions
        else:
            # No RSI data available, log and do not change allocations
            log(f"No RSI data available for {self.ticker}.")
            allocation_dict[self.ticker] = 0.0 # No action, could be adjusted based on preference
            
        return TargetAllocation(allocation?dict)