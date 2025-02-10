from datetime import datetime, timedelta

import pandas as pd

from config import PAIR
from helper import into_day, into_unix
from market_data_api import MarketApi


class DataManger:
    def __init__(self):
        self.pair = PAIR
        self.data_file = "./data.csv"

        self.today = self.set_today()
        self.yesterday = self.set_yesterday()
        self.update_threshold()

        self.set_df()

        self.threshold = 10
        self.cutoff_day = 15
        self.market_api = MarketApi()

    def set_today(self):
        return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    def set_yesterday(self):
        return self.today - timedelta(days=1)

    def set_df(self):
        self.df = pd.read_csv(self.data_file)

    def check_days(self):
        if (
            datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            != self.today
        ):
            self.today = self.set_today()
            self.yesterday = self.set_yesterday()
            self.update_threshold()

    def update_threshold(self):
        today = datetime.day
        if 1 <= today <= self.cutoff_day:
            self.threshold = 10
        elif self.cutoff_day < today < (self.cutoff_day + self.threshold):
            self.threshold -= 1
        else:
            self.threshold = 0

    def is_yesterday_missing(self) -> bool:
        if self.yesterday.strftime("%Y-%m-%d") not in self.df["date"].values:
            return True
        return False

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

    def is_price_low_enough(self):
        last_7_days = pd.to_numeric(self.df["avg"].tail(7), errors="coerce")
        seven_days_avg = last_7_days.mean()
        ask_price = float(self.market_api.request_ask_price())
        percentage = (100 * ask_price) / seven_days_avg
        return percentage <= (100 - self.threshold)
