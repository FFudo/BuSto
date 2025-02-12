import time
from datetime import datetime

from config import BUY_AMOUNT, PAIR
from data_manager import DataManger
from discord_messenger import DiscordWebhook
from fund_manager import FundManager

if __name__ == "__main__":
    data_manager = DataManger()
    fund_manager = FundManager()
    discord_webhook = DiscordWebhook()

    while True:
        data_manager.check_days()

        if data_manager.is_yesterday_missing():
            data_manager.add_yesterday()
            fund_manager.update_transaction()
            discord_webhook.send_message(
                f"Just added {data_manager.yesterday} and set threshhold to {data_manager.threshold}%"
            )
            discord_webhook.send_message(
                f"At the Moment {PAIR} is {data_manager.last_percentage}% compared to the last 7 days"
            )
            discord_webhook.send_message(
                f"Bought this month is: {fund_manager.bought_this_month}"
            )

        if not fund_manager.bought_this_month:
            if data_manager.is_price_low_enough():
                price = data_manager.market_api.request_ask_price()
                fund_manager.buy(price=price)
                discord_webhook.send_message(
                    f"Bought {BUY_AMOUNT}€ of {PAIR} for {price}"
                )

        current_time = datetime.now().time()
        if current_time.hour in [6, 18] and current_time.minute == 30:
            discord_webhook.send_message(
                f"At the Moment {PAIR} is {data_manager.last_percentage}% compared to the last 7 days"
            )
            discord_webhook.send_message(
                f"Bought this month is: {fund_manager.bought_this_month}"
            )
        time.sleep(15)
