import sys
import pyupbit
from PyQt5 import uic
from core.upload_data import Get_data
from core.base_searching import Strainer
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from multiprocessing import Process, Queue
import multiprocessing as mp
import datetime
import time

form_class = uic.loadUiType("coin.ui")[0]

class Consumer(QThread):
    poped = pyqtSignal(str)

    def __init__(self, q):
        super().__init__()
        self.q = q

    def run(self):
        while True:
            if not self.q.empty():
                data = self.q.get()
                self.poped.emit(data)
                print(data)

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.gd = Get_data() #upload_data를 gd로 바꿈

        self.start = Strainer() # base_searching을 start로
        self.price_list={}

        self.notice_2.append('프로그램 시작')

        # 상태바 타이머
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.timeout)

        # self.pushButton.clicked.connect(self.start.search_routine)
        self.pushButton.clicked.connect(self.ButtonstartPush)

        # QComboBox upload 하고 아이템 선택시 이벤트
        self.coin_list_upload()
        self.coin_list_cbox.currentIndexChanged.connect(self.coin_choice)

        q = Queue()
        # thread for data consumer
        self.consumer = Consumer(q)
        self.consumer.poped.connect(self.print_data)
        self.consumer.start()

    @pyqtSlot(str)
    def print_data(self, data):
        self.statusBar().showMessage(data)

    def timeout(self):
        current_time = QTime.currentTime()

        text_time = current_time.toString("hh:mm:ss")
        time_msg = "현재시간: " + text_time

        self.statusbar.showMessage(time_msg + " | Yun & Kim")

    # 멀티프로세싱 코인찾기
    def search_start(self):
        q = Queue()

        # thread for data consumer
        self.consumer = Consumer(q)
        self.consumer.poped.connect(self.print_data)
        self.consumer.start()

        # producer process
        p = Process(name="producer", target=self.start.search_routine, args=(q,), daemon=True)
        p.start()

    # 코인 선택시 실행되는 함수
    def coin_choice(self):
        coin = self.coin_list_cbox.currentText()
        self.notice_2.append(coin)

    def coin_list_upload(self):
        print(self.start.market_coin[1]['market'])
        for i in range(len(self.start.market_coin)):
            self.coin_list_cbox.addItem(self.start.market_coin[i]['market'])

    # 일단 모든 코인 현재가 tablewidget에 표시
    def ButtonstartPush(self):
        self.gd = Get_data()
        tickers = self.gd.coin_name_loading()
        prices_KRW =  pyupbit.get_current_price(tickers) # 나 이거 밖에서 어떻게 들고오는지 모르겠음
        prices = list(prices_KRW.values())
        self.coinlist.setRowCount(len(tickers)) # ui 몇줄일지설정

        for i, ticker in enumerate(tickers):
            coinName =QTableWidgetItem(ticker)
            self.coinlist.setItem(i,0,coinName) 
            self.coinlist.setItem(i, 1, QTableWidgetItem(str(prices[i])))
            # 위에 두 방법중 밑에 방법이 나을듯?
            # 나도 밑에껄로함
            
            ## QTableWidget값은 str값이 들어가야함

        self.search_start()

if __name__ == "__main__":
    # Main process
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()
