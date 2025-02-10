from datetime import datetime

import pandas as pd

from config import BUY_AMOUNT, PAIR


class FundManager:
    def __init__(self):
        self.buy_amount = BUY_AMOUNT
        self.pair = PAIR
        self.buy_price = None
        self.transaction_columns = ["Date", "Time", "Pair", "Price", "Buy Amount"]
        self.update_transaction()

    def buy(self):
        if not self.bought_this_month:
            self.buy_price = 62000
            self.log_transaction(self.buy_price)

    def log_transaction(self, price):
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M")
        new_transaction = pd.DataFrame(
            {
                "Date": [today],
                "Time": [time],
                "Pair": [self.pair],
                "Price": [price],
                "Buy Amount": [self.buy_amount],
            }
        )

        try:
            df = pd.read_csv("transactions.csv")
        except FileNotFoundError:
            df = pd.DataFrame(columns=self.transaction_columns)

        df = pd.concat([df, new_transaction], ignore_index=True)

        df.to_csv("transactions.csv", index=False)

    def update_transaction(self):
        if self.is_transaction_for__current_month():
            self.bought_this_month = True
        else:
            self.bought_this_month = False

    def is_transaction_for__current_month(self):
        try:
            df = pd.read_csv("transactions.csv")

            df["Date"] = pd.to_datetime(df["Date"])

            current_month = datetime.now().strftime("%Y-%m")

            df["Month"] = df["Date"].dt.to_period("M")

            month_exists = (df["Month"] == current_month).any()

            return month_exists
        except FileNotFoundError:
            return False
