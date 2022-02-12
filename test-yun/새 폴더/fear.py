import requests
import json
import pandas as pd
import datetime



url = "https://api.alternative.me/fng/?limit="


def fear_day():
    _url = url + "1"
    res = requests.request("GET", _url);

    parsed = json.loads(res.text)
    data = parsed["data"]

    return data[0]["value"]


def fear_yester():
    _url = url + "2"
    res = requests.request("GET", _url);

    parsed = json.loads(res.text)
    data = parsed["data"]

    return data[1]["value"]


def fear_twodaysago():
    _url = url + "3"
    res = requests.request("GET", _url);

    parsed = json.loads(res.text)
    data = parsed["data"]

    return data[2]["value"]


def fear_week():
    _url = url + "7"
    res = requests.request("GET", _url);

    parsed = json.loads(res.text)
    data = parsed["data"]

    sum = 0
    for index, value in enumerate(data):
        sum += int(value["value"])

    return sum / 7


def fear_month():
    _url = url + "30"
    res = requests.request("GET", _url);

    parsed = json.loads(res.text)
    data = parsed["data"]

    sum = 0
    for index, value in enumerate(data):
        sum += int(value["value"])

    return sum / 30

now= datetime.datetime.now()
fd = fear_day()
fy = fear_yester()
fw= fear_week()
ft= fear_twodaysago()
fm= fear_month()

fear_list= ['today_now','day', 'yesterday', 'twodaysago', 'week', 'month']
fear=[]
line=[]
line.append(now)
line.append(fd)
line.append(fy)
line.append(fw)
line.append(ft)
line.append(fm)
fear.append(line)


df=pd.DataFrame(fear, columns=fear_list)
df.to_csv('fear_index.csv',encoding='utf-8-sig')

print(now)
print(fd)