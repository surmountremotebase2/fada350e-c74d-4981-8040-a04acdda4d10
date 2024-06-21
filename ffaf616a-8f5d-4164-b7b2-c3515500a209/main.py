import matplotlib.pyplot as plt
from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self, rsi_threshold):
        self.spy_ticker = "SPY"
        self.shy_ticker = "SHY"
        self.tqqq_ticker = "TQQQ"
        self.uvxy_ticker = "UVXY"
        self.rsi_threshold = rsi_threshold

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return [self.spy_ticker, self.shy_ticker, self.tqqq_ticker, self.uvxy_ticker]  

    def run(self, data):
        allocation = {self.spy_ticker: 100.0, self.shy_ticker: 0.0, self.tqqq_ticker: 0.0, self.uvxy_ticker: 0.0}
        
        rsi_values = RSI(self.tqqq_ticker, data["ohlcv"], 10)
        
        if rsi_values:
            latest_rsi = rsi_values[-1]

            if latest_rsi >= self.rsi_threshold:
                allocation[self.uvxy_ticker] = 50.0
                allocation[self.shy_ticker] = 50.0
                allocation[self.spy_ticker] = 0.0
            else:
                allocation[self.spy_ticker] = 100.0
                allocation[self.uvxy_ticker] = 0.0
                allocation[self.shy_ticker] = 0.0

        return TargetAllocation(allocation)

def backtest_strategy(strategy, data):
    # Simulate the strategy using the provided data
    # This function should return a performance metric (e.g., cumulative return, Sharpe ratio)
    # For simplicity, we assume it returns cumulative return
    performance = 0  # Placeholder, replace with actual backtest result
    return performance

def optimize_rsi_threshold(data, thresholds):
    best_threshold = None
    best_performance = float('-inf')
    performance_results = []

    for threshold in thresholds:
        strategy = TradingStrategy(rsi_threshold=threshold)
        performance = backtest_strategy(strategy, data)
        
        performance_results.append((threshold, performance))
        
        if performance > best_performance:
            best_performance = performance
            best_threshold = threshold
    
    return best_threshold, best_performance, performance_results

# Example data (replace with actual data)
data = {
    "ohlcv": ...  # Your OHLCV data here
}

# Define the range of RSI threshold values to test
rsi_thresholds = range(60, 90, 5)

# Perform the optimization
best_threshold, best_performance, performance_results = optimize_rsi_threshold(data, rsi_thresholds)

print(f"Best RSI threshold: {best_threshold} with performance: {best_performance}")

# Plot the performance results
thresholds, performances = zip(*performance_results)
plt.plot(thresholds, performances, marker='o')
plt.xlabel('RSI Threshold')
plt.ylabel('Performance')
plt.title('RSI Threshold Optimization')
plt.show()