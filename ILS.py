class ILS:

	def shake(self,Locations, R,S):
		print "in 1"
		for l in range(S,R+1):
			i = 0 if l >= len(Locations) else l
			print "removing location: ",Locations[i].id_location
			Locations.remove(Locations[i])


		return Locations
