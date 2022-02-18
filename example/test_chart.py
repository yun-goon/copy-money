import json
import time

import requests
import plotly.graph_objects as go
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# coin 차트 데이터 불러오기
from pandas.io.json import json_normalize

headers = {"Accept": "application/json"}

response = requests.request("GET", "https://api.upbit.com/v1/candles/days?market=KRW-BTC&count=100", headers=headers)

print(response.json())
df = json_normalize(response.json())  # Results contain the required data
print(df)

stock_name = '비트코인'

fig = go.Figure(data=[go.Candlestick(x=df['candle_date_time_kst'],
                                    open=df['opening_price'],
                                    high=df['high_price'],
                                    low=df['low_price'],
                                    close=df['trade_price'])])
# x축 type을 카테고리 형으로 설정, 순서를 오름차순으로 날짜순서가 되도록 설정
fig.layout = dict(title=stock_name,
                       xaxis = dict(type="category",
                                    categoryorder='category ascending'))
fig.update_xaxes(nticks=5)
fig.write_image('11_plotly.png')
fig.show()

from PIL import Image

image = Image.open("../11_plotly.png")

image.show()