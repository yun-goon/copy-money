import time

from core.upload_data import Get_data

import threading
import time
import pyupbit

class main():
    def __init__(self):
        print('coin trading program')
        self.prosess = prosess()
        self.prosess.wallet_loop()

class prosess():
    def __init__(self):
        self.up = Get_data()

    def wallet_loop(self):
        threading.Thread(target=self.up.get_wallet())
        while True:
            print('operating')
            time.sleep(1)


if __name__=='__main__':
    Main = main()