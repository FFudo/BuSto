import time

from config import PAIR
from data_manager import DataManger
from discord_messenger import DiscordWebhook
from fund_manager import FundManager

if __name__ == "__main__":
    data_manager = DataManger()
    fund_manager = FundManager()
    discord_webhook = DiscordWebhook()

    discord_webhook.send_message("Started up!")

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
                fund_manager.buy()
                discord_webhook.send_message(
                    f"Bought {PAIR} for {fund_manager.buy_price}"
                )

        time.sleep(10)
