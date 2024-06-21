from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["SPY", "QQQ"]  # Preferable US equity ETFs
        self.data_list = []

    @property
    def interval(self):
        return "1day"  # Daily analysis

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def calculate_ibs(self, data):
        """Calculates Internal Bar Strength (IBS) for a ticker."""
        low = data['low']
        high = data['high']
        close = data['close']
        # IBS formula = (Close - Low) / (High - Low)
        return (close - low) / (high - low) if (high - low) > 0 else 0.5

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            daily_data = data["ohlcv"][-1][ticker]  # Latest available data
            rsi_values = RSI(ticker, data["ohlcv"], 10)  # Calculate RSI for each ticker

            # Calculate the IBS
            ibs = self.calculate_ibs(daily_data)

            # Allocation strategy based on IBS levels
            # Low IBS values (<0.3) indicate a potential buy (mean reversion expected)
            # High IBS values (>0.7) suggest avoiding buying or possibly selling
            if rsi_values and len(rsi_values) > 0:
                latest_rsi = rsi_values[-1]
                if ibs < 0.3 and latest_rsi < 30:  # Correct conditional check for RSI values
                    allocation_dict[ticker] = 1 / len(self.tickers)  # Equal allocation
                elif ibs > 0.7 and latest_rsi > 70:
                    allocation_dict[ticker] = 0   # No allocation
                else:
                    allocation_dict[ticker] = 0.5 / len(self.tickers)  # Neutral allocation

        return TargetAllocation(allocation_dict)

    @property
    def metadata(self):
        # Metadata to identify the days of the week and adapt the strategy accordingly,
        # especially focusing on Mondays or during high volatility periods
        return {"include_weekdays": [1], "volatility_threshold": None}