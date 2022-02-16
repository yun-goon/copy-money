import os
import jwt
import uuid
import hashlib
import privacy as pr
from ast import literal_eval
from urllib.parse import urlencode
import pyupbit
import json
import math

import requests

access_key = pr.access_key
secret_key = pr.secret_key
server_url = 'http://api.upbit.com'

payload = {
    'access_key': access_key,
    'nonce': str(uuid.uuid4()),
}

jwt_token = jwt.encode(payload, secret_key)
authorize_token = 'Bearer {}'.format(jwt_token)
headers = {"Authorization": authorize_token}

res = requests.get(server_url + "/v1/accounts", headers=headers)

test = res.text
dict = json.loads(test)
test2 = 'KRW-BORA'
list=[]
list_EA=[]
list_PA=[]

for i in range(len(dict)):
    bought_number = float(dict[i]['balance'])
    bought_price = float(dict[i]['avg_buy_price'])
    PA = bought_price * bought_number
    list_PA.append(PA)
    list.append('KRW-'+dict[i]['currency'])
print(dict)



