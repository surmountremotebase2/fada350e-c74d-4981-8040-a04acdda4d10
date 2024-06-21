from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the tickers to monitor and trade
        self.tickers = ["SPY", "QQQ", "TLT"]

    @property
    def interval(self):
        return "1day"  # Use daily data

    @property
    def assets(self):
        # Assets to trade
        return self.tickers

    def calculate_ibs(self, data):
        """Calculates Internal Bar Strength (IBS) for a ticker."""
        low = data['low']
        high = data['high']
        close = data['close']
        return (close - low) / (high - low) if (high - low) > 0 else 0.5

    def run(self, data):
        # Initialize allocation dictionary
        allocation_dict = {ticker: 0.0 for ticker in self.tickers}
        
        for ticker in self.tickers:
            daily_data = data["ohlcv"][ticker][-1]  # Latest available data for the ticker
            rsi_values = RSI(ticker, data["ohlcv"][ticker], 10)  # Calculate RSI for each ticker

            # Calculate the IBS
            ibs = self.calculate_ibs(daily_data)

            if rsi_values and len(rsi_values) > 0:
                latest_rsi = rsi_values[-1]
                if ibs < 0.3 and latest_rsi < 30:
                    allocation_dict[ticker] = 1.0 / len(self.tickers)  # Equal allocation
                elif ibs > 0.7 and latest_rsi > 70:
                    allocation_dict[ticker] = 0.0  # No allocation
                else:
                    allocation_dict[ticker] = 0.5 / len(self.tickers)  # Neutral allocation

        return TargetAllocation(allocation_dict)