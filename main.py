import sys
import pyupbit
from PyQt5 import uic
from core.upload_data import Get_data
from core.base_searching import Strainer
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

form_class = uic.loadUiType("coin.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.gd = Get_data() #upload_data를 gd로 바꿈

        self.start = Strainer() # base_searching을 start로
        self.price_list={}

        # 상태바 타이머
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.timeout)

        # self.pushButton.clicked.connect(self.start.search_routine)
        self.pushButton.clicked.connect(self.ButtonstartPush)

    def timeout(self):
        current_time = QTime.currentTime()

        text_time = current_time.toString("hh:mm:ss")
        time_msg = "현재시간: " + text_time

        self.statusbar.showMessage(time_msg + " | Yun & Kim")

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
            
            ## QTableWidget값은 str값이 들어가야함

if __name__ == "__main__":
    # Main process
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()
