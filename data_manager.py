from datetime import datetime, timedelta

import pandas as pd

from config import PAIR
from market_data_api import MarketApi
from helper import into_day, into_unix


class DataManger:
    def __init__(self):
        self.pair = PAIR
        self.data_file = "./data.csv"
        self.update_days()
        self.set_df()

        self.market_api = MarketApi()

    def is_yesterday_missing(self) -> bool:
        self.update_days()
        if self.yesterday.strftime("%Y-%m-%d") not in self.df["date"].values:
            return True

        return False

    def set_today(self):
        now = datetime.now()
        return now.replace(hour=0, minute=0, second=0, microsecond=0)

    def set_yesterday(self):
        return self.today - timedelta(days=1)

    def update_days(self):
        self.today = self.set_today()
        self.yesterday = self.set_yesterday()

    def set_df(self):
        self.df = pd.read_csv(self.data_file)

    def add_yesterday(self):
        data = self.market_api.request_ohcl_data(into_unix(self.yesterday))
        date_unix = data[0]
        high = float(data[2])
        low = float(data[3])
        yesterday_data = {
            "pair": self.pair,
            "date": into_day(date_unix),
            "date_unix": date_unix,
            "high": high,
            "low": low,
            "avg": (high + low) / 2,
        }

        self.df.loc[len(self.df)] = yesterday_data
        self.df.to_csv(self.data_file, encoding="utf-8", index=False, header=True)
        print(f"Added Day: {yesterday_data["date"]} to csv")
