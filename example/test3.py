import requests
import json

url = "https://api.upbit.com/v1/candles/days?market=KRW-BTC&count=200&convertingPriceUnit=KRW"

headers = {"Accept": "application/json"}

response = requests.request("GET", url, headers=headers)
result = json.loads(response.text)
print(result)