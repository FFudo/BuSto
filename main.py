import time

import schedule

from data_manager import DataManger

data_manager = DataManger()
schedule.every().day.at("06:00").do(data_manager.add_yesterday)
print("Check")

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(60)
