import time
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from multiprocessing import Process, Queue
import multiprocessing as mp
from core.upload_data import Get_data
from core.smart_bot import *

class Strainer():
    def __init__(self):
        self.gd = Get_data()
        # {'market': 'KRW-BTC', 'korean_name': '비트코인', 'english_name': 'Bitcoin'}
        self.market_coin = self.gd.market_data()
        self.cnt = 0
        self.len = len(self.market_coin)

    class Worker(threading.Thread):
        def __init__(self, market, gd):
            super().__init__()
            self.market = market  # thread 이름 지정
            self.gd = gd

        def run(self):
            self.min_data = self.gd.candle_data_rest(type='1', market=self.market, count=30)
            self.day_data = self.gd.candle_data_rest(type='days', market=self.market, count=30)

            # 여기서부터 조건 짜서 넣기
            if True:
                print(self.market)

    # 다음 서칭코인 체크
    def search_routine(self):
        # 어디까지 했는지 확인
        if self.cnt == self.len:
            self.cnt = 0
        else:
            self.cnt +=1

        coin = self.market_coin[self.cnt]
        t = self.Worker(coin, self.gd)  # sub thread 생성
        t.start()  # sub thread의 run 메서드를 호출