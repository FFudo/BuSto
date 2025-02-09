import time

from data_manager import DataManger


if __name__ == "__main__":
    data_manager = DataManger()
    print("data manager started")
    while True:
        if data_manager.is_yesterday_missing():
            data_manager.add_yesterday()
        time.sleep(10)




