# ____________________ GetChannels ____________________ #

# Return the channels on all data given. 
# You have to mmodifie this fonction to select the CurrentRank like in GetTrend.


def channels(ParamFractal, coefa, coefb, coefc, coefd, coefsuperposition, data, PrintResult): # PrintResult == "yes" or "no"

    # -- Working exemple for parametres --- #

    # ParamFractal = 10
    # coefa = 1
    # coefb = 1
    # coefc = 0.001
    # coefd = 2
    # coefsuperposition = 0.99


    if PrintResult == "yes" or "Yes" or 1 :
        import matplotlib.pyplot as plt
        
    nb = len(data)


    # --- Find all fractals --- #

    fracth = []
    fractb = []
    for i in range (ParamFractal+1, nb-ParamFractal-1) :
        tfracth = data[i][2]
        y = 1
        while tfracth != None and y <= ParamFractal :
            if data[i+y][2] > tfracth or data[i-y][2] > tfracth :
                tfracth = None
            y+=1
        if tfracth != None :
            fracth.append([i,tfracth])
        else :
            tfractb = data[i][3]
            y = 1
            while tfractb != None and y <= ParamFractal :
                if data[i+y][3] < tfractb or data[i-y][3] < tfractb :
                    tfractb = None
                y+=1
            if tfractb != None :
                fractb.append([i,tfractb])

    # Supprimer les doublons
    i=0
    while i < len(fracth)-1 :
        if fracth[i][1] == fracth[i+1][1] and fracth[i+1][0] - fracth[i][0] -1 < ParamFractal :
            fracth.pop(i+1)
        i+=1
    i=0
    while i < len(fractb)-1 :
        if fractb[i][1] == fractb[i+1][1] and fractb[i+1][0] - fractb[i][0] -1 < ParamFractal :
            fractb.pop(i+1)
        i+=1


    # Calcul espace moyen entre fracth et fractb
    hauteurmoy0=[]
    counth = len(fracth)-1
    countb = len(fractb)-1
    while counth >=0 and countb >= 0:
        somme = 0
        countx = 0
        start=(fracth[counth][0]+fractb[countb][0])//2
        while counth >= 0 and countb >= 0 and countx < 10 :
            somme += abs(fracth[counth][1]-fractb[countb][1])
            countx += 1
            if fracth[counth][0] > fractb[countb][0] :
                counth -= 1
            else :
                countb -= 1
        hauteurmoy0.append([start, somme / countx])

    hauteurmoy = []
    for j in range (hauteurmoy0[-1][0]) :
        hauteurmoy.append(hauteurmoy0[-1][1])
    for i in range (len(hauteurmoy0)) :
        for j in range(hauteurmoy0[len(hauteurmoy0)-1-i][0], hauteurmoy0[len(hauteurmoy0)-1-i-1][0]) :
            hauteurmoy.append(hauteurmoy0[len(hauteurmoy0)-1-i-1][1])



    # --- canneaux (haut) --- #
    prt = 0
    canneaux = []
    for i in range (2, len(fracth)) :
        if i <= 20 :
            val = 0
        else :
            val = i-20
        for j in range (val, i) :
            ok = 1
            pente = (fracth[j][1]-fracth[i][1])/(fracth[j][0]-fracth[i][0])
            val_init = fracth[i][1] - pente*fracth[i][0]
            for k in range (j+1, i) :
                if fracth[k][1] > val_init + pente*fracth[k][0] + coefa*hauteurmoy[fracth[k][0]] :
                    ok = 0
            if ok == 1 :
                canneaux.append([val_init, pente, fracth[j][0], fracth[i][0]])

    canneaux_identiques = []
    for i in range (len(canneaux)) :
        canneaux_identiques.append([])
        if i <= 20 :
            val = 0
        else :
            val = i-20
        for j in range (val, i) :
            a = (canneaux[i][3]+canneaux[j][2])//2
            if abs((canneaux[j][0]+canneaux[j][1]*a)-(canneaux[i][0]+canneaux[i][1]*a)) < hauteurmoy[a]*coefb and abs(canneaux[j][1]-canneaux[i][1]) < hauteurmoy[a]*coefc :
                if len(canneaux_identiques[i]) <= 2 :
                    canneaux_identiques[i].append(canneaux[j][2])
                    canneaux_identiques[i].append(canneaux[i][3])
                elif canneaux[j][2] < canneaux_identiques[i][0] :
                    #print("ca ne devrait pas arriver, l.119")
                    canneaux_identiques[i][0] = canneaux[j][2]
                canneaux_identiques[i].append(canneaux[j])


    canneaux2=[]
    for i in range(len(canneaux_identiques)) :
        if len(canneaux_identiques[i]) > 4 :
            moy1 = 0
            moy2 = 0
            for j in range (2, len(canneaux_identiques[i])) :
                moy1 += canneaux_identiques[i][j][0]
                moy2 += canneaux_identiques[i][j][1]
            moy1 /= len(canneaux_identiques[i])-2
            moy2 /= len(canneaux_identiques[i])-2
            ect1 = 0
            ect2 = 0
            for k in range (2, len(canneaux_identiques[i])) :
                ect1+=(canneaux_identiques[i][k][0]-moy1)**2
                ect2+=(canneaux_identiques[i][k][1]-moy2)**2
            ect1 /= len(canneaux_identiques[i])-2
            ect2 /= len(canneaux_identiques[i])-2
            ect1 = ect1**0.5
            ect2 = ect2**0.5
            canneaux2.append([canneaux_identiques[i][0], canneaux_identiques[i][1], moy1, moy2, ect1, ect2])

    rangasup=[]
    i=0
    while i < (len(canneaux2)) :
        j=0
        while j < (len(canneaux2)) :
            if i != j :

                if canneaux2[i][0] <= canneaux2[j][0] <= canneaux2[i][1] and canneaux2[i][0] <= canneaux2[j][1] <= canneaux2[i][1] :
                    U = [canneaux2[j][0], canneaux2[j][1]]
                elif canneaux2[i][0] <= canneaux2[j][0] <= canneaux2[i][1] and canneaux2[j][1] > canneaux2[i][1] :
                    U = [canneaux2[j][0], canneaux2[i][1]]
                elif canneaux2[i][0] > canneaux2[j][0] and canneaux2[i][0] <= canneaux2[j][1] <= canneaux2[i][1] :
                    U = [canneaux2[i][0], canneaux2[j][1]]
                elif canneaux2[j][0] <= canneaux2[i][0] <= canneaux2[j][1] and canneaux2[j][0] <= canneaux2[i][1] <= canneaux2[j][1] :
                    U = [canneaux2[i][0], canneaux2[i][1]]
                elif canneaux2[j][0] <= canneaux2[i][0] <= canneaux2[j][1] and canneaux2[i][1] > canneaux2[j][1] :
                    U = [canneaux2[i][0], canneaux2[j][1]]
                elif canneaux2[j][0] > canneaux2[i][0] and canneaux2[j][0] <= canneaux2[i][1] <= canneaux2[j][1] :
                    U = [canneaux2[j][0], canneaux2[i][1]]
                else :
                    U = None
                
                if U != None :
                    if U[1]-U[0] > coefsuperposition*(canneaux2[i][1]-canneaux2[i][0]) or U[1]-U[0] > coefsuperposition*(canneaux2[j][1]-canneaux2[j][0]) :
                        # Lequel est le meilleur à garder ? #uniquement ect2, ect1 demande encore des manipes pour etre un indic sur.
                        rangpresenti = None
                        rangpresentj = None
                        for k in range(len(rangasup)) :
                            if i in rangasup[k] :
                                rangpresenti = k
                                break
                        for k in range(len(rangasup)) :
                            if j in rangasup[k] :
                                rangpresentj = k
                                break
                        if rangpresenti != None and rangpresentj == None:
                            rangasup[rangpresenti].append(j)
                        elif rangpresentj != None and rangpresenti == None:
                            rangasup[rangpresentj].append(i)
                        elif rangpresentj == None and rangpresenti == None:
                            rangasup.append([i,j])
            j+=1
        i+=1


    asupdef = []
    for i in range (len(rangasup)) :
        rangmeilleur = 0
        moyx=[]
        for j in range (len(rangasup[i])) :
            somme = 0
            for k in range (canneaux2[rangasup[i][j]][0], canneaux2[rangasup[i][j]][1]) :
                somme += abs(canneaux2[rangasup[i][j]][2] + canneaux2[rangasup[i][j]][3]*k - data[k][2])
            moyx.append(somme/(canneaux2[rangasup[i][j]][1]-canneaux2[rangasup[i][j]][0]))
        mini = min(moyx)
        for j in range (len(rangasup[i])) :
            if moyx[j] != mini :
                asupdef.append(rangasup[i][j])
            elif mini > coefd*hauteurmoy[rangasup[i][j]] :
                asupdef.append(rangasup[i][j])

    asupdef.sort()
    for i in range (len(asupdef)) :
        canneaux2.pop(asupdef[len(asupdef)-1-i])

    xcanneaux = []
    ycanneaux = []
    for i in range (len(canneaux2)) :
        for y in range (canneaux2[i][0], canneaux2[i][1]+1) :
            xcanneaux.append(y)
            ycanneaux.append(canneaux2[i][2] + canneaux2[i][3]*y)




    # --- cannaux (bas) --- #

    prt = 0
    canneauxb = []
    for i in range (2, len(fractb)) :
        if i <= 20 :
            val = 0
        else :
            val = i-20
        for j in range (val, i) :
            ok = 1
            pente = (fractb[j][1]-fractb[i][1])/(fractb[j][0]-fractb[i][0])
            val_init = fractb[i][1] - pente*fractb[i][0]
            for k in range (j+1, i) :
                if fractb[k][1] < val_init + pente*fractb[k][0] - coefa*hauteurmoy[fractb[k][0]] :
                    ok = 0
            if ok == 1 :
                canneauxb.append([val_init, pente, fractb[j][0], fractb[i][0]])

    canneaux_identiquesb = []
    for i in range (len(canneauxb)) :
        canneaux_identiquesb.append([])
        if i <= 20 :
            val = 0
        else :
            val = i-20
        for j in range (val, i) :
            a = (canneauxb[i][3]+canneauxb[j][2])//2
            if abs((canneauxb[j][0]+canneauxb[j][1]*a)-(canneauxb[i][0]+canneauxb[i][1]*a)) < hauteurmoy[a]*coefb and abs(canneauxb[j][1]-canneauxb[i][1]) < hauteurmoy[a]*coefc :
                if len(canneaux_identiquesb[i]) <= 2 :
                    canneaux_identiquesb[i].append(canneauxb[j][2])
                    canneaux_identiquesb[i].append(canneauxb[i][3])
                elif canneauxb[j][2] < canneaux_identiquesb[i][0] :
                    #print("ca ne devrait pas arriver, l.119")
                    canneaux_identiquesb[i][0] = canneauxb[j][2]
                canneaux_identiquesb[i].append(canneauxb[j])


    canneaux2b=[]
    for i in range(len(canneaux_identiquesb)) :
        if len(canneaux_identiquesb[i]) > 4 :
            moy1 = 0
            moy2 = 0
            for j in range (2, len(canneaux_identiquesb[i])) :
                moy1 += canneaux_identiquesb[i][j][0]
                moy2 += canneaux_identiquesb[i][j][1]
            moy1 /= len(canneaux_identiquesb[i])-2
            moy2 /= len(canneaux_identiquesb[i])-2
            ect1 = 0
            ect2 = 0
            for k in range (2, len(canneaux_identiquesb[i])) :
                ect1+=(canneaux_identiquesb[i][k][0]-moy1)**2
                ect2+=(canneaux_identiquesb[i][k][1]-moy2)**2
            ect1 /= len(canneaux_identiquesb[i])-2
            ect2 /= len(canneaux_identiquesb[i])-2
            ect1 = ect1**0.5
            ect2 = ect2**0.5
            canneaux2b.append([canneaux_identiquesb[i][0], canneaux_identiquesb[i][1], moy1, moy2, ect1, ect2])

    rangasupb=[]
    i=0
    while i < (len(canneaux2b)) :
        j=0
        while j < (len(canneaux2b)) :
            if i != j :

                if canneaux2b[i][0] <= canneaux2b[j][0] <= canneaux2b[i][1] and canneaux2b[i][0] <= canneaux2b[j][1] <= canneaux2b[i][1] :
                    U = [canneaux2b[j][0], canneaux2b[j][1]]
                elif canneaux2b[i][0] <= canneaux2b[j][0] <= canneaux2b[i][1] and canneaux2b[j][1] > canneaux2b[i][1] :
                    U = [canneaux2b[j][0], canneaux2b[i][1]]
                elif canneaux2b[i][0] > canneaux2b[j][0] and canneaux2b[i][0] <= canneaux2b[j][1] <= canneaux2b[i][1] :
                    U = [canneaux2b[i][0], canneaux2b[j][1]]
                elif canneaux2b[j][0] <= canneaux2b[i][0] <= canneaux2b[j][1] and canneaux2b[j][0] <= canneaux2b[i][1] <= canneaux2b[j][1] :
                    U = [canneaux2b[i][0], canneaux2b[i][1]]
                elif canneaux2b[j][0] <= canneaux2b[i][0] <= canneaux2b[j][1] and canneaux2b[i][1] > canneaux2b[j][1] :
                    U = [canneaux2b[i][0], canneaux2b[j][1]]
                elif canneaux2b[j][0] > canneaux2b[i][0] and canneaux2b[j][0] <= canneaux2b[i][1] <= canneaux2b[j][1] :
                    U = [canneaux2b[j][0], canneaux2b[i][1]]
                else :
                    U = None
                
                if U != None :
                    if U[1]-U[0] > coefsuperposition*(canneaux2b[i][1]-canneaux2b[i][0]) or U[1]-U[0] > coefsuperposition*(canneaux2b[j][1]-canneaux2b[j][0]) :
                        # Lequel est le meilleur à garder ? #uniquement ect2, ect1 demande encore des manipes pour etre un indic sur.
                        rangpresenti = None
                        rangpresentj = None
                        for k in range(len(rangasupb)) :
                            if i in rangasupb[k] :
                                rangpresenti = k
                                break
                        for k in range(len(rangasupb)) :
                            if j in rangasupb[k] :
                                rangpresentj = k
                                break
                        if rangpresenti != None and rangpresentj == None:
                            rangasupb[rangpresenti].append(j)
                        elif rangpresentj != None and rangpresenti == None:
                            rangasupb[rangpresentj].append(i)
                        elif rangpresentj == None and rangpresenti == None:
                            rangasupb.append([i,j])
            j+=1
        i+=1


    asupdefb = []
    for i in range (len(rangasupb)) :
        rangmeilleur = 0
        moyx=[]
        for j in range (len(rangasupb[i])) :
            somme = 0
            for k in range (canneaux2b[rangasupb[i][j]][0], canneaux2b[rangasupb[i][j]][1]) :
                somme += abs(canneaux2b[rangasupb[i][j]][2] + canneaux2b[rangasupb[i][j]][3]*k - data[k][2])
            moyx.append(somme/(canneaux2b[rangasupb[i][j]][1]-canneaux2b[rangasupb[i][j]][0]))
        mini = min(moyx)
        for j in range (len(rangasupb[i])) :
            if moyx[j] != mini :
                asupdefb.append(rangasupb[i][j])
            elif mini > coefd*hauteurmoy[rangasupb[i][j]] :
                asupdefb.append(rangasupb[i][j])

    asupdefb.sort()
    for i in range (len(asupdefb)) :
        canneaux2b.pop(asupdefb[len(asupdefb)-1-i])

    xcanneauxb = []
    ycanneauxb = []
    for i in range (len(canneaux2b)) :
        for y in range (canneaux2b[i][0], canneaux2b[i][1]+1) :
            xcanneauxb.append(y)
            ycanneauxb.append(canneaux2b[i][2] + canneaux2b[i][3]*y)





    # --- PrintResults --- #

    if PrintResult == "Yes" or "yes" or 1 :

        fig3, ax3 = plt.subplots()


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


        ax3.plot(pmax, color='green')                                      
        ax3.plot(pmin, color='red')                                       
        ax3.plot(pc, color="purple")
        ax3.scatter(xgraph, ygraph)

        ax3.scatter(xcanneaux, ycanneaux, color='black', marker = '_')
        ax3.scatter(xcanneauxb, ycanneauxb, color='black', marker = '_')


    return [xcanneaux, ycanneaux] , [xcanneauxb, ycanneauxb]

    # Table Format (x2 : for low (canneauxb) and also for high (canneaux)): 
    # [ [range0.0, range0.1, range0.2, range1.0, range1.1, range1.2 ...] , [price0.0, price0.1, price0.2, price1.0, price1.1, price1.2, ...] ]
    # Exemple : [[8,9,10, 43,44,45, ...],[1.012, 1.013, 1.014,  1.341, 1.343, 1.345,  ...]]