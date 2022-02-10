import os
import sys
import logging
import math
import traceback

# 공통 모듈 Import
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from module import upbit as upbit  # noqa

# -----------------------------------------------------------------------------
# - Name : main
# - Desc : 메인
# -----------------------------------------------------------------------------
if __name__ == '__main__':

    # noinspection PyBroadException
    try:

        print("***** USAGE ******")
        print("[1] 로그레벨(D:DEBUG, E:ERROR, 그외:INFO)")

        # 로그레벨(D:DEBUG, E:ERROR, 그외:INFO)
        upbit.set_loglevel('I')

        # ---------------------------------------------------------------------
        # Logic Start!
        # ---------------------------------------------------------------------
        # 보유 종목 리스트 조회
        rsi_data = upbit.get_rsi('KRW-BTC', '30', '200')
        logging.info(rsi_data)


    except KeyboardInterrupt:
        logging.error("KeyboardInterrupt Exception 발생!")
        logging.error(traceback.format_exc())
        sys.exit(1)

    except Exception:
        logging.error("Exception 발생!")
        logging.error(traceback.format_exc())
        sys.exit(1)

rsi_data = upbit.get_rsi('KRW-BTC', '30', '200')