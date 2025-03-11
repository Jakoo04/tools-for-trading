# ____________________ GetPriceHistory ____________________ #

import ccxt
import time

# --- Get Pairs Availeble --- #

def GetPairsAvailable() :
    markets = ccxt.binance.load_markets()
    print(markets.keys())

# --- Get data with ccxt and Binance API --- #

def GetData(start, symbol, timeframe) :

    # start Exemple : '2023-01-01T00:00:00Z'
    # symbol Exemple : 'DOGE/USDT'
    # timeframe Exemple : '1d'

    binance = ccxt.binance({
        'rateLimit': 1000,      # Limite de requêtes par minute
        'enableRateLimit': True  # Activation de la gestion automatique de la limite de taux
    })

    exchange = ccxt.binance()
    limit = 1000 # (Maximum for Binance API)

    data= []

    # Start Timestamp
    since = exchange.parse8601(start)

    while True:

        candles = exchange.fetch_ohlcv(symbol, timeframe, since=since, limit=limit)

        if len(candles) == 0:
            break

        data += candles
        since = candles[-1][0] + 1  # Repartir juste après la dernière bougie

        # Respecter les limites de l'API
        time.sleep(exchange.rateLimit / 1000)

    return data

    # data Format : [[candle time, open price, max price, min price, close price, volume], [candle time, open price, max price, min price, close price, volume], ...]
    # data Exemple : [[1672790400000, 0.07049, 0.07362, 0.07019, 0.07311, 790550617.0], [1672876800000, 0.0731, 0.07529, 0.07035, 0.07152, 1201528327.0], ...]