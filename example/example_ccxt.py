import pandas as pd
import ccxt
from ta.volatility import BollingerBands, AverageTrueRange

exchange_ftx = ccxt.ftx({
    'apiKey': 'pEkTLyrK1c_vWLnGSfyq8oS_x21qWEzkhlq9yyLe',
    'secret': 'LcIYZOuJ1nlicj-k4zjc7l0Y5WRD6kjwC824zp6E',
})
exchange_upbit = ccxt.upbit({
    'apiKey': 'NjUGijNrj9TH84c3aDD5LFt8OWieIiNxoPyB2T0I',
    'secret': 'hCryxjfrEFAWPo2ArB0tu2d3c1ppJaNQLnuZDit0',
})

market = exchange_upbit.load_markets()

bars = exchange_upbit.fetch_ohlcv('BORA/KRW', timeframe='1m', limit=20)
for i in bars:
    print(i)

df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

bb_indicator = BollingerBands(df['close'])
df['upper_band'] = bb_indicator.bollinger_hband()
df['lower_band'] = bb_indicator.bollinger_lband()
df['moving_average'] = bb_indicator.bollinger_mavg()

print(df)
print(df['timestamp'][len(df)-1])

balance = exchange_upbit.fetch_balance()
print(balance)

def test():
    exchange_ftx = ccxt.ftx({
        'apiKey': 'pEkTLyrK1c_vWLnGSfyq8oS_x21qWEzkhlq9yyLe',
        'secret': 'LcIYZOuJ1nlicj-k4zjc7l0Y5WRD6kjwC824zp6E',
    })
    exchange_upbit = ccxt.upbit({
        'apiKey': 'NjUGijNrj9TH84c3aDD5LFt8OWieIiNxoPyB2T0I',
        'secret': 'hCryxjfrEFAWPo2ArB0tu2d3c1ppJaNQLnuZDit0',
    })

    market = exchange_upbit.load_markets()

    bars = exchange_upbit.fetch_ohlcv('BORA/KRW', timeframe='1m', limit=20)
    for i in bars:
        print(i)

    df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    bb_indicator = BollingerBands(df['close'])
    df['upper_band'] = bb_indicator.bollinger_hband()
    df['lower_band'] = bb_indicator.bollinger_lband()
    df['moving_average'] = bb_indicator.bollinger_mavg()

    print(df)
    print(df['timestamp'][len(df) - 1])

    balance = exchange_upbit.fetch_balance()
    print(balance)
    return df

a = test()
print('진짜결과')
print(a['timestamp'])
