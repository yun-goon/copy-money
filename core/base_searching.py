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
        self.market_coin = self.gd.market_data()
        self.list = {}

    # 1초마다 코인돌려보기
    def search_routine(self,q):
        while(True):
            for market in self.market_coin:
                self.specific_pattern(market,q)
                time.sleep(1)

    # 우리가 원하는 조건
    def specific_pattern(self,market,q):
        self.min_data = self.gd.candle_data_rest(type='1', market=market, count=30)
        self.day_data = self.gd.candle_data_rest(type='days', market=market, count=30)


        # 여기서부터 조건 짜서 넣기
        if True:
            q.put(market['market'])