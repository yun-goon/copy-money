# {
#   "access_key": "발급 받은 acccess key (필수)",
#   "nonce": "무작위의 UUID 문자열 (필수)",
#   "query_hash": "해싱된 query string (파라미터가 있을 경우 필수)",
#   "query_hash_alg": "query_hash를 생성하는 데에 사용한 알고리즘 (기본값 : SHA512)"
# }
#
# # 입력없는요청
# import jwt   # PyJWT
# import uuid
#
# payload = {
#     'access_key': '발급받은 Access Key',
#     'nonce': str(uuid.uuid4()),
# }
#
# jwt_token = jwt.encode(payload, '발급받은 Secret Key')
# authorization_token = 'Bearer {}'.format(jwt_token)
#
# # --------------------------------------------------------
#
# # 입력있는 요청
# import jwt  # PyJWT
# import uuid
# import hashlib
# from urllib.parse import urlencode
#
# # query는 dict 타입입니다.
# m = hashlib.sha512()
# m.update(urlencode(query).encode())
# query_hash = m.hexdigest()
#
# payload = {
#     'access_key': '발급받은 Access Key',
#     'nonce': str(uuid.uuid4()),
#     'query_hash': query_hash,
#     'query_hash_alg': 'SHA512',
# }
#
# jwt_token = jwt.encode(payload, '발급받은 Secret Key')
# authorization_token = 'Bearer {}'.format(jwt_token)

# ----------------------------------------------------------------

# 전체 계좌조회
import os
import time

# import jwt
# import uuid
# import hashlib
# from urllib.parse import urlencode
#
# import requests
# import threading
# import time
#
# def account_loop():
#     while(True):
#         time.sleep(5)
#         access_key = 'ySWg8zG5UTmuP0mEZuAdwNNCah2Lt8F6qLQckwcM'
#         secret_key = 'LOXTJLbJ08ckNwj0Z3Zu5SPpcjynEPTTvpv9zAXw'
#         server_url = 'https://api.upbit.com'
#
#         payload = {
#             'access_key': access_key,
#             'nonce': str(uuid.uuid4()),
#         }
#
#         jwt_token = jwt.encode(payload, secret_key)
#         authorize_token = 'Bearer {}'.format(jwt_token)
#         headers = {"Authorization": authorize_token}
#
#         res = requests.get(server_url + "/v1/accounts", headers=headers)
#
#         print(res.json())
#
# def test_loop():
#     while (True):
#         print('a')
#         time.sleep(2)
#
# threading.Thread(target=account_loop).start()
# threading.Thread(target=test_loop()).start()

# -----------------------------------------------------------------------------

# 실시간 데이터 받기
# import websockets
# import asyncio
# import json
#
# async def upbit_websocket():
#     async with websockets.connect("wss://api.upbit.com/websocket/v1", ping_interval=None) as wb:
#         await wb.send('[{"ticket":"test"},{"type":"trade","codes":["KRW-BTC","BTC-BCH"]},{"format":"SIMPLE"}]')
#         while(True):
#             result = await wb.recv()
#             print(json.loads(result))
#
# loop = asyncio.get_event_loop()
# asyncio.ensure_future(upbit_websocket())
# loop.run_forever()

# 2번째방법
# import websockets
# import asyncio
# import json
#
# async def upbit_websocket():
#     websocket = await websockets.connect("wss://api.upbit.com/websocket/v1", ping_interval=None)
#     await websocket.send(json.dumps([{"ticket":"test"},{"type":"trade","codes":["KRW-BTC","BTC-BCH"]},{"format":"SIMPLE"}]))
#
#     while True:
#         if websocket.open:
#             result = await websocket.recv()
#             print(json.loads(result))
#         else:
#             print('disconnect')
#
# loop = asyncio.get_event_loop()
# asyncio.ensure_future(upbit_websocket())
# loop.run_forever()

# -----------------------------------------------------------------------

# 주문

import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests

access_key = 'ySWg8zG5UTmuP0mEZuAdwNNCah2Lt8F6qLQckwcM'
secret_key = 'LOXTJLbJ08ckNwj0Z3Zu5SPpcjynEPTTvpv9zAXw'
server_url = 'https://api.upbit.com'

query = {
    'market': 'KRW-BTC',
    'side': 'bid',
    'volume': '0.01',
    'price': '100.0',
    'ord_type': 'limit',
}
query_string = urlencode(query).encode()

m = hashlib.sha512()
m.update(query_string)
query_hash = m.hexdigest()

payload = {
    'access_key': access_key,
    'nonce': str(uuid.uuid4()),
    'query_hash': query_hash,
    'query_hash_alg': 'SHA512',
}

jwt_token = jwt.encode(payload, secret_key)
authorize_token = 'Bearer {}'.format(jwt_token)
headers = {"Authorization": authorize_token}

res = requests.post(server_url + "/v1/orders", params=query, headers=headers)