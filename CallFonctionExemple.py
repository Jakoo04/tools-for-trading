import matplotlib.pyplot as plt

import GetPriceHistory
import GetTrend
import GetChannelsDraft
import GetSupportsAndResistances

start = '2023-06-01T00:00:00Z'
symbol = 'BTC/USDT'
timeframe = '1d'
data = GetPriceHistory.GetData(start, symbol, timeframe)

CurrentRank = len(data)-1
ParamFractal = 10
PrintResult = "yes"
GetTrend.trend(CurrentRank, ParamFractal, data, PrintResult)

ParamFractal = 10
coefa = 2
coefb = 2
coefc = 2
coefd = 2
coefsuperposition = 0.99
PrintResult = "yes"
GetChannelsDraft.channels(ParamFractal, coefa, coefb, coefc, coefd, coefsuperposition, data, PrintResult)

paramFractal = 14
coefa = 1/9
coefb = 1/21
eqmax = 2
lmin = 24
PrintResult = "yes"
GetSupportsAndResistances.supres(CurrentRank, ParamFractal, coefa, coefb, eqmax, lmin, data, PrintResult)

plt.show()