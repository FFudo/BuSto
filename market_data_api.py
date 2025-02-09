import requests


class MarketApi:
    def __init__(self):
        self.base_url = "https://api.kraken.com/0/public/"

    def request_ohcl_data(self, since: int, pair="BTCEUR"):
        ohlc_url = self.base_url + "OHLC"

        ohlc_params = {
            "pair": pair,
            "interval": 1440,
            "since": since,
        }

        payload = {}
        headers = {"Accept": "application/json"}

        response = requests.request(
            "GET",
            url=ohlc_url,
            headers=headers,
            data=payload,
            params=ohlc_params,
        )
        return response.json()["result"]["XXBTZEUR"][0]
