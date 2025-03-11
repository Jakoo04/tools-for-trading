# ____________________ GetTrend ____________________ #

# Returns the trend up to the current indicated rank. Does not necessarily go to the end of the data.
# If you want to go to the end of the data, set the current rank very large (greater than or equal (-1) to the number of candles in the data).

def trend(CurrentRank, ParamFractal, data, PrintResult): # PrintResult == "yes" or "no"

	if PrintResult == "yes" or "Yes" or 1 :
		import matplotlib.pyplot as plt
	
	fract=[[],[],[]]
	if CurrentRank >= len(data) :
		CurrentRank = len(data)-1
	nb = CurrentRank+1

	# --- High and low fractals of parametre ParamFractal are found on all data --- #
	
	for i in range(ParamFractal+1, CurrentRank-ParamFractal):
		cst = 1
		y=1
		while  cst == 1 and y <=ParamFractal :
				if data[i-y][2]>data[i][2] or data[i+y][2]>data[i][2] :
					cst = 0
				y+=1
		if cst == 1 :
			fract[0].append(i)
			fract[1].append(data[i][2])
			fract[2].append(cst)
		else :
			cst = -1
			y=1
			while  cst == -1 and y <=ParamFractal :
				if data[i-y][3]<data[i][3] or data[i+y][3]<data[i][3] :
					cst = 0
				y+=1
			if cst == -1 :
				fract[0].append(i)
				fract[1].append(data[i][3])
				fract[2].append(cst)

	# If we have enough fractals (2) we move on to the next step
	if len(fract[0]) >= 2 :

		# We remove fractals that are too close.
		x = 1
		while x < len(fract[0]) :
			if abs(fract[0][x]-fract[0][x-1]) <= ParamFractal :
				fract[0].pop(x)
				fract[1].pop(x)
				fract[2].pop(x)
				x-=1
			x+=1
		
		x = 1
		while x < len(fract[0]) :

			# We insert low fractals if there are 2 high fractals following each other.
			if fract[2][x] == 1 and fract[2][x-1] == 1 :
			
				cst = 0
				z=ParamFractal-1
				while cst == 0 :
					i=fract[0][x-1]+1
					while cst==0 and i<fract[0][x] :
						cst = -1
						y=1
						while  cst == -1 and y <=z :
							if data[i-y][3]<data[i][3] or data[i+y][3]<data[i][3] :
								cst = 0
							y+=1
						i+=1
					z-=1
				fract[0].insert(x,i-1)
				fract[1].insert(x,data[i-1][3])
				fract[2].insert(x,cst)
					
			# We insert high fractals when 2 low fractals follow each other.
			elif fract[2][x] == -1 and fract[2][x-1] == -1 :
			
				cst = 0
				z=ParamFractal-1
				while cst == 0 :
					i=fract[0][x-1]+1
					while cst==0 and i<fract[0][x] :
						cst = 1
						y=1
						while  cst == 1 and y <=z :
							if data[i-y][2]>data[i][2] or data[i+y][2]>data[i][2] :
								cst = 0
							y+=1
						i+=1
					z-=1
				fract[0].insert(x,i-1)
				fract[1].insert(x,data[i-1][2])
				fract[2].insert(x,cst)

			x+=1

	# If at the end there is a big rise or fall without a fractal, then we add a fractal
	if nb - fract[0][-1] > 2*ParamFractal :

		fract_finale = [None, 0, None]

		if fract[2][-1] == -1 :
			for y in range (fract[0][-1] + ParamFractal, nb) :
				fract_finale_test = data[y][2]
				while fract_finale_test != None and z <= ParamFractal :
					if data[y-z][2] > fract_finale_test :
						fract_finale_test = None
					z+=1
				if fract_finale_test != None :
					z = 1
					while y+z < nb and data[y+z][2] <= fract_finale_test :
						z+=1
					if z-1 >= fract_finale[1] :
						fract_finale = [fract_finale_test, z-1, y]

		elif fract[2][-1] == 1 :
			for y in range (fract[0][-1] + ParamFractal, nb) :
				fract_finale_test = data[y][3]
				while fract_finale_test != None and z <= ParamFractal :
					if data[y-z][3] < fract_finale_test :
						fract_finale_test = None
					z+=1
				if fract_finale_test != None :
					z = 1
					while y+z < nb and data[y+z][3] >= fract_finale_test :
						z+=1
					if z-1 >= fract_finale[1] :
						fract_finale = [fract_finale_test, z-1, y]

		if fract_finale != [None, 0] :
			fract[2].append(fract[2][-1]*(-1))
			fract[0].append(fract_finale[2])
			fract[1].append(fract_finale[0])


	moy0 = [[],[]]
	moy=[]
	moy0[0].append(round((fract[0][0]+fract[0][1])/2))
	moy0[1].append((fract[1][0]+fract[1][1])/2)
	for i in range (moy0[0][0]):
		moy.append(None)
	for i in range (2,len(fract[0])) :
		moy0[0].append(round((fract[0][i]+fract[0][i-1])/2))
		moy0[1].append((fract[1][i]+fract[1][i-1])/2)

		k = moy0[0][-1]-moy0[0][-2]
		for y in range (k) :
			moy.append(moy0[1][-2]+(moy0[1][-1]-moy0[1][-2])/k*y)
			
	if PrintResult == "yes" or "Yes" or 1 :
		
		fig, ax = plt.subplots()
		
		pmax=[]
		pmin=[]                  
		pc=[]     
		for y in range(nb)   :   
			pmax.append(data[y][2])
			pmin.append(data[y][3])
			pc.append(data[y][4])

		ax.plot(pmax, color='green')                                      
		ax.plot(pmin, color='red')                                       
		ax.plot(pc, color="purple")
		
		ax.scatter(fract[0], fract[1])
		ax.scatter(moy0[0], moy0[1], marker="x", color="black")
		ax.plot(moy, color = "black")
		

	return fract, moy0, moy