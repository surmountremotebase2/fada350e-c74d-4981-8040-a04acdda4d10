from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA
from surmount.logging import log
from datetime import datetime

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "QQQ"  # Define the ticker we want to trade
        self.target_profit_long = 0.04  # Target profit for long position (4%)
        self.stop_loss_long = -0.04  # Stop loss for long position (-4%)
        self.target_profit_short = 0.01  # Target profit for short position (1%)
        self.stop_loss_short = -0.04  # Stop loss for short position (-4%)
        self.under_ema_weeks_count = 0  # Counter to track consecutive weeks under EMA 50
    
    @property
    def interval(self):
        return "W"  # Use weekly data for this strategy, adjusted format

    @property
    def assets(self):
        return [self.ticker]  # Assets that this strategy will use

    def run(self, data):
        weekly_data = data["ohlcv"]  # Get weekly OHLCV data
        last_close_price = weekly_data[-1][self.ticker]["close"]  # Last weekly close price
        ema_50 = EMA(self.ticker, weekly_data, 50)  # Calculate EMA 50

        # Ensure we have enough data points for both last close price and the EMA calculation
        if len(weekly_data) < 50 or ema_50 is None or len(ema_50) == 0:
            return TargetAllocation({})
        
        today = datetime.now()
        position = {}
        
        # Determine if today is Monday
        if today.weekday() == 0:  # Monday
            if last_close_price > ema_50[-1]:  # Weekly candle is above EMA 50
                self.under_ema_weeks_count = 0  # Reset counter as we are above EMA 50
                position[self.ticker] = 1  # Long QQQ
                log(f"Going long on {self.ticker}. Weekly close: {last_close_price}, EMA 50: {ema_50[-1]}")
            else:
                # Increment the counter if weekly candle is below EMA 50
                self.under_ema_weeks_count += 1
                
                # Only open a short position if we've been under the EMA 50 for more than 2 consecutive weeks
                if self.under_ema_weeks_count > 2:
                    position[self.ticker] = -1  # Short QQQ
                    log(f"Going short on {self.ticker}. Weekly close: {last_close_price}, EMA 50: {ema_50[-1]}, Weeks under EMA: {self.under_ema_weeks_count}")
                else:
                    position[self.ticker] = 0  # No action
                    log(f"No action. Weekly close: {last_close_price}, EMA 50: {ema_50[-1]}, Weeks under EMA: {self.under_ema_weeks_count}")
        else:
            # If it's not Monday, we do not trade.
            position[self.ticker] = 0
            log("Today is not Monday, no trading action is taken.")
        
        # Note: Target profit and stop loss levels are mentioned for strategy implementation.
        # Actual execution of these levels would need to be handled via order management after placing trades,
        # which is outside the scope of this strategy logic.

        return TargetAllocation(position)