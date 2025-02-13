import base64
import hashlib
import hmac
import json
import time
import urllib.parse

import requests

from config import BTC_ADDRESS, BUY_AMOUNT, KRAKEN_API_KEY, KRAKEN_PRIVATE_KEY, PAIR


class TransactionApi:
    def __init__(self):
        self.base_url = "https://api.kraken.com"

    def get_nonce(self):
        return str(int(time.time() * 1000))

    def construct_payload(self, type: str):
        if type == "buy":
            payload = json.dumps(
                {
                    "nonce": self.get_nonce(),
                    "ordertype": "market",
                    "type": "buy",
                    "pair": PAIR,
                    "volume": BUY_AMOUNT,
                    "oflags": "viqc",
                }
            )
        elif type == "balance":
            payload = json.dumps(
                {
                    "nonce": self.get_nonce(),
                }
            )
        elif type == "transfer":
            asset = "XXBT"
            payload = json.dumps(
                {
                    "nonce": self.get_nonce(),
                    "asset": asset,
                    "key": "ledger_btc",
                    "amount": self.get_account_balance(asset),
                }
            )
        return payload

    def get_kraken_signature(self, urlpath, data, secret):

        if isinstance(data, str):
            encoded = (str(json.loads(data)["nonce"]) + data).encode()
        else:
            encoded = (str(data["nonce"]) + urllib.parse.urlencode(data)).encode()

        message = urlpath.encode() + hashlib.sha256(encoded).digest()

        mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
        sigdigest = base64.b64encode(mac.digest())
        return sigdigest.decode()

    def add_buy_order(self) -> str:
        payload = self.construct_payload(type="buy")
        endpoint = "/0/private/AddOrder"
        signature = self.get_kraken_signature(endpoint, payload, KRAKEN_PRIVATE_KEY)

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "API-Key": KRAKEN_API_KEY,
            "API-Sign": signature,
        }

        url = self.base_url + endpoint
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            return response.json()["result"]["txid"][0]

        except:
            return "Failed"

    def get_account_balance(self, balance_type) -> str:
        payload = self.construct_payload(type="balance")
        endpoint = "/0/private/Balance"
        signature = self.get_kraken_signature(endpoint, payload, KRAKEN_PRIVATE_KEY)

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "API-Key": KRAKEN_API_KEY,
            "API-Sign": signature,
        }

        url = self.base_url + endpoint
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            return response.json()["result"][balance_type]
        except:
            return "Failed"

    def transfer_funds(self):
        payload = self.construct_payload(type="transfer")
        endpoint = "/0/private/Withdraw"
        signature = self.get_kraken_signature(endpoint, payload, KRAKEN_PRIVATE_KEY)

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "API-Key": KRAKEN_API_KEY,
            "API-Sign": signature,
        }

        url = self.base_url + endpoint
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            return response.json()["result"]["refid"]
        except:
            return "Failed"
