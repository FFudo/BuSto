import time
from datetime import datetime, timedelta

import pandas as pd
import requests

from config import PAIR


class DataManger:
    def __init__(self):
        self.pair = PAIR

        self.today = self.set_today()
        self.yesterday = self.set_yesterday()
        self.df = self.set_df()

    def request_yesterday_data(self):
        ohlc_url = "https://api.kraken.com/0/public/OHLC"

        ohlc_params = {
            "pair": self.pair,
            "interval": 1440,
            "since": self.into_unix(self.yesterday),
        }
        payload = {}
        headers = {"Accept": "application/json"}

        response = requests.request(
            "GET",
            url=ohlc_url,
            headers=headers,
            data=payload,
            params=ohlc_params,
        )
        return response.json()

    def set_today(self):
        now = datetime.now()
        return now.replace(hour=0, minute=0, second=0, microsecond=0)

    def set_yesterday(self):
        return self.today - timedelta(days=1)

    def into_unix(self, day):
        return int(time.mktime(day.timetuple()))

    def into_day(self, time):
        return datetime.fromtimestamp(time).strftime("%Y-%m-%dT%H:%M:%SZ")

    def set_df(self):
        return pd.read_csv("./data.csv")

    def add_yesterday(self):
        data = self.request_yesterday_data()
        data = data["result"]["XXBTZEUR"][0]
        date_unix = data[0]
        high = float(data[2])
        low = float(data[3])
        yesterday_data = {
            "pair": self.pair,
            "date": self.into_day(date_unix),
            "date_unix": date_unix,
            "high": high,
            "low": low,
            "avg": (high + low) / 2,
        }
        self.df.loc[len(self.df)] = yesterday_data
        print(self.df)
