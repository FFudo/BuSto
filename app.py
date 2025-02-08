import time
from datetime import datetime, timedelta

import requests

# url = "https://api.kraken.com/0/public/Ticker"

# param = {"pair": "BTCEUR"}

# payload = {}
# headers = {"Accept": "application/json"}

# response = requests.request("GET", url, headers=headers, data=payload, params=param)

now = datetime.now()
today_at_midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)

yesterday_at_midnight = today_at_midnight - timedelta(days=1)
seven_days_ago_at_midnight = today_at_midnight - timedelta(days=7)

today_unix = int(time.mktime(today_at_midnight.timetuple()))
yesterday_unix = int(time.mktime(yesterday_at_midnight.timetuple()))
seven_days_ago_unix = int(time.mktime(seven_days_ago_at_midnight.timetuple()))

ohlc_url = "https://api.kraken.com/0/public/OHLC"

ohlc_params = {"pair": "BTCEUR", "interval": 1440, "since": seven_days_ago_unix}
payload = {}
headers = {"Accept": "application/json"}

response = requests.request(
    "GET",
    url=ohlc_url,
    headers=headers,
    data=payload,
    params=ohlc_params,
)

print(response.json())
