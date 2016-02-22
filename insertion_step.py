import random

class insertion_step:

	def wait(self, opening,arrival):
		#Wait: in case of arriving before the location opens, 
		#if we arrive later then we wait 0 minutes
		return max(0, opening-arrival)

	def estimateArrival(self,l_i, l_k, times,start):
		#estimate time from location_i to location_k + start time
		return times[l_i][l_k]+start
	
	#this for maxShift
	def getLeaveTime(self, Locations, i,end):
		return Locations[i].closing if Locations[i].closing <= end else end

	#this for location
	def getLeave(self, Locations, i):
		return Locations[i].arrival+Locations[i].max_shift

	def maxShift(self, Locations, i, opening, closing, arrival, times,start,end):
		
		#if i+1 == (len(Locations)-1):
		
		#If we reach the last location, means it's the end of the tour
		leave = self.getLeaveTime(Locations,i,end)
		print "leave from ",i,": ",leave
		arr2 = times[i][i+1]
		print "arrival: ",arrival
		print "next arrival: ",arr2
		max_shift = leave-arrival-arr2
		print "max_shift: ",max_shift
		return max_shift

		#We chose the maximum time allowed to stay in one place in order to not make 
		#infeasible the staying time for the rest of locations.
		"""
		return 	min( closing-arrival , 
						self.wait(opening, arrival) + 
							self.maxShift(
								Locations, i+1, Locations[i+1].opening, 
								Locations[i+1].closing, self.estimateArrival(i, i+1,times,start), 
								times,start,end))
		"""


	def ratio(self,Locations,i):
		#Gain of choosing it taking score vs cost of time
		return Locations[i].score*1.0/Locations[i].shift	

	def Shift( self, Locations, j , i, times, start):
		#Get the total cost of time of including a location between location_i and location_k
		k = j+1
		cij = times[i][j]#self.estimateArrival( i, j, times, start )
		print "cij: ", cij
		wait = Locations[j].wait
		print "wait: ",wait
		
		cjk = times[j][k]#self.estimateArrival( j, k , times, start)
		print "cjk: ",cjk
		cik = times[i][k]#self.estimateArrival( i, k, times, start)
		print "cik: ",cik
		Tj = max(0,Locations[j].max_shift)
		print "Tj: ",Tj

		Shift = cij + wait + Tj + cjk - cik
		print "shift: ",Shift
		Sum_Wait_MaxShift = Locations[j].wait + Locations[j].max_shift

		return Shift if (Shift <= Sum_Wait_MaxShift) else Sum_Wait_MaxShift
		
	def update_locations(self,Locations,times,start,end):
		#Since location 0 is the origin and the last one the end of the tour:
		#Iterate from the second location until the penultimate location
		for i in range(1,len(Locations)-1):
			#print "i: ",i
			Locations[i].arrival = self.estimateArrival(0,Locations[i].id_location,times,start)
			#print "Location arrival: ", Locations[i].arrival
			
			Locations[i].wait = self.wait(Locations[i].opening, Locations[i].arrival)

			Locations[i].max_shift = self.maxShift(Locations, i, Locations[i].opening, Locations[i].closing, Locations[i].arrival, times,start,end)
			
			Locations[i].leave = self.getLeave(Locations,i)

			Locations[i].shift = self.Shift(Locations, i, i-1, times, start)
		
			Locations[i].ratio = self.ratio( Locations, i )
			
		return Locations

	def select_to_insert(self,Locations):
		percentage = 30 #percent
		ratios = [e.ratio for e in Locations]
		#Get radio value to select potential locations to choose
		selection_point = sum(ratios)*percentage/100
		potential_locations = [e for e in Locations if e.ratio >= selection_point]
		
		len_pot = len(potential_locations)
		index = random.randrange(0,len_pot)
		location_selected = potential_locations[index]
		"""
		print "random_number: ",index
		print "ratios: ",ratios
		print "select_point: ",selection_point
		print "potencial_locations: ",potential_locations
		"""
		#print "location_selected: ",location_selected
		#print "l sel: ",Locations[location_selected].id_location
		return location_selected

	def update_shift(self, Locations, times, start):

		for l in range(1,len(Locations)-1):
			Locations[l].shift = self.Shift(Locations,l+1,l, times, Locations[l].arrival)

		return Locations

	def update_arrival(self, Locations,times):
		print "in"
		for l in range(2,len(Locations)-1):
			i = Locations[l-1].id_location
			k = Locations[l].id_location
			Locations[l].arrival = Locations[l-1].leave+times[i][k]
			print "l id: ",k," arrival: ",Locations[l].arrival
		print "out"
		return Locations

	def update_leave(self, Locations):
		for l in range(1,len(Locations)-2):
			Locations[l].leave = Locations[l].arrival + Locations[l].max_shift

		return Locations

	def update_max_shift(self, Locations):
		for l in range(1,len(Locations)-2):
			potential_max = min(Locations[l].closing-Locations[l].arrival,Locations[l].wait+Locations[l+1].max_shift)

			Locations[l].max_shift = min(potential_max,1)

		return Locations

	def update_after_insertion(self,j,Locations,times,start,end):
		
		k = j+1
		"""
		Locations[j].shift = self.Shift(Locations, j, j-1, times, start)
		Locations[k].wait = max( 0, Locations[k].wait - Locations[j].shift )
		Locations[k].arrival = start+times[j][k]+Locations[j].shift#Locations[k].arrival + Locations[j].shift
		Locations[k].shift = max(0,Locations[j].shift - Locations[k].wait)
		
		print "k: ",k," loc id: ",Locations[k].id_location," shift: ",Locations[k].shift
		#Locations[k].start = Locations[k].start + Locations[k].shift
		Locations[k].max_shift = max(0,Locations[k].max_shift - Locations[k].shift)
		"""

		return Locations

	def set_at_better_position(Locations, location,start):
		shift_list = {}

		#for i in range(len(Locations)):



