import pandas as pd
import pyupbit

# print(pyupbit.Upbit)

# # 모든 종목 코드 확인
# tickers = pyupbit.get_tickers()
# print(tickers)

# # KRW로 표기된 종목의 코드 확인
tickers = pyupbit.get_tickers(fiat="KRW")
print(tickers)

# 개별 가격 조회
price_KRW = pyupbit.get_current_price(tickers)

price = list(price_KRW.values())
print(price)
#print("\nBTC : {0:>10,} 원".format(int(price_KRW["KRW-BTC"]))) # 딕셔너리 type
#print("ETH : {0:>10,} 원".format(int(price_KRW["KRW-ETH"])))
#print("XRP : {0:>10,} 원".format(int(price_KRW["KRW-XRP"])))

# 아래와 같이 BTC로도 가격 조회가 가능함
#price_BTC = pyupbit.get_current_price("BTC-ETH")
#print("ETH : {} BTC\n".format(price_BTC))

print(len(tickers))
print(len(price))