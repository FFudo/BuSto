import time

from data_manager import DataManger
from discord_messenger import DiscordWebhook
from fund_manager import FundManager

if __name__ == "__main__":
    data_manager = DataManger()
    fund_manager = FundManager()
    discord_webhook = DiscordWebhook()
    print("DataManager started")
    
    while True:
        data_manager.check_days()

        if data_manager.is_yesterday_missing():
            data_manager.add_yesterday()

        if not fund_manager.bought_this_month:
            if data_manager.is_price_low_enough():
                fund_manager.buy()
                discord_webhook.send_message(f"Bought Coin")
                
        time.sleep(10)
