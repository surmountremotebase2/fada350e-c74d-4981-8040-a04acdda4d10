from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD, LWMA, SMA
from surmount.data import OHLCV, Asset
from datetime import datetime, timedelta
import pandas as pd

class TradingStrategy(Strategy):
    def __init__(self):
        # Your initialization here
        self.symbol = "SPY"
        self.cash = 100000
        self.start_date = datetime(2020, 1, 1)
        self.end_date = datetime(2023, 1, 1)
        self.data_list = [OHLCV(self.symbol)]

    @property
    def interval(self):
        # Set to daily resolution
        return "1day"

    @property
    def assets(self):
        # Define the main trading symbol
        return [self.symbol]

    def run(self, data):
        allocation_dict = {self.symbol: 0}  # Default to no allocation
        ohlcv_data = data["ohlcv"][self.symbol]

        # Implement MACD Indicator
        macd_values = MACD(self.symbol, ohlcv_data, 12, 26, "wilders")
        signal_line = SMA(macd_values["MACD"], 9)  # Signal line with specified period (approximation)

        # Implementing 55-period LWMA for entry/exit
        price_data = [x["close"] for x in ohlcv_data[-55:]]  # Latest 55 periods data
        lwma_55 = LWMA(self.symbol, ohlcv_data, 55)  # Lightweight moving average

        # Assuming a method to get current position or invested status
        # invested = self.check_invested_status(self.symbol)
        invested = False  # Placeholder for demonstration

        # Buy Logic
        if macd_values[-1] > signal_line[-1] and price_data[-1] > lwma_55[-1] and not invested:
            allocation_dict[self.symbol] = 1  # 100% allocation to SPY

        # Sell Logic
        elif macd_values[-1] < signal_line[-1] or price_data[-1] < lwma_55[-1]:
            allocation_dict[self.symbol] = 0  # Sell SPY, move to cash

        # Weekly volume check logic (simplified for demonstration)
        today = datetime.now()
        if today.weekday() == 4:  # Assuming Friday as the last trading day
            weekly_volume = self.calculate_weekly_volume(ohlcv_data)
            # Additional logic to track and sort based on volume difference

        return TargetAllocation(allocation_dict)

    def calculate_weekly_volume(self, ohlcv_data):
        # Example function logic to calculate weekly volumes
        volume_data = [x["volume"] for x in ohlcv_data]
        df = pd.DataFrame(volume_data, columns=['Volume'])
        df['Week'] = pd.to_datetime(ohlcv_data['date']).dt.week
        weekly_volume = df.groupby('Week')['Volume'].sum()
        return weekly_volume.tolist()