from config import BUY_AMOUNT, PAIR

class FundManager:
    def __init__(self):
        self.buy_amount = BUY_AMOUNT
        self.pair = PAIR

        self.bought_this_month = False

    def buy(self):
        self.bought_this_month = True