import time
import os
import sys
import logging
import traceback
import math
import datetime

from decimal import Decimal

# 공통 모듈 Import
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from module import upbit

# -----------------------------------------------------------------------------
# - Name : main
# - Desc : 메인
# -----------------------------------------------------------------------------
if __name__ == '__main__':

    # noinspection PyBroadException
    try:
        #while 1:

            upbit.set_loglevel('I')

            indicators = upbit.get_indicator_sel('KRW-BTC', 'D', 200, 100, ['RSI', 'MFI', 'MACD', 'WILLIAMS'])

            # 보조지표 추출
            rsi_data = indicators['RSI']
            mfi_data = indicators['MFI']
            macd_data = indicators['MACD']
            williams_data = indicators['WILLIAMS']

            # logging.info(rsi_data)
            #logging.info(mfi_data)
            # print(macd_data)
            # print(williams_data)
            for i in range(0,100):

                dt = rsi_data[i]['DT']
                rsi = rsi_data[i]['RSI']
                mfi = mfi_data[i]['MFI']
                macd= macd_data[i]['MACD']
                r = williams_data[i]['W']
                now = datetime.datetime.now()


                list_index = ['TIME','RSI','MFI','MACD','R%']
                list =[]
                line=[]
                line.append(dt)
                line.append(rsi)
                line.append(mfi)
                line.append(macd)
                line.append(r)

                list.append(line)

                df=pd.DataFrame(list, columns=list_index)

                if not os.path.exists('indicator.csv'):
                    df.to_csv('indicator.csv', index=False, mode='w', encoding='utf-8-sig')
                else:
                    df.to_csv('indicator.csv', index=False, mode='a', encoding='utf-8-sig', header=False)


            # time.sleep(60)





    except KeyboardInterrupt:
        logging.error("KeyboardInterrupt Exception 발생!")
        logging.error(traceback.format_exc())
        sys.exit(-100)

    except Exception:
        logging.error("Exception 발생!")
        logging.error(traceback.format_exc())
        sys.exit(-200)