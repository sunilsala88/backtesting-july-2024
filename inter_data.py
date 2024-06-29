from ib_insync import *


ib = IB()
ib.connect('127.0.0.1', 7497, clientId=14)


contract=Stock('AMZN','SMART','USD')
bars = ib.reqHistoricalData(
        contract,
        endDateTime='',
        durationStr='20 D',
        barSizeSetting='1 min',
        whatToShow='MIDPOINT',
        useRTH=True,
        formatDate=1)
print(bars)
df = util.df(bars)
print(df)