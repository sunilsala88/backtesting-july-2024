# from ib_insync import *


# ib = IB()
# ib.connect('127.0.0.1', 7497, clientId=14)


# contract=Stock('AMZN','SMART','USD')
# bars = ib.reqHistoricalData(
#         contract,
#         endDateTime='',
#         durationStr='20 D',
#         barSizeSetting='1 min',
#         whatToShow='MIDPOINT',
#         useRTH=True,
#         formatDate=1)
# print(bars)
# df = util.df(bars)
# print(df)




from ib_insync import *
# util.startLoop()  # uncomment this line when in a notebook
import datetime as dt
import pandas as pd
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=66)

def last_day_of_month(year, month):
    next_month = month % 12 + 1
    next_year = year + month // 12
    last_day = dt.date(next_year, next_month, 1) - dt.timedelta(days=1)
    return last_day


name='GOOG'
contract2=Stock(name,'SMART','USD')
contract2=ib.qualifyContracts(contract2)[0]
# year=5
print(contract2)

final_data=pd.DataFrame()
for year in range(2016,2023,1):

    for month in range(1,13):

        end_time=last_day_of_month(year, month)
        print(end_time)
        bars = ib.reqHistoricalData(
            contract2, endDateTime=end_time, durationStr='1 M',
            barSizeSetting='1 hour', whatToShow='TRADES', useRTH=True,formatDate=1)
        df1 = util.df(bars)
        print(df1)
        final_data=pd.concat([final_data,df1],axis=0).drop_duplicates()
    
print(final_data)

# d1={'date':'Date','open':'Open','high':'High','low':'Low','close':'Close','volume':'Volume'}
# final_data.rename(columns =d1, inplace = True) 
# final_data.set_index('Date',inplace=True)
# final_data.to_csv(f'{name}_1hour.csv')