import random
from location import location

class random_instance:
	
	Locations = []
	start = 0
	end = 0

	def generate_times(self, n):

		times = [ [ 0 ]*(i+1)+[random.randint(0,60)/60.0 for j in range(i,n) if j > i] for i in range(n) ]
		
		for i in range(1,n):
			for j in range(n):
				if j < i:
					times[i][j] = times[j][i]

		return times

	def generate(self, n, start, end):

		self.start = start
		self.end = end

		for i in range(n):
			self.Locations.append(location())
			if i == 0:
				self.Locations[0].id_location = i
				self.Locations[0].name = "start"
				self.Locations[0].opening = self.start
				self.Locations[0].closing = self.end
				self.Locations[0].score = 0
				self.Locations[0].max_shift = 0
				self.Locations[0].shift = 0
				self.Locations[0].ratio = 0
				self.Locations[0].arrival = 0
				self.Locations[0].leave = 0
			elif i == n-1:
				self.Locations[i].id_location = i
				self.Locations[i].name = "End"
				self.Locations[i].opening = start
				self.Locations[i].closing = end
				self.Locations[i].score = 0
				self.Locations[i].wait = 0
				self.Locations[i].max_shift = 0
				self.Locations[i].shift = 0
				self.Locations[i].ratio = 0
				self.Locations[i].arrival = 0
				self.Locations[i].leave = 0
			else:
				self.Locations[i].id_location = i
				self.Locations[i].name = "Loc"+str(i)
				self.Locations[i].opening = random.randint(8,17)
				self.Locations[i].closing = random.randint(self.Locations[i].opening,22)+1
				self.Locations[i].score = random.randint(1,5)
				self.Locations[i].wait = 0
				self.Locations[i].max_shift = 0
				self.Locations[i].shift = 0
				self.Locations[i].ratio = 0
				self.Locations[i].arrival = 0
				self.Locations[i].leave = 0

		return self.Locations
			

