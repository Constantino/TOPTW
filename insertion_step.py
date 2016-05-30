import random
import copy

class insertion_step:

	def tw(self, locations, times, start):

		req_time = 1

		for i in range(1, len(locations)-1):
			
			if i == 1:
				locations[i].arrival = times[0][1]+start
			else:
				locations[i].arrival = self.estimateArrival(i-1,i,times,locations[i-1].leave)
			
			locations[i].wait = self.wait(locations[i].opening,locations[i].arrival)
			locations[i].leave = locations[i].arrival + locations[i].wait + req_time

		return locations

	def update_stuff(self, locations, times, start):

		#req_time = 10 #TIEMPO REQUERIDO

		for i in range(1,len(locations)-1):

			if i == 1:
				#locations[i].arrival = self.estimateArrival(i,i+1,times,start)
				locations[i].arrival = self.estimateArrival(i-1,i,times,start)
				locations[i].shift = self.Shift( locations, i , i-1, times, start)
			else:
				#locations[i].arrival = self.estimateArrival(i,i+1,times,locations[i-1].leave)
				locations[i].arrival = self.estimateArrival(i-1,i,times,locations[i-1].leave)
				locations[i].shift = self.Shift( locations, i , i-1, times, locations[i-1].leave)

			locations[i].wait = self.wait(locations[i].opening,locations[i].arrival)
			locations[i].leave = locations[i].arrival + locations[i].wait + locations[i].required_time # req_time
			locations[i].ratio = self.ratio(locations,i)

		return locations

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
		#print "leave from ",i,": ",leave
		arr2 = times[i][i+1]
		#print "arrival: ",arrival
		#print "next arrival: ",arr2
		max_shift = leave-arrival-arr2
		#print "max_shift: ",max_shift
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
		#print Locations[i].id_location

		#return Locations[i].score*1.0/Locations[i].shift if Locations[i].shift > 0 else 1
		#<exp> Need same unit than unit tests
		return Locations[i].score

	def Shift( self, Locations, j , i, times, start):
		#Get the total cost of time of including a location between location_i and location_k
		k = j+1
		cij = times[i][j]#self.estimateArrival( i, j, times, start )
		#print "cij: ", cij
		wait = Locations[j].wait
		#print "wait: ",wait
		
		cjk = times[j][k]#self.estimateArrival( j, k , times, start)
		#print "cjk: ",cjk
		cik = times[i][k]#self.estimateArrival( i, k, times, start)
		#print "cik: ",cik
		Tj = max(0,Locations[j].max_shift)
		#print "Tj: ",Tj

		Shift = cij + wait + Tj + cjk - cik
		#print "shift: ",Shift
		Sum_Wait_MaxShift = Locations[j].wait + Locations[j].max_shift

		return Shift if (Shift <= Sum_Wait_MaxShift) else Sum_Wait_MaxShift
	
	def ShiftSim( self, Locations, i, j, k, times):
		#Get the total cost of time of including a location between location_i and location_k
		cij = times[i][j]#self.estimateArrival( i, j, times, start )
		#print "cij: ", cij
		wait = Locations[1].wait
		#print "wait: ",wait
		
		cjk = times[j][k]#self.estimateArrival( j, k , times, start)
		#print "cjk: ",cjk
		cik = times[i][k]#self.estimateArrival( i, k, times, start)
		#print "cik: ",cik
		Tj = max(0,Locations[1].max_shift)
		#print "Tj: ",Tj

		Shift = cij + wait + Tj + cjk - cik
		#print "shift: ",Shift
		Sum_Wait_MaxShift = Locations[1].wait + Locations[1].max_shift

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
		
		#for e in potential_locations:
		#	print "potential: ",e.id_location

		len_pot = len(potential_locations)-1
		index = random.randint(0,len_pot)
		location_selected = potential_locations[index]
		
		#location_selected = random.choice(potential_locations)
		#print "**location_selected: ",location_selected.id_location
		#print "len_pot: ",len_pot
		#for l in potential_locations:
		#	print "potencial_location: ",e.id_location, "  index: ",index
		"""
		print "random_number: ",index
		print "ratios: ",ratios
		print "select_point: ",selection_point
		print "potencial_locations: ",potential_locations
		"""
		#print "location_selected: ",location_selected
		#print "l sel: ",Locations[location_selected].id_location

		return location_selected

	def update_ratio(self, Locations):

		for l in range(1,len(Locations)-1):
			Locations[l].ratio = self.ratio(Locations,l)


		return Locations

	def update_shift(self, Locations, times):

		for l in range(1,len(Locations)-2):
			Locations[l].shift = self.Shift(Locations,l+1,l, times, Locations[l].arrival)

		return Locations

	def update_wait(self, Locations):

		for l in range(1,len(Locations)-1):
			Locations[l].wait = self.wait(Locations[l].opening,Locations[l].arrival)
			#print "wait: ",Locations[l].wait, " --- l: ",l, " opening: ",Locations[l].opening, " arrival: ",Locations[l].arrival
		return Locations

	def update_arrival(self, Locations,times):
		#print "in"
		for l in range(2,len(Locations)-1):
			i = Locations[l-1].id_location
			k = Locations[l].id_location
			Locations[l].arrival = Locations[l-1].leave+times[i][k]
			#print "l id: ",k," arrival: ",Locations[l].arrival
		#print "out"
		return Locations

	def update_leave(self, Locations):
		for l in range(1,len(Locations)-2):
			Locations[l].leave = Locations[l].arrival + Locations[l].max_shift + Locations[l].wait

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

	def insert_location(self, Locations, selected, times, start):
		ratio_list = []
		#print len(Locations)
		for l in range(len(Locations)-1):
			Locations_tmp = [Locations[l],selected,Locations[l+1]]
			shift = self.Shift(Locations_tmp, l+1, l, times, start)
			ratio_list.append(selected.score*1.0/shift if shift > 0 else 1)

		#print "len ratio_list: ",len(ratio_list)
		selected_index = shift_list.index(max(ratio_list))+1

		#print "<shifts>"
		#print shift_list
		#print "insert at index: ",selected_index
		#print "</shifts>"
		Locations.insert(selected_index,selected)

		return Locations


	def simulate_insertion(self, Locations, selected, times):
		potential_inserts = []
		local_information = {}
		for l in range(1,len(Locations)-1):
			local = [0,-1,-1]
			for s in range(len(selected)-1):
				tmp = [ selected[s],Locations[l],selected[s+1] ]
				#print "i:",selected[s].id_location," j:",Locations[l].id_location," k: ",selected[s+1].id_location
				
				shift = self.ShiftSim(tmp, selected[s].id_location,Locations[l].id_location,selected[s+1].id_location, times)
				ratio = Locations[l].score*1.0/shift if shift > 0 else 1
				
				#validate time windows
				
				if self.validate_time_windows(selected,Locations[l], s, times):
					#print "TIME WINDOW VALIDATED: ",s
					if ratio > local[1]:
						local[0] = Locations[l]
						local[1] = ratio
						local[2] = s #after this index
					#print "--- ratio: ", ratio
				
				
				"""
				if ratio > local[1]:
					local[0] = Locations[l]
					local[1] = ratio
					local[2] = s #after this index
					print "--- ratio: ", ratio
				"""

			if local[1] != -1:
				#print "local: ",local
				potential_inserts.append(local[0])
				local_information[local[0].id_location] = local[2]
				#print "local_information: ", local_information

		return potential_inserts, local_information

	def validate_time_windows(self, s_l, location, index, times):
		
		#BUG
		selected_locations = copy.copy(s_l)
		selected_locations.insert(index+1,location)

		"""
		print "validate_time_windows:"
		print "s index: ",index
		print "location to insert: ",location.id_location
		"""

		"""
		for e in selected_locations:
			print "-- location ID: ",e.id_location
			print "-- name: ",e.name
			print "-- score: ",e.score
			print "-- opening: ",e.opening
			print "-- closing: ",e.closing
			print "-- arrival: ",e.arrival
			print "-- wait: ",e.wait
			print "-- max_shift: ",e.max_shift
			print "-- shift: ",e.shift
			print "-- ratio: ",e.ratio
			print "-- leave: ",e.leave
			print " "
		"""

		req_time = 1
		start = 8

		selected_locations = self.update_stuff(selected_locations,times,start)

		"""
		#Update properties from 
		print "updating shift"
		selected_locations = self.update_shift(selected_locations,times)
		
		selected_locations = self.update_max_shift(selected_locations)
		
		selected_locations = self.update_leave(selected_locations)
		print "updating arrival"
		selected_locations = self.update_arrival(selected_locations,times)
			
		print "updating wait"
		selected_locations = self.update_wait(selected_locations)
		
		print "updating ratio"
		selected_locations = self.update_ratio(selected_locations)

		"""

		for e in selected_locations:
			#print "TW --- arrival: ",e.arrival, "closing: ",e.closing
			if e.arrival >= (e.closing - req_time):

				return False
		
		return True 

	def select_potential_location(self, Locations):

		if len(Locations) == 0:
			return []

		ratios = [e.ratio for e in Locations]
		#Get radio value to select potential locations to choose
		ratio_max = max(ratios)
		selection_point = ratio_max - 0.3*(ratio_max - min(ratios))
		potential_locations = [e for e in Locations if e.ratio >= selection_point]

		len_pot = len(potential_locations)-1
		index = random.randint(0,len_pot)
		location_selected = potential_locations[index]
		#print "||||"
		#print "selection_point: ", selection_point
		#print "|||| *** len_pot: ",len_pot
		#print "|||| *** location: ", location_selected.id_location," index: ", index
		#print "||||"

		#print "selection_point: ",selection_point
		return location_selected







