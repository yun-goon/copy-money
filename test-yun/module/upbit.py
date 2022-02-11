import logging
import requests
import time
import smtplib
import jwt
import sys
import uuid
import hashlib
import math
import numpy
import pandas as pd
from datetime import datetime, timedelta
from decimal import Decimal
from urllib.parse import urlencode
import privacy as pr

# Keys
access_key = pr.access_key
secret_key = pr.access_key
server_url = 'https://api.upbit.com'


# -----------------------------------------------------------------------------
# - Name : set_loglevel
# - Desc : 로그레벨 설정
# - Input
#   1) level : 로그레벨
#     1. D(d) : DEBUG
#     2. E(e) : ERROR
#     3. 그외(기본) : INFO
# - Output
# -----------------------------------------------------------------------------
def set_loglevel(level):
    try:

        # ---------------------------------------------------------------------
        # 로그레벨 : DEBUG
        # ---------------------------------------------------------------------
        if level.upper() == "D":
            logging.basicConfig(
                format='[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d]:%(message)s',
                datefmt='%Y/%m/%d %I:%M:%S %p',
                level=logging.DEBUG
            )
        # ---------------------------------------------------------------------
        # 로그레벨 : ERROR
        # ---------------------------------------------------------------------
        elif level.upper() == "E":
            logging.basicConfig(
                format='[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d]:%(message)s',
                datefmt='%Y/%m/%d %I:%M:%S %p',
                level=logging.ERROR
            )
        # ---------------------------------------------------------------------
        # 로그레벨 : INFO
        # ---------------------------------------------------------------------
        else:
            # -----------------------------------------------------------------------------
            # 로깅 설정
            # 로그레벨(DEBUG, INFO, WARNING, ERROR, CRITICAL)
            # -----------------------------------------------------------------------------
            logging.basicConfig(
                format='[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d]:%(message)s',
                datefmt='%Y/%m/%d %I:%M:%S %p',
                level=logging.INFO
            )

    # ----------------------------------------
    # Exception Raise
    # ----------------------------------------
    except Exception:
        raise


# -----------------------------------------------------------------------------
# - Name : send_request
# - Desc : 리퀘스트 처리
# - Input
#   1) reqType : 요청 타입
#   2) reqUrl : 요청 URL
#   3) reqParam : 요청 파라메타
#   4) reqHeader : 요청 헤더
# - Output
#   4) reponse : 응답 데이터
# -----------------------------------------------------------------------------
def send_request(reqType, reqUrl, reqParam, reqHeader):
    try:

        # 요청 가능회수 확보를 위해 기다리는 시간(초)
        err_sleep_time = 0.3

        # 요청에 대한 응답을 받을 때까지 반복 수행
        while True:

            # 요청 처리
            response = requests.request(reqType, reqUrl, params=reqParam, headers=reqHeader)

            # 요청 가능회수 추출
            if 'Remaining-Req' in response.headers:

                hearder_info = response.headers['Remaining-Req']
                start_idx = hearder_info.find("sec=")
                end_idx = len(hearder_info)
                remain_sec = hearder_info[int(start_idx):int(end_idx)].replace('sec=', '')
            else:
                logging.error("헤더 정보 이상")
                logging.error(response.headers)
                break

            # 요청 가능회수가 3개 미만이면 요청 가능회수 확보를 위해 일정시간 대기
            if int(remain_sec) < 3:
                logging.debug("요청 가능회수 한도 도달! 남은횟수:" + str(remain_sec))
                time.sleep(err_sleep_time)

            # 정상 응답
            if response.status_code == 200 or response.status_code == 201:
                break
            # 요청 가능회수 초과인 경우
            elif response.status_code == 429:
                logging.error("요청 가능회수 초과!:" + str(response.status_code))
                time.sleep(err_sleep_time)
            # 그 외 오류
            else:
                logging.error("기타 에러:" + str(response.status_code))
                logging.error(response.status_code)
                break

            # 요청 가능회수 초과 에러 발생시에는 다시 요청
            logging.info("[restRequest] 요청 재처리중...")

        return response

    # ----------------------------------------
    # Exception Raise
    # ----------------------------------------
    except Exception:
        raise


