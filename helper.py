import time
from datetime import datetime


def into_unix(day):
    return int(time.mktime(day.timetuple()))


def into_day(time):
    return datetime.fromtimestamp(time).strftime("%Y-%m-%d")
