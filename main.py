import pyupbit
import os
import sys
import time
import logging
import requests
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
from pandas.io.json import json_normalize
import pandas as pd
from core.upload_data import Get_data
from core.base_searching import Strainer
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import json
import plotly.graph_objects as go
from multiprocessing import Process, Queue
import multiprocessing as mp

form_class = uic.loadUiType("coin.ui")[0]

# 스택 받아올 함수실행 클래스
class Sub_main():
    def __init__(self, q, start):
        start.producer(q)

# 스택 받아오는곳 분류해서 메인 ui로 데이터보냄
class Get_stack(QThread):
    poped = pyqtSignal(str)

    def __init__(self, q):
        super().__init__()
        self.q = q

    def run(self):
        while True:
            if not self.q.empty():
                data = self.q.get()
                print(data)
                if data:
                    self.poped.emit(data)

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.gd = Get_data() #upload_data를 gd로 바꿈

        self.start = Strainer() # base_searching을 start로


        self.notice_2.append('프로그램 시작\n')
        self.notice_2.append('업비트 공지사항 크롤링 중...')
        notice_list = self.gd.upbit_notice(5)  # 프로그램 시작시 상위 5개 upbit 공지사항 업데이트
        if notice_list:
            for i in notice_list:
                self.notice_2.append(i)

        # 조건검색 체크 멀티프로세싱으로 돌리기
        q = Queue()
        # producer process
        p = Process(name="producer", target=Sub_main, args=(q, self.start,), daemon=True)
        p.start()

        # thread for data consumer
        self.consumer = Get_stack(q)
        self.consumer.poped.connect(self.print_data)
        self.consumer.start()


        # 상태바 타이머
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.timeout) #timer를 timeout에 연결

        # 5초 타이머
        self.timer2 = QTimer(self)
        self.timer2.start(5000)
        self.timer2.timeout.connect(self.timeout2) # timer2를 timeout2에 연결

        # self.pushButton.clicked.connect(self.start.search_routine)
        self.pushButton.clicked.connect(self.ButtonstartPush)

        # QComboBox upload 하고 아이템 선택시 이벤트 (코인명, 차트유형, 봉개수)
        self.coin_list_upload()
        self.coin_list_cbox.currentIndexChanged.connect(self.coin_choice)
        self.coin_list_cbox_2.currentIndexChanged.connect(self.coin_choice)
        self.coin_list_cbox_3.currentIndexChanged.connect(self.coin_choice)

    @pyqtSlot(str)
    def print_data(self, data):
        # if self.checkBox.isChecked():  # 감시여부 체크시
        self.searched_coin.append(data)


    def timeout(self):
        # 맨아래 시간표시
        current_time = QTime.currentTime()

        text_time = current_time.toString("hh:mm:ss")
        time_msg = "현재시간: " + text_time

        self.statusbar.showMessage(time_msg + " | Yun & Kim")

    def timeout2(self):
        if self.checkBox.isChecked():       # 감시여부 체크시
            self.ButtonstartPush()          # 5초마다 버튼 누른효과

        notice_list = self.gd.upbit_notice()  # upbit 공지사항 업데이트
        if notice_list:
            for i in notice_list:
                self.notice_2.append(i)

    def coin_choice(self):
        '''
        type, market, count
        '''
        coin = self.coin_list_cbox.currentText()
        type = self.coin_list_cbox_2.currentText()
        count = self.coin_list_cbox_3.currentText()
        self.notice_2.append(coin)

        # 차트 업로드
        df = self.gd.candle_data_rest(type, coin, int(count), low=1)                # json 그대로 가져오기
        df = pd.json_normalize(df.json())  # Results contain the required data      # 준비
        fig = go.Figure(data=[go.Candlestick(x=df['candle_date_time_kst'],          # 데이터 넣기
                                             open=df['opening_price'],
                                             high=df['high_price'],
                                             low=df['low_price'],
                                             close=df['trade_price'])])
        # x축 type을 카테고리 형으로 설정, 순서를 오름차순으로 날짜순서가 되도록 설정
        fig.layout = dict(title=coin,
                          xaxis=dict(type="category",
                                     categoryorder='category ascending'))           # 어떻게 보일지 설정
        fig.update_xaxes(nticks=5)                                                  # x축 5단위 표시
        self.webEngineView.setHtml(fig.to_html(include_plotlyjs='cdn'))             # ui에 표시

    # 코인 이름을 ui에 표시
    def coin_list_upload(self):
        for i in range(len(self.start.market_coin)):
            self.coin_list_cbox.addItem(self.start.market_coin[i])

    def MyWalletLoading(self):
        wallet = self.gd.get_wallet()
        walletDict = json.loads(wallet.text)
        del walletDict[0] # KRW_KRW 값 삭제
        list_currency = [] # 보유 코인 이름 목록
        list_now_cost = [] # 보유 코인의 현재 가격 목록
        list_return = [] # 수익률 목록

        # list_now_cost.append(walletDict[0]['currency'])
        for i in range(len(walletDict)): #코인 이름 목록 만드는거
            list_currency.append('KRW-' + walletDict[i]['currency'])
        for j in range(len(list_currency)): # 코인 가격 목록 만드는거
            prices = pyupbit.get_current_price(list_currency[j])
            list_now_cost.append(prices)

            bought_number = float(walletDict[j]['balance']) #산 갯수
            bought_price = float(walletDict[j]['avg_buy_price']) #매수평균가
            # PA: 매수금액(매수평균가 * 보유수량)
            PA = bought_price * bought_number
            # EA : 평가금액(현재가 * 보유수량)
            EA = prices * bought_number
            returncost = EA/PA*100 # 수익률 계산, 결과물 -+로 바꿀려면 여기
            list_return.append(returncost)

        self.wallet.setRowCount(len(list_currency)) #칸수 정하기

        for i in range(len(list_currency)): #ui에 넣는거
            self.wallet.setItem(i, 0, QTableWidgetItem(list_currency[i]))
            self.wallet.setItem(i, 1, QTableWidgetItem(str(list_now_cost[i])))
            self.wallet.setItem(i, 2 ,QTableWidgetItem(str(list_return[i])))

    # 일단 모든 코인 현재가 tablewidget에 표시
    def ButtonstartPush(self):

        self.MyWalletLoading()

        tickers = self.start.market_coin #list 타입, 코인이름 불러오기
        prices_KRW =  pyupbit.get_current_price(tickers) # dict 타입 /  나 이거 밖에서 어떻게 들고오는지 모르겠음
        prices = list(prices_KRW.values()) #리스트 타입으로 변환
        self.coinlist.setRowCount(len(tickers)) # ui 몇줄일지설정

        for i, ticker in enumerate(tickers):
            coinName =QTableWidgetItem(ticker)
            self.coinlist.setItem(i,0,coinName)
            self.coinlist.setItem(i, 1, QTableWidgetItem(str(prices[i])))
            # 위에 두 방법중 밑에 방법이 나을듯?
            # 나도 밑에껄로함

            ## QTableWidget값은 str값이 들어가야함


if __name__ == "__main__":
    # Main process
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()
