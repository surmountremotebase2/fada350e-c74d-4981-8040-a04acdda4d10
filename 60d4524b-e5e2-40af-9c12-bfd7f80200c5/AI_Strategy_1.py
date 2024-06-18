from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA, SMA, MACD, MFI, BB
from surmount.logging import log
from surmount.data import Asset, InstitutionalOwnership, InsiderTrading
import pandas as pd

class TradingStrategy(Strategy):
    def __init__(self):
        # Define initial capital and start date for the backtest.
        # These features are for demonstrational purposes. Actual use would depend on Surmount's main backtest engine.
        self.initial_capital = 10000
        self.start_date = pd.to_datetime("2010-01-01")
        self.tickers = ["SPY", "QQQ", "AAPL", "GOOGL"]
        self.data_list = [InstitutionalOwnership(i) for i in self.tickers]
        self.data_list += [InsiderTrading(i) for i in self.tickers]
    
    @property
    def interval(self):
        return "1day"
    
    @property
    def assets(self):
        return self.tickers
    
    @property
    def data(self):
        return self.data_list

    def run(self, data):
        # Strategy logic here
        # The focus here is on how to potentially use initial capital and start date,
        # but these would interact with broader backtest configurations, not directly within the run method.
        allocation_dict = {i: 1/len(self.tickers) for i in self.tickers}
        for i in self.data_list:
            if tuple(i)[0]=="insider_trading":
                if data[tuple(i)] and len(data[tuple(i)])>0:
                    if "Sale" in data[tuple(i)][-1]['transactionType']:
                        allocation_dict[tuple(i)[1]] = 0

        return TargetAllocation(allocation_dict)