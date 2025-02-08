import os
import time

import schedule

from data_manager import DataManger

data_manager = DataManger()
schedule.every().day.at("02:00").do(data_manager.add_yesterday())

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(60)
