from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.data import Asset
import logging

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["SPY"]
        logging.basicConfig(level=logging.INFO)

    @property
    def interval(self):
        return "1day"  # Use daily data

    @property
    def assets(self):
        return self.tickers

    def calculate_ibs(self, data):
        low = data['low']
        high = data['high']
        close = data['close']
        return (close - low) / (high - low) if (high - low) > 0 else 0.5

    def run(self, data):
        allocation_dict = {ticker: 0.0 for ticker in self.tickers}
        
        for ticker in self.tickers:
            if ticker not in data["ohlcv"] or not data["ohlcv"][ticker]:
                logging.info(f"No OHLCV data for ticker: {ticker}")
                continue
            
            daily_data = data["ohlcv"][ticker][-1]
            rsi_values = RSI(ticker, data["ohlcv"][ticker], 10)

            if rsi_values and len(rsi_values) > 0:
                latest_rsi = rsi_values[-1]
                ibs = self.calculate_ibs(daily_data)
                
                logging.info(f"{ticker} - IBS: {ibs}, RSI: {latest_rsi}")
                
                if ibs < 0.3 and latest_rsi < 50:
                    allocation_dict[ticker] = 100.0 / len(self.tickers)
                elif ibs > 0.7 and latest_rsi > 50:
                    allocation_dict[ticker] = 0.0
                else:
                    allocation_dict[ticker] = 0.0  # Neutral allocation

        logging.info(f"Final Allocation dict: {allocation_dict}")
        return TargetAllocation(allocation_dict)