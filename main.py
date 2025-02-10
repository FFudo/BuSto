import time

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
            discord_webhook.send_message(
                f"Just added {data_manager.yesterday} to CSV and set threshhold to {data_manager.threshold}%"
            )
            discord_webhook.send_message(
                f"Yesterdays was {data_manager.current_percentage - 100}% compared to the last 7 days"
            )

        if not fund_manager.bought_this_month:
            if data_manager.is_price_low_enough():
                fund_manager.buy()
                discord_webhook.send_message(f"Bought Coin")

        time.sleep(10)
