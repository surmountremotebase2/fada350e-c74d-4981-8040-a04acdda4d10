import pandas as pd

def run(self, data):
        # Initialize TQQQ allocation to 0
        allocation = {"TQQQ": 0, "BIL": 1}

        StockData = data["ohlcv"]
        #d[-1]["QQQ"]
        # Retrieve OHLCV data for SPY
        StockDF = pd.DataFrame(StockData)
        ohlcv_spy = StockDF["QQQ"]
        ohlcv_tqqq = StockDF["TQQQ"]

        # Ensure we have at least two days of data for SPY to compare
        if len(ohlcv_spy) >= 2:
            # Define "yesterday" and "today" based on the latest two data points
            yesterday = ohlcv_spy.iloc[-2]
            today = ohlcv_spy.iloc[-1]
            todaydate = today['date']
            #log(f'TODAY: {todaydate}')
            # convert the string to a datetime object
            todaydate_obj = pd.to_datetime(todaydate)
            '''vols = [i["QQQ"]["volume"] for i in StockData]
            smavolL = self.SMAVol("QQQ", StockData, 30)
            smavolS = self.SMAVol("QQQ", StockData, 3)
            #log(f'SMA Vol: {smavolL}')

            if len(vols)==0:
                    #return TargetAllocation({})
                self.VolTrigger = False
            else:
                if len(vols) < 30:
                    self.VolTrigger = True
                else:
                    if smavolS[-1] > smavolL[-1]:
                            self.VolTrigger = True
                    else: self.VolTrigger = False'''

            # check if the date is between December 20th and January 1st
            if (todaydate_obj.month == 12 and todaydate_obj.day >= 20 or todaydate_obj.month == 1 and todaydate_obj.day <= 6):
                #log(f'The date is between December 20th and January 1st.')
                if self.buy_signal:
                    log(f'The date is between December 20th and January 1st.')
                    self.buy_signal = False
                    self.hold_days = 0
                    
            else:
                # Check if today is a Monday and if the conditions are fulfilled
                today_date = pd.to_datetime(today['date'])
                if today_date.weekday() == 0:  # 0 represents Monday
                    ibs_today = self.IBS(today['close'], today['high'], today['low'])
                    #if today['close'] < yesterday['close'] and ibs_today < 0.5 and self.VolTrigger:
                    if today['close'] < yesterday['close'] and ibs_today < 0.5:
                        # Mark buy signal as True if conditions are met
                        self.buy_signal = True
            
            # Sell conditions based on SPY performance or holding duration
            if self.buy_signal:
                ht = yesterday['high']
                #ibs_today = self.IBS(today['close'], today['high'], today['low'])
                #if ( self.hold_days >= 7 or today['close'] > yesterday['high'] ):
                if ( self.hold_days >= 7 or today['close'] > ht ):
                #if self.hold_days >= 5 or today['close'] > yesterday['high']:
                    # Sell TQQQ (set allocation to 0) if holding period is 4 days or SPY closes higher than yesterday's high
                    self.buy_signal = False  # Reset buy signal
                    self.hold_days = 0  # Reset holding counter
                else:
                    # Keep holding TQQQ
                    allocation["TQQQ"] = 1
                    allocation["BIL"] = 0
                    self.hold_days += 1
        
        if self.buy_signal and self.hold_days == 0:
            # If a buy signal was triggered and we are in the initial day of action
            allocation["TQQQ"] = 1
            allocation["BIL"] = 0
            self.hold_days = 1  # Increment the hold day counter since we decided to buy