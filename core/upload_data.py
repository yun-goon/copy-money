import pyupbit
import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import privacy as pr
import pandas as pd
import requests
import websockets
import asyncio
import json

class Get_data():
    def __init__(self):
        self.access_key = pr.access_key
        self.secret_key = pr.access_key
        self.server_url = 'http://api.upbit.com'

    # 계좌 코인정보
    def get_wallet(self):
        payload = {
            'access_key': self.access_key,
            'nonce': str(uuid.uuid4()),
        }

        jwt_token = jwt.encode(payload, self.secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}

        res = requests.get(self.server_url + "/v1/accounts", headers=headers)

        print(res.json())

    # 주문 넣기
    def order(self, market, side, volume, price, ord_type):
        '''
        query = {
            'market': 'KRW-BTC',
            'side': 'bid':매수 , ask:매도,
            'volume': '0.01',
            'price': '100.0',
            'ord_type': 'limit:지정가 , price:시장가매수 , market:시장가매도',
        }'''
        query = {
            'market': market,
            'side': side,
            'volume': volume,
            'price': price,
            'ord_type': ord_type,
        }
        query_string = urlencode(query).encode()

        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()

        payload = {
            'access_key': self.access_key,
            'nonce': str(uuid.uuid4()),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512',
        }

        jwt_token = jwt.encode(payload, self.secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}

        res = requests.post(self.server_url + "/v1/orders", params=query, headers=headers)

    # 주문 정보 조회
    def order_check(self, market):
        query = {
            'market': market,
        }
        query_string = urlencode(query).encode()

        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()

        payload = {
            'access_key': self.access_key,
            'nonce': str(uuid.uuid4()),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512',
        }

        jwt_token = jwt.encode(payload, self.secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}

        res = requests.get(self.server_url + "/v1/orders/chance", params=query, headers=headers)

        print(res.json())

    # coin 이름 불러오기
    def market_data(self):
        url = "https://api.upbit.com/v1/market/all?isDetails=false"

        headers = {"Accept": "application/json"}

        response = requests.request("GET", url, headers=headers)

        print(response.text)

    # coin 차트 데이터 불러오기
    def candle_data_rest(self, type, market, count):
        '''

        :param type: days , minutes , weeks , months
        :param market: KRW - BTC
        :param count: candle count
        :return:
        '''
        url = f"https://api.upbit.com/v1/candles/{type}?market=%20{market}&count={count}&convertingPriceUnit=KRW"

        headers = {"Accept": "application/json"}

        response = requests.request("GET", url, headers=headers)

        print(response.text)

    # 실시간 체결 데이터 조회 (1개)
    def Trade_data_socket(self, market):
        async def upbit_websocket():
            websocket = await websockets.connect("wss://api.upbit.com/websocket/v1", ping_interval=None)
            await websocket.send(json.dumps([{"ticket":"UNIQUE_TICKET"},{"type":"trade","codes":[market]}]))

            while True:
                if websocket.open:
                    result = await websocket.recv()
                    result = json.loads(result)

                    # 수신시 행동
                    self.trade_data_action(result)
                else:
                    print('disconnect')

        # 실제 실시간 조회시 사용
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(upbit_websocket())
        loop.run_forever()

    # 실시간 체결데이터 수신시 action   -> 코딩 필요
    def trade_data_action(self, data):
        print(data)