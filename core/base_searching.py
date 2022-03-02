import time
import sys
import logging
from decimal import Decimal

import requests
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from multiprocessing import Process, Queue
import multiprocessing as mp
from core.upload_data import Get_data
from core.smart_bot import *
import core.upbit

class Strainer():
    def __init__(self):
        self.gd = Get_data()
        # {'market': 'KRW-BTC', 'korean_name': '비트코인', 'english_name': 'Bitcoin'}
        self.market_coin = self.gd.coin_name_loading()
        self.cnt = 0
        self.len = len(self.market_coin)

    # 실시간으로 스택 쌓는곳
    def producer(self, q):
        while True:
            # 어디까지 했는지 확인 (하나마다 번호부여 list)
            if self.cnt == self.len:  # 마지막 코인까지 왔는지
                self.cnt = 0
            else:  # 아니면 다음꺼
                self.cnt += 1

            coin = self.market_coin[self.cnt]
            result = self.searching(coin)
            q.put(result)

            time.sleep(1)


    # 1개씩 조건에 맞는지 찾아볼때 쓰레드 이용하기위한 클래스
    def searching(self, market):
        # 일봉 분봉데이터 불러오기
        self.min_data = self.gd.candle_data_rest(type='1', market=market, count=30)
        self.day_data = self.gd.candle_data_rest(type='days', market=market, count=30)

        target_item = market
        indicator_data = self.gd.load_indicator(target_item, '1', 200, 5, ['RSI', 'MFI', 'MACD', 'WILLIAMS', 'CANDLE'])

        #target_items = core.upbit.get_items('KRW', '').

        rsi = indicator_data['RSI']
        mfi = indicator_data['MFI']
        macd = indicator_data['MACD']
        williams = indicator_data['WILLIAMS']


        rsi_val = False
        mfi_val = False
        ocl_val = False
        williams_val = False

        if 'CANDLE' not in indicator_data or len(indicator_data['CANDLE']) < 200:
            logging.info('캔들 데이터 부족으로 데이터 산출 불가...[' + str(target_item['market']) + ']')

        '''
        print('rsi',rsi[0]['RSI'])
        print('mfi',mfi[0]['MFI'])
        print('macd',macd[0]['OCL'])
        print('wiilams',williams[0]['W'])
    
        '''
        if (Decimal(str(rsi[0]['RSI'])) > Decimal(str(rsi[1]['RSI'])) > Decimal(str(rsi[2]['RSI']))
                and Decimal(str(rsi[3]['RSI'])) > Decimal(str(rsi[2]['RSI']))
                and Decimal(str(rsi[2]['RSI'])) < Decimal(str(300))):
            rsi_val = True
            return f'{target_item} : rsi good'

        if (Decimal(str(mfi[0]['MFI'])) > Decimal(str(mfi[1]['MFI'])) > Decimal(str(mfi[2]['MFI']))
                and Decimal(str(mfi[3]['MFI'])) > Decimal(str(mfi[2]['MFI']))
                and Decimal(str(mfi[2]['MFI'])) < Decimal(str(30))):
            mfi_val = True
            return f'{target_item} : mfi good'

        if (Decimal(str(macd[0]['OCL'])) > Decimal(str(macd[1]['OCL'])) > Decimal(str(macd[2]['OCL']))
                and Decimal(str(macd[3]['OCL'])) > Decimal(str(macd[2]['OCL']))
                and Decimal(str(macd[1]['OCL'])) < Decimal(str(0))
                and Decimal(str(macd[2]['OCL'])) < Decimal(str(0))
                and Decimal(str(macd[3]['OCL'])) < Decimal(str(0))):
            ocl_val = True
            return f'{target_item} : ocl good'

        if (Decimal(str(williams[0]['W'])) > Decimal(str(williams[1]['W'])) > Decimal(str(williams[2]['W']))
                and Decimal(str(williams[3]['W'])) > Decimal(str(williams[2]['W']))
                and Decimal(str(williams[2]['W'])) < Decimal(str(-80))):
            williams_val = True
            return f'{target_item} : williams good'


        if rsi_val and mfi_val and ocl_val and williams_val:
            return f'{target_item} : 대상 발견'


        # 여기서부터 조건 짜서 넣기
        if True:
            print(market) # 딕션 타입