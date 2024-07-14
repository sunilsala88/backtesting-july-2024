
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import yfinance as yf
import pandas as pd
import time
from ib_insync import *
import pandas_ta as ta

def sma(close_data,period):
    return ta.sma(close_data,length=period)

def bbands(close,n):
    b=ta.bbands(close,length=n)
    print(b)
    return b[f'BBL_{n}_2.0'],b[f'BBU_{n}_2.0']

class bollingerband(Strategy):
    n=20
    stop_number=0.05
    def init(self):
        # self.sma20=self.I(sma,self.data.Close.s,20)
        # self.sma50=self.I(sma,self.data.Close.s,50)
        # self.sma200=self.I(sma,self.data.Close.s,200)
        self.lower,self.upper=self.I(bbands,self.data.Close.s,self.n)


    def next(self):
        if self.lower[-1]>self.data.Close[-1] :
            p=self.data.Close[-1]
            if self.position.is_short:
                self.position.close()
            else:
                pass
            self.buy(sl=(1-self.stop_number)*p)
        elif self.upper[-1]<self.data.Close[-1]  :
            p=self.data.Close[-1]
            if self.position.is_long:
                self.position.close()
            else:
                pass
            self.sell(sl=(1+self.stop_number)*p)


data=yf.download("RELIANCE.NS",start="2017-01-01",end="2023-04-30")
print(data)
data=data['2021-08-24':]
print(bbands(data["Close"],20))



bt=Backtest(data,bollingerband,cash=100_000)
output=bt.run()
print(output)
print(output['_trades'])
bt.plot()




a=[0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1]
stats=bt.optimize(stop_number=a,maximize='Return [%]')
print(stats)
print(stats['_strategy'])
bt.plot()

