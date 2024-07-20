import pandas as pd
#getting 10 year data
data=pd.read_csv('MNST_1hour.csv')
data['Date']=pd.to_datetime(data['Date'])
data['Date']=data['Date'].dt.tz_localize(None)
data.set_index('Date',inplace=True)
print(data)