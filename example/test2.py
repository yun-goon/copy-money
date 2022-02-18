from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
import plotly.express as px
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


class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.button = QtWidgets.QPushButton('Plot', self)
        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        vlayout = QtWidgets.QVBoxLayout(self)
        vlayout.addWidget(self.button, alignment=QtCore.Qt.AlignHCenter)
        vlayout.addWidget(self.browser)
        self.button.clicked.connect(self.show_graph)
        self.resize(1000,800)

    def show_graph(self):
        headers = {"Accept": "application/json"}

        response = requests.request("GET", "https://api.upbit.com/v1/candles/days?market=KRW-BTC&count=100",
                                    headers=headers)
        response = json.loads(response.text)
        response = json.dumps(response)
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
                          xaxis=dict(type="category",
                                     categoryorder='category ascending'))
        fig.update_xaxes(nticks=5)
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = Widget()
    widget.show()
    app.exec()