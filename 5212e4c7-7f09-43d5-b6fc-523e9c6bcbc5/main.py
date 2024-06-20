from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset
import numpy as np
import pandas as pd

class TradingStrategy(Strategy):
    def __init__(self):
        self.stocks = ['SMH', 'FDN', 'IGV', 'QQQ', 'SPY', 'XLI', 'XLF', 'XLP']
        self.bonds = ['TLT']
        self.slv = 'SLV'
        self.gld = 'GLD'
        self.xli = 'XLI'
        self.xlu = 'XLU'
        self.dbb = 'DBB'
        self.uup = 'UUP'
        self.mkt = 'SPY'
        self.all_assets = self.stocks + self.bonds + [self.slv, self.gld, self.xli, self.xlu, self.dbb, self.uup, self.mkt]
        
        self.mom_lookback = 90  # 3 months
        self.vola_lookback = 126
        self.base_ret = 85
        self.lev = 0.99
        self.rebalance_interval = 19  # Roughly every month
        self.rebalance_counter = 0
        
        self.mkt_data = {}
        self.bull = True

    @property
    def assets(self):
        return self.all_assets

    @property
    def interval(self):
        return "1day"
    
    def calculate_vola(self, symbol, data):
        returns = data["ohlcv"][symbol]["close"].pct_change()
        vola = returns[-self.vola_lookback:].std() * np.sqrt(252)
        return vola
    
    def calculate_momentum(self, symbols, data):
        momentums = {}
        for symbol in symbols:
            price_old = data["ohlcv"][symbol]["close"][-self.mom_lookback]
            price_new = data["ohlcv"][symbol]["close"][-1]
            momentum = (price_new / price_old) - 1
            momentums[symbol] = momentum
        return momentums
    
    def daily_check(self, data):
        vola = self.calculate_vola(self.mkt, data)
        wait_days = int(vola * self.base_ret)
        bull_check = self.calculate_momentum([self.slv, self.gld, self.xli, self.xlu, self.dbb, self.uup], data)
        exit_condition = all(bull_check[self.slv] < bull_check[self.gld], bull_check[self.xli] < bull_check[self.xlu], bull_check[self.dbb] < bull_check[self.uup])
        self.bull = not exit_condition

    def run(self, data):
        self.rebalance_counter += 1
        if self.rebalance_counter >= self.rebalance_interval:
            self.rebalance_counter = 0
            momentums = self.calculate_momentum(self.stocks, data)
            top_momentum_stocks = sorted(momentums, key=momentums.get, reverse=True)[:1]  # select top stock
        
        allocation_dict = {}
        if self.bull:
            for stock in self.stocks:
                allocation_dict[stock] = self.lev if stock in top_momentum_stocks else 0.0
            for bond in self.bonds:
                allocation_dict[bond] = 0.0
        else:
            for stock in self.stocks:
                allocation_dict[stock] = 0.0
            for bond in self.bonds:
                allocation_dict[bond] = self.lev
        
        return TargetAllocation(allocation_dict)