# -----------------------------------------------------------------------------
# - Name : get_candle
# - Desc : 캔들 조회
# - Input
#   1) target_item : 대상 종목
#   2) tick_kind : 캔들 종류 (1, 3, 5, 10, 15, 30, 60, 240 - 분, D-일, W-주, M-월)
#   3) inq_range : 조회 범위
# - Output
#   1) 캔들 정보 배열
# -----------------------------------------------------------------------------
def get_candle(target_item, tick_kind, inq_range):
    try:

        # ----------------------------------------
        # Tick 별 호출 URL 설정
        # ----------------------------------------
        # 분붕
        if tick_kind == "1" or tick_kind == "3" or tick_kind == "5" or tick_kind == "10" or tick_kind == "15" or tick_kind == "30" or tick_kind == "60" or tick_kind == "240":
            target_url = "minutes/" + tick_kind
        # 일봉
        elif tick_kind == "D":
            target_url = "days"
        # 주봉
        elif tick_kind == "W":
            target_url = "weeks"
        # 월봉
        elif tick_kind == "M":
            target_url = "months"
        # 잘못된 입력
        else:
            raise Exception("잘못된 틱 종류:" + str(tick_kind))

        logging.debug(target_url)

        # ----------------------------------------
        # Tick 조회
        # ----------------------------------------
        querystring = {"market": target_item, "count": inq_range}
        res = send_request("GET", server_url + "/v1/candles/" + target_url, querystring, "")
        candle_data = res.json()

        logging.debug(candle_data)

        return candle_data

    # ----------------------------------------
    # Exception Raise
    # ----------------------------------------
    except Exception:
        raise


# -----------------------------------------------------------------------------
# - Name : get_rsi
# - Desc : RSI 조회
# - Input
#   1) candle_data : 캔들 정보
# - Output
#   1) RSI 값
# -----------------------------------------------------------------------------
def get_rsi(candle_datas):
    try:

        # RSI 데이터 리턴용
        rsi_data = []

        # 캔들 데이터만큼 수행
        for candle_data_for in candle_datas:
            df = pd.DataFrame(candle_data_for)
            dfDt = df['candle_date_time_kst'].iloc[::-1]
            df = df.reindex(index=df.index[::-1]).reset_index()

            df['close'] = df["trade_price"]

            # RSI 계산
            def rsi(ohlc: pd.DataFrame, period: int = 14):
                ohlc["close"] = ohlc["close"]
                delta = ohlc["close"].diff()

                up, down = delta.copy(), delta.copy()
                up[up < 0] = 0
                down[down > 0] = 0

                _gain = up.ewm(com=(period - 1), min_periods=period).mean()
                _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()

                RS = _gain / _loss
                return pd.Series(100 - (100 / (1 + RS)), name="RSI")

            rsi = round(rsi(df, 14).iloc[-1], 4)
            rsi_data.append({"type": "RSI", "DT": dfDt[0], "RSI": rsi})

        return rsi_data

    # ----------------------------------------
    # 모든 함수의 공통 부분(Exception 처리)
    # ----------------------------------------
    except Exception:
        raise


# -----------------------------------------------------------------------------
# - Name : get_mfi
# - Desc : MFI 조회
# - Input
#   1) candle_datas : 캔들 정보
# - Output
#   1) MFI 값
# -----------------------------------------------------------------------------
def get_mfi(candle_datas):
    try:

        # MFI 데이터 리턴용
        mfi_list = []

        # 캔들 데이터만큼 수행
        for candle_data_for in candle_datas:

            df = pd.DataFrame(candle_data_for)
            dfDt = df['candle_date_time_kst'].iloc[::-1]

            df['typical_price'] = (df['trade_price'] + df['high_price'] + df['low_price']) / 3
            df['money_flow'] = df['typical_price'] * df['candle_acc_trade_volume']

            positive_mf = 0
            negative_mf = 0

            for i in range(0, 14):

                if df["typical_price"][i] > df["typical_price"][i + 1]:
                    positive_mf = positive_mf + df["money_flow"][i]
                elif df["typical_price"][i] < df["typical_price"][i + 1]:
                    negative_mf = negative_mf + df["money_flow"][i]

            if negative_mf > 0:
                mfi = 100 - (100 / (1 + (positive_mf / negative_mf)))
            else:
                mfi = 100 - (100 / (1 + (positive_mf)))

            mfi_list.append({"type": "MFI", "DT": dfDt[0], "MFI": round(mfi, 4)})

        return mfi_list

    # ----------------------------------------
    # 모든 함수의 공통 부분(Exception 처리)
    # ----------------------------------------
    except Exception:
        raise


