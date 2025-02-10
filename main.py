import time

from data_manager import DataManger
from discord_messenger import DiscordWebhook


if __name__ == "__main__":
    data_manager = DataManger()
    discord_webhook = DiscordWebhook()
    print("DataManager started")
    while True:
        if data_manager.is_yesterday_missing():
            data_manager.add_yesterday()
        if data_manager.is_price_low_enough():
            discord_webhook.send_message(f"Bought at {data_manager.last_buy}")
        time.sleep(10)




