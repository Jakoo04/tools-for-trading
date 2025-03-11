# ____________________ GetSupportsAndResistances ____________________ #

# Returns the supports and the resistances up to the current indicated rank. Does not necessarily go to the end of the data.
# If you want to go to the end of the data, set the current rank very large (greater than or equal (-1) to the number of candles in the data).


import statistics

def supres(CurrentRank, ParamFractal, coefa, coefb, eqmax, lmin, data, PrintResult) :

    # --- Working exemple for parametres --- #

    # ParamFractal = 14
    # coefa = 1/9
    # coefb = 1/21
    # eqmax = 2
    # lmin = 24

    if PrintResult == "yes" or PrintResult == "Yes" or PrintResult == 1 :
        import matplotlib.pyplot as plt
    import statistics

    if CurrentRank >= len(data) :
        CurrentRank = len(data)-1

    # --- Supports et résistances --- #

    i = CurrentRank-ParamFractal

    # On recherche toutes les fractales

    fracth = []
    fractb = []
    for i in range (ParamFractal+1, CurrentRank-ParamFractal-1) :
        tfracth = data[i][2]
        y = 1
        while tfracth != None and y <= ParamFractal :
            if i+y > CurrentRank :
                tfracth = None
                break
            if data[i+y][2] > tfracth or data[i-y][2] > tfracth :
                tfracth = None
            y+=1
        if tfracth != None :
            fracth.append([i,tfracth])
        else :
            tfractb = data[i][3]
            y = 1
            while tfractb != None and y <= ParamFractal :
                if i+y > CurrentRank :
                    tfractb = None
                    break
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


    #hauteurmoy0
    # Calcul espace moyen entre fracth et fractb moyenne
    hauteurmoy0=[]
    counth = len(fracth)-1
    countb = len(fractb)-1
    while counth >=0 and countb >= 0:
        somme = 0
        countx = 0
        if fracth[counth][0] > fractb[countb][0] :
            start=fracth[counth][0]
        else :
            start=fractb[countb][0]
        while counth >= 0 and countb >= 0 and countx < 4 :
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

    # --- niveaux --- #

    niveaux = []
    for i in range (len(fracth)) :
        potentielsniveaux = [fracth[i]+[i]]
        j = 1
        count_fract_horsjeu = 0
        while count_fract_horsjeu <= eqmax and i-j >= 0 :
            milieu = statistics.median([x[1] for x in potentielsniveaux])
            if abs(fracth[i-j][1]-milieu) < coefa*hauteurmoy[fracth[i-j][0]] :
                potentielsniveaux.append(fracth[i-j]+[i-j])
                count_fract_horsjeu = 0
            else :
                count_fract_horsjeu += 1
            j+=1

        if len(potentielsniveaux) >= 2 :
            ok = 1
            # + stricte avec les résistances à seuelement 2 fracts (si pas de fract intercalaire, alors marge plus petite (coefb))
            if len(potentielsniveaux) == 2 :
                if potentielsniveaux[0][0] - potentielsniveaux[1][0] < lmin :
                    ok = 0
                else :
                    j = 0
                    valstart = None
                    valend = None
                    while valend == None or valstart == None :
                        if potentielsniveaux[0][0] == fracth[j][0] :
                            valstart = j
                        elif potentielsniveaux[1][0] == fracth[j][0] :
                            valend = j
                        j+=1

                    if abs(valend - valstart) == 1 :
                        if abs(potentielsniveaux[1][1]-potentielsniveaux[0][1]) > coefb*hauteurmoy[potentielsniveaux[1][0]] :
                            ok = 0
            
            # AUCUN fractals qui sort du mauvais côté du support/résistance
            if ok == 1 :

                limite = -1
                for j in range (potentielsniveaux[-1][2]+1, potentielsniveaux[0][2]) :
                    ok2 = 0
                    for k in range (len(potentielsniveaux)) :
                        if fracth[j][1]-potentielsniveaux[k][1] < coefa*hauteurmoy[fracth[j][0]] :
                            ok2 = 1
                            break
                    if ok2 == 0 :
                        limite = j

                while len(potentielsniveaux) >= 2 and potentielsniveaux[-1][2] <= limite :
                    potentielsniveaux.pop(-1)

                if len(potentielsniveaux) >= 2 :
                    ok = 1
                else : 
                    ok = 0

            if ok == 1 :

                somme=0
                for k in range (len(potentielsniveaux)) :
                    somme+=potentielsniveaux[k][1]
                niveaux.append([somme/len(potentielsniveaux), fracth[potentielsniveaux[-1][2]][0], fracth[potentielsniveaux[0][2]][0]])

        while len(niveaux) >= 2 and niveaux[-2][2] > niveaux[-1][1] :
            niveaux.pop(-2)



    # --- nivbas --- #

    nivbas = []
    for i in range (len(fractb)) :
        potentielsnivbas = [fractb[i]+[i]]
        j = 1
        count_fract_horsjeu = 0
        while count_fract_horsjeu <= eqmax and i-j >= 0 :
            milieu = statistics.median([x[1] for x in potentielsnivbas])
            if abs(fractb[i-j][1]-milieu) < coefa*hauteurmoy[fractb[i-j][0]] :
                potentielsnivbas.append(fractb[i-j]+[i-j])
                count_fract_horsjeu = 0
            else :
                count_fract_horsjeu += 1
            j+=1

        if len(potentielsnivbas) >= 2 :
            ok = 1
            # + stricte avec les résistances à seuelement 2 fracts (si pas de fract intercalaire, alors marge plus petite (coefb))
            if len(potentielsnivbas) == 2 :
                if potentielsnivbas[0][0] - potentielsnivbas[1][0] < lmin :
                    ok = 0
                else :
                    j = 0
                    valstart = None
                    valend = None
                    while valend == None or valstart == None :
                        if potentielsnivbas[0][0] == fractb[j][0] :
                            valstart = j
                        elif potentielsnivbas[1][0] == fractb[j][0] :
                            valend = j
                        j+=1

                    if abs(valend - valstart) == 1 :
                        if abs(potentielsnivbas[1][1]-potentielsnivbas[0][1]) > coefb*hauteurmoy[potentielsnivbas[1][0]] :
                            ok = 0
            
            # AUCUN fractals qui sort du mauvais côté du support/résistance
            if ok == 1 :

                limite = -1
                for j in range (potentielsnivbas[-1][2]+1, potentielsnivbas[0][2]) :
                    ok2 = 0
                    for k in range (len(potentielsnivbas)) :
                        if potentielsnivbas[k][1]-fractb[j][1] < coefa*hauteurmoy[fractb[j][0]] :
                            ok2 = 1
                            break
                    if ok2 == 0 :
                        limite = j

                while len(potentielsnivbas) >= 2 and potentielsnivbas[-1][2] <= limite :
                    potentielsnivbas.pop(-1)

                if len(potentielsnivbas) >= 2 :
                    ok = 1
                else : 
                    ok = 0

            if ok == 1 :

                somme=0
                for k in range (len(potentielsnivbas)) :
                    somme+=potentielsnivbas[k][1]
                nivbas.append([somme/len(potentielsnivbas), fractb[potentielsnivbas[-1][2]][0], fractb[potentielsnivbas[0][2]][0]])

        while len(nivbas) >= 2 and nivbas[-2][2] > nivbas[-1][1] :
            nivbas.pop(-2)

    if PrintResult == "yes" or PrintResult == "Yes" or PrintResult == 1 :

        fig, ax = plt.subplots()

        pmax=[]
        pmin=[]                  
        pc=[]     
        for y in range(len(data))   :   
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


    return niveaux, nivbas, fracth, fractb, hauteurmoy