# -----------------------------------------------------------------------------
# - Name : get_macd
# - Desc : MACD 조회
# - Input
#   1) candle_datas : 캔들 정보
#   2) loop_cnt : 반복 횟수
# - Output
#   1) MACD 값
# -----------------------------------------------------------------------------
def get_macd(candle_datas, loop_cnt):
    try:

        # MACD 데이터 리턴용
        macd_list = []

        df = pd.DataFrame(candle_datas[0])
        df = df.iloc[::-1]
        df = df['trade_price']

        # MACD 계산
        exp1 = df.ewm(span=12, adjust=False).mean()
        exp2 = df.ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        exp3 = macd.ewm(span=9, adjust=False).mean()

        for i in range(0, int(loop_cnt)):
            macd_list.append(
                {"type": "MACD", "DT": candle_datas[0][i]['candle_date_time_kst'], "MACD": round(macd[i], 4),
                 "SIGNAL": round(exp3[i], 4),
                 "OCL": round(macd[i] - exp3[i], 4)})

        return macd_list

    # ----------------------------------------
    # 모든 함수의 공통 부분(Exception 처리)
    # ----------------------------------------
    except Exception:
        raise


# -----------------------------------------------------------------------------
# - Name : get_bb
# - Desc : 볼린저밴드 조회
# - Input
#   1) candle_datas : 캔들 정보
# - Output
#   1) 볼린저 밴드 값
# -----------------------------------------------------------------------------
def get_bb(candle_datas):
    try:

        # 볼린저밴드 데이터 리턴용
        bb_list = []

        # 캔들 데이터만큼 수행
        for candle_data_for in candle_datas:
            df = pd.DataFrame(candle_data_for)
            dfDt = df['candle_date_time_kst'].iloc[::-1]
            df = df['trade_price'].iloc[::-1]

            # 표준편차(곱)
            unit = 2

            band1 = unit * numpy.std(df[len(df) - 20:len(df)])
            bb_center = numpy.mean(df[len(df) - 20:len(df)])
            band_high = bb_center + band1
            band_low = bb_center - band1

            bb_list.append({"type": "BB", "DT": dfDt[0], "BBH": round(band_high, 4), "BBM": round(bb_center, 4),
                            "BBL": round(band_low, 4)})

        return bb_list


    # ----------------------------------------
    # 모든 함수의 공통 부분(Exception 처리)
    # ----------------------------------------
    except Exception:
        raise


# -----------------------------------------------------------------------------
# - Name : get_indicators
# - Desc : 보조지표 조회
# - Input
#   1) target_item : 대상 종목
#   2) tick_kind : 캔들 종류 (1, 3, 5, 10, 15, 30, 60, 240 - 분, D-일, W-주, M-월)
#   3) inq_range : 캔들 조회 범위
#   4) loop_cnt : 지표 반복계산 횟수
# - Output
#   1) RSI
#   2) MFI
#   3) MACD
#   4) BB
# -----------------------------------------------------------------------------
def get_indicators(target_item, tick_kind, inq_range, loop_cnt):
    try:

        # 보조지표 리턴용
        indicator_data = []

        # 캔들 데이터 조회용
        candle_datas = []

        # 캔들 추출
        candle_data = get_candle(target_item, tick_kind, inq_range)

        # 조회 횟수별 candle 데이터 조합
        for i in range(0, int(loop_cnt)):
            candle_datas.append(candle_data[i:int(len(candle_data))])

        # RSI 정보 조회
        rsi_data = get_rsi(candle_datas)

        # MFI 정보 조회
        mfi_data = get_mfi(candle_datas)

        # MACD 정보 조회
        macd_data = get_macd(candle_datas, loop_cnt)

        # BB 정보 조회
        bb_data = get_bb(candle_datas)

        if len(rsi_data) > 0:
            indicator_data.append(rsi_data)

        if len(mfi_data) > 0:
            indicator_data.append(mfi_data)

        if len(macd_data) > 0:
            indicator_data.append(macd_data)

        if len(bb_data) > 0:
            indicator_data.append(bb_data)

        return indicator_data

    # ----------------------------------------
    # 모든 함수의 공통 부분(Exception 처리)
    # ----------------------------------------
    except Exception:
        raise