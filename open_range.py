
from backtesting import Backtest, Strategy

import pandas as pd

import time
from ib_insync import *

stocks = ['MSFT', 'GOOGL']
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=66)


class ORBStrategy(Strategy):
    
    def init(self):
        self.orb_high = None
        self.orb_low = None
        self.trade=0


    def next(self):
        # print(self.data.df)
        # time.sleep(1)

        # if len(self.data) < 2:
        #     return
        # else:
            if self.data.index[-1].time() == pd.Timestamp('10:00').time():
                df=self.data.df
                d=self.data.index[-1]
                d=pd.to_datetime(d.date())
                df=df[df.index>=d]
                self.orb_high = df.High.max()
                self.orb_low = df.Low.min()
                self.trade=0
                print(self.orb_high, self.orb_low)

        
            if not self.position and self.orb_high and self.orb_low:
                print('inside condition')
                if (self.data.Close[-1] > self.orb_high) and self.trade==0:
                    print('buy condition satisfied')
                    self.buy()
                    self.trade=1
                elif (self.data.Close[-1] < self.orb_low) and self.trade==0:
                    print('sell condition satisfied')
                    self.sell()
                    self.trade=1
            elif self.position:
                # Close position by the end of the day
                print('i have some position')
                if self.data.index[-1].time() == pd.Timestamp('15:20').time():
                    self.position.close()
                print(self.position)


def fetch_data(symbol):



    # contractS2=Contract(secType='FUT', symbol='ES', lastTradeDateOrContractMonth='202406', multiplier='50', exchange='CME', currency='USD', localSymbol='ESM4', tradingClass='ES') 
    contract2=Stock(symbol,'SMART','USD')


    # print(util.df(ib.reqContractDetails(Future(symbol='ES'))).to_string())
    # print(ib.reqContractDetails(contract2))
    contract2=ib.qualifyContracts(contract2)[0]
    print(contract2)
    bars = ib.reqHistoricalData(
        contract2, endDateTime='', durationStr='1 M',
        barSizeSetting='5 mins', whatToShow='TRADES', useRTH=True,formatDate=1)
    print('bars')
    print(bars)
    df1 = util.df(bars)
    print(df1)

    d1={'date':'Date','open':'Open','high':'High','low':'Low','close':'Close','volume':'Volume'}
    df1.rename(columns =d1, inplace = True) 
    # df1.set_index('Date',inplace=True)
    data=df1
    return data




# data = fetch_data('AMZN')
# print(data)


  # Focus on regular trading hours
# data.to_csv('data.csv')
# data['Date']=data['Date'].dt.tz_localize(None)
# data.set_index('Date',inplace=True)
# data = data.between_time('09:00:00', '16:00:00')

# bt = Backtest(data, ORBStrategy, cash=100_000, commission=.002)
# stats = bt.run()
# print(stats)
# bt.plot()

results = {}
for stock in stocks:
    data = fetch_data(stock)
    print(data)
    data['Date']=data['Date'].dt.tz_localize(None)
    data.set_index('Date',inplace=True)
    bt = Backtest(data, ORBStrategy, cash=100_000, commission=.002)
    stats = bt.run()
    results[stock] = stats
    bt.plot()

for stock, stats in results.items():
    print(f"{stock}:")
    print(stats)
