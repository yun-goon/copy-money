import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, QObject, pyqtSignal
#사용자 정의 시그널 사용을 위한 클래스 정의

class CustomSignal(QObject):
    signal = pyqtSignal(int, str)
    #반드시 클래스 변수로 선언할 것

    def run(self):
        tempstr = "emit으로 전달"
        for i in range(1, 11):
            self.signal.emit(i, tempstr)
            #customFunc 메서드 실행시 signal의 emit 메서드사용

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        customsignal = CustomSignal()
        #Mysignal 클래스의 객체 선언
        customsignal.signal.connect(self.funcEmit)
        #객체에 대한시그널 및 슬롯 설정
        customsignal.run()
        #객체의 customFunc 메서드 실행
        # #customFunc에서 emit 메서드 실행시 GUI에서 받음.
        @pyqtSlot(int, str)
        def funcEmit(self, i, tempstr):
            self.i = i
            #emit을 통해 받은 값을 GUI 객체 변수에 저장
            self.tempstr = tempstr
            print(str(self.i)+"번째 출력 : ", self.tempstr)
            #출력해보기

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()