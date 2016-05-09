class ILS:

	def shake(self,Locations, R,S):
		
		for l in range(S,S+R+1):
			i = 0 if l >= len(Locations) else l
			print "removing location: ",Locations[i].id_location
			Locations.remove(Locations[i])

		return Locations

	def execute():

		S = 1
		R = 1

		NoImprovementCounter = 0

		BestFound = {"ratio": 0, "tour":0}

		SmallestTourSize = 0

		while NoImprovementCounter < 150:
			
			NewTour = 0; #Get tour
			if BestFound['tour'] < NewTour:
				
				#Assign new tour as local optimum
				BestFound['tour'] = NewTour

				R = 1
				NoImprovementCounter = 0

			else:
				NoImprovementCounter += 1

			tour = self.shake(BestFound['tour'], R, S)

			S = S + R
			R = R + 1

			if S >= SmallestTourSize:
				S = S - SmallestTourSize

			if R == (1.0*n/(3*n)):
				R = 1

		return BestFound

	



