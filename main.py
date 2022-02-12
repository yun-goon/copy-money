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
        self.gd = Get_data()

        self.start = Strainer()

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
        self.coinlist.setRowCount(len(tickers))
        for i, ticker in enumerate(tickers):
            coinName =QTableWidgetItem(ticker)
            self.coinlist.setItem(i,0,coinName)

        # print(tickers)


if __name__ == "__main__":
    # Main process
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()

    #tickers=pyupbit.get_tickers(fiat="KRW")
    # print(tickers)
    # print(len(tickers))