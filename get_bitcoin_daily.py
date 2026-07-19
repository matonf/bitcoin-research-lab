import requests
import pandas as pd
from datetime import datetime, timedelta

start = datetime(2010, 7, 23)
today = datetime.today()

rows = []

current = start

while current <= today:

    url = f"https://onfray.info/bitcoin/getpriceapi.php?iddate={current:%Y-%m-%d}"

    data = requests.get(url).json()

    for date, price in data.items():
        rows.append({
            "date": date,
            "price_usd": price
        })

    current += timedelta(days=10)

df = pd.DataFrame(rows)

df["date"] = pd.to_datetime(df["date"])

df = (
    df
    .drop_duplicates("date")
    .sort_values("date")
    .reset_index(drop=True)
)

df["day"] = (df["date"] - df["date"].min()).dt.days

df.to_csv("bitcoin_daily.csv", index=False)
