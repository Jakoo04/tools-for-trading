# ____________________ BacktestExemple ____________________ #

import matplotlib.pyplot as plt
from GetSupportsAndResistances import supres
import GetPriceHistory
import ccxt
import time


# --- PARAMETRES --- #

param_fract = 14
coefa = 1/9
coefb = 1/21
eqmax = 2
lmin = 24

# --- GetPriceHistory (data) --- #

start = '2023-01-01T00:00:00Z'
symbol = 'DOGE/USDT'
timeframe = '1d'
data0 = GetPriceHistory.GetData(start, symbol, timeframe)

# --- SIMULATION --- #

print("SIMULATION START")

data = []
resultats = []
position = None
nb = len(data0)

niveaux = []
nivbas = []
fracth = []
fractb = []

for i in range(100):
    data.append(data0[i])

for aaa in range (100, nb) :

    data.append(data0[aaa])


    # Gestion des positions ouvertes :
    # une position = [rang ouvert, a quel prix, montant(+/-), tp, sl]
    # resultats = [rang ouvert, a quel prix, position achat/vente (1/-1), tp, sl, rang fermé, type de cloture(tp/sl), resultat en %]
    if position != None :
        if position[2] == 1 :
            if data[aaa][2] >= position[3] :
                res = (position[3]-position[1])*100
                resultats.append(position+[aaa, "tp", res])
                position = None
            elif data[aaa][3] <= position[4] :
                res = (position[4]-position[1])*100
                resultats.append(position+[aaa, "sl", res])
                position = None
        elif position[2] == -1 :
            if data[aaa][3] <= position[3] :
                res = -(position[3]-position[1])*100
                resultats.append(position+[aaa, "tp", res])
                position = None
            elif data[aaa][2] >= position[4] :
                res = -(position[4]-position[1])*100
                resultats.append(position+[aaa, "sl", res])
                position = None

    # (aaa, param_fract, coefa, coefb, eqmax, lmin, data, PrintResult)
    sortie = supres(aaa, param_fract, coefa, coefb, eqmax, lmin, data, "Do not print")

    if sortie != None :
        
        niveaux = sortie[0]
        nivbas = sortie[1]
        fracth = sortie[2]
        fractb = sortie[3]
        hauteurmoy = sortie[4]

    # [rang ouvert, a quel prix, montant(+/-), tp, sl]
    if position == None and len(fracth)>0 and len(fractb)>0 :
        if len(niveaux)>0 : #and (fracth[-1][0] == niveaux[-1][2]): # or fracth[-2][0] == niveaux[-1][2]) :
            if data[aaa][3] <= niveaux[-1][0] <= data[aaa][2] :
                ok = 1
                for z in range (niveaux[-1][2], aaa-1) :
                    if data[z][2] > niveaux[-1][0] + hauteurmoy[niveaux[-1][2]-1]*coefa :
                        ok = 0
                        break
                if ok == 1 :
                    position = [aaa, niveaux[-1][0], -1, niveaux[-1][0]-hauteurmoy[-1]*0.9, niveaux[-1][0]+hauteurmoy[-1]*2*coefb]

        if position == None and len(nivbas)>0 : #and (fractb[-1][0] == nivbas[-1][2]): # or fractb[-2][0] == nivbas[-1][2]) :
            if data[aaa][3] <= nivbas[-1][0] <= data[aaa][2] :
                ok = 1
                for z in range (nivbas[-1][2], aaa-1) :
                    if data[z][3] < nivbas[-1][0] - hauteurmoy[nivbas[-1][2]-1]*coefa :
                        ok = 0
                        break
                if ok == 1 :
                    position = [aaa, nivbas[-1][0], 1, nivbas[-1][0]+hauteurmoy[-1]*0.9, nivbas[-1][0]-hauteurmoy[-1]*2*coefb]

print("END OF SIMULTATION, WHAIT GRAPHIC")

fig, ax = plt.subplots()

pmax=[]
pmin=[]                  
pc=[]     
for y in range(nb)   :   
    pmax.append(data[y][2])
    pmin.append(data[y][3])
    pc.append(data[y][4])


xgraph = []
ygraph = []
for y in range (len(fracth)) :
    xgraph.append(fracth[y][0])
    ygraph.append(fracth[y][1])
for y in range (len(fractb)) :
    xgraph.append(fractb[y][0])
    ygraph.append(fractb[y][1])


ax.plot(pmax, color='green')                                      
ax.plot(pmin, color='red')                                       
ax.plot(pc, color="purple")
ax.scatter(xgraph, ygraph)

xniveaux=[]
yniveaux=[]
for i in range (len(niveaux)) :
    for j in range (niveaux[i][1], niveaux[i][2]+1) :
        xniveaux.append(j)
        yniveaux.append(niveaux[i][0])
for i in range (len(nivbas)) :
    for j in range (nivbas[i][1], nivbas[i][2]+1) :
        xniveaux.append(j)
        yniveaux.append(nivbas[i][0])

ax.scatter(xniveaux, yniveaux, color='black', marker = '_')

# resultats = [rang ouvert, a quel prix, position achat/vente (1/-1), tp, sl, rang fermé, type de cloture(tp/sl), resultat en %]
ouvertures = [[],[]]
fermetures = [[],[],[],[]]
for i in range (len(resultats)) :
    ouvertures[0].append(resultats[i][0])
    ouvertures[1].append(resultats[i][1])
    if resultats[i][7] > 0 :
        fermetures[0].append(resultats[i][5])
        fermetures[1].append(resultats[i][3])
    else :
        fermetures[2].append(resultats[i][5])
        fermetures[3].append(resultats[i][4])

ax.scatter(ouvertures[0], ouvertures[1], marker="x", color = "blue")
ax.scatter(fermetures[0], fermetures[1], marker="x", color = "green")
ax.scatter(fermetures[2], fermetures[3], marker="x", color = "red")


figres, axres = plt.subplots()

print(resultats)

graphresultats = [0]
for i in range (len(resultats)) :
    graphresultats.append(graphresultats[-1]+resultats[i][7])

axres.plot(graphresultats)


plt.show()