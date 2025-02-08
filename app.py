import requests

url = "https://api.kraken.com/0/public/Ticker"

param = {"pair": "BTCEUR"}

payload = {}
headers = {"Accept": "application/json"}

response = requests.request("GET", url, headers=headers, data=payload, params=param)

print(response.json())
