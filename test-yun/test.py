import time
import os
import sys
import logging
import traceback
import math

from decimal import Decimal

# 공통 모듈 Import
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from module import upbit

# -----------------------------------------------------------------------------
# - Name : main
# - Desc : 메인
# -----------------------------------------------------------------------------
if __name__ == '__main__':

    # noinspection PyBroadException
    try:

        upbit.set_loglevel('I')

        indicators = upbit.get_indicator_sel('KRW-BTC', '60', 200, 5, ['RSI', 'CANDLE'])

        # 보조지표 추출
        rsi_data = indicators['RSI']
        candles = indicators['CANDLE']

        logging.info(rsi_data)
        logging.info(candles)

    except KeyboardInterrupt:
        logging.error("KeyboardInterrupt Exception 발생!")
        logging.error(traceback.format_exc())
        sys.exit(-100)

    except Exception:
        logging.error("Exception 발생!")
        logging.error(traceback.format_exc())
        sys.exit(-200)