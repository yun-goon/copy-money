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

    # 1개씩 조건에 맞는지 찾아볼때 쓰레드 이용하기위한 클래스
    class Worker(threading.Thread):
        def __init__(self, market, gd):                         # 코인명과 Get_data 클래스 위치 가져옴
            super().__init__()
            self.market = market                                # 클래스 내 전체에서 변수 사용하기위해
            self.gd = gd

        def run(self):
            # 일봉 분봉데이터 불러오기
            self.min_data = self.gd.candle_data_rest(type='1', market=self.market, count=30)
            self.day_data = self.gd.candle_data_rest(type='days', market=self.market, count=30)

            # 여기서부터 조건 짜서 넣기
            if True:
                print(self.market)

    # 다음 서칭코인 체크
    def search_routine(self):
        # 어디까지 했는지 확인 (하나마다 번호부여 list)
        if self.cnt == self.len:                                # 마지막 코인까지 왔는지
            self.cnt = 0
        else:                                                   # 아니면 다음꺼
            self.cnt +=1

        coin = self.market_coin[self.cnt]
        t = self.Worker(coin, self.gd)                          # thread 준비
        t.start()                                               # sub thread의 run 메서드를 호출