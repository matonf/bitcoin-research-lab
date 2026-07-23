from datetime import datetime, timedelta
import requests
import pandas as pd

API = 'https://onfray.info/bitcoin/getpriceapi.php?iddate={}'
START = datetime(2010,7,23)
END = datetime.today()

rows=[]
current=START
while current<=END:
    data=requests.get(API.format(current.strftime('%Y-%m-%d')),timeout=30).json()
    for d,p in data.items():
        rows.append({'date':d,'price_usd':p})
    current += timedelta(days=10)

df=pd.DataFrame(rows)
df['date']=pd.to_datetime(df['date'])
df=df.drop_duplicates('date').sort_values('date').reset_index(drop=True)
df['day']=(df['date']-df['date'].min()).dt.days
print(df.head())
print(df.tail())
print(f'Records: {len(df)}')