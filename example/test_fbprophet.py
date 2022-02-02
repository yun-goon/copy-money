import pyupbit
import matplotlib.pyplot as plt
from pykrx import stock
from fbprophet import Prophet
from fbprophet.plot import add_changepoints_to_plot

# BTC 최근 200시간의 데이터 불러옴

df = pyupbit.get_ohlcv("KRW-BTC", interval="minute60")

# 시간(ds)와 종가(y)값만 남김
df = df.reset_index()
df['ds'] = df['index']
df['y'] = df['close']
data = df[['ds', 'y']]

#학습
#튜닝 전
# model = Prophet()
# model.fit(data)


#학습
#튜닝 후
model = Prophet(
    seasonality_mode='multiplicative',
    changepoint_prior_scale=0.5,
    changepoint_range=0.9,
)
model.fit(data)

#24시간 예측
future = model.make_future_dataframe(periods=24, freq='H')

forecast = model.predict(future)

# # 그래프1
fig1 = model.plot(forecast)
a = add_changepoints_to_plot(fig1.gca(), model, forecast)

# # 그래프2
fig2 = model.plot_components(forecast)

# #가격 조회
nowValue = pyupbit.get_current_price("KRW-BTC")
closeValue = forecast['yhat'].values[-1]

print("현재가 : ", nowValue)
print("24시간뒤의 가격: ", closeValue)

plt.show()