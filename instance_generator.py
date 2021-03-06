import random
from location import location
import math

class random_instance:
	
	Locations = []
	start = 0
	end = 0

	def EuclideanDistance(self, L1, L2):

		return math.sqrt( pow(float(L1.x) - float(L2.x), 2) + pow(float(L1.y) - float(L2.y), 2) )

	def generate_times_for_instances(self, n, Locations):

		#times = [ [ 0 ]*(i+1)+[random.randint(0,60)/60.0 for j in range(i,n) if j > i] for i in range(n) ]
		times = [ [ 0 ]*(i+1)+[ self.EuclideanDistance(Locations[i],Locations[j]) for j in range(i,n) if j > i] for i in range(n) ]
		
		for i in range(1,n):
			for j in range(n):
				if j < i:
					times[i][j] = times[j][i]

		return times

	def load_instance(self, n, file_name):

		n = n+2 # + start and end

		#file = open('c101.txt', 'r') #identify file name
		file = open(file_name, 'r') #identify file name

		lines = file.readlines()

		new_lines = []

		for line in lines:
			new_lines.append( line.split() )


		self.start = 0
		self.end = float(new_lines[2][8])

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
				self.Locations[0].x = new_lines[2][1]
				self.Locations[0].y = new_lines[2][2]
				self.Locations[0].required_time = float(new_lines[2][3])

				new_lines.pop(0)
				new_lines.pop(0)

			elif i == n-1:
				self.Locations[i].id_location = i
				self.Locations[i].name = "End"
				self.Locations[i].opening = self.start
				self.Locations[i].closing = self.end
				self.Locations[i].score = 0
				self.Locations[i].wait = 0
				self.Locations[i].max_shift = 0
				self.Locations[i].shift = 0
				self.Locations[i].ratio = 0
				self.Locations[i].arrival = 0
				self.Locations[i].leave = 0
				self.Locations[i].x = new_lines[0][1]
				self.Locations[i].y = new_lines[0][2]
				self.Locations[i].required_time = float(new_lines[0][3])

			else:
				self.Locations[i].id_location = i
				self.Locations[i].name = "Loc"+str(i)
				self.Locations[i].opening = float(new_lines[i][8])
				self.Locations[i].closing = float(new_lines[i][9])
				self.Locations[i].score = float(new_lines[i][4])
				self.Locations[i].wait = 0
				self.Locations[i].max_shift = 0
				self.Locations[i].shift = 0
				self.Locations[i].ratio = 0
				self.Locations[i].arrival = 0
				self.Locations[i].leave = 0
				self.Locations[i].x = new_lines[i][1]
				self.Locations[i].y = new_lines[i][2]
				self.Locations[i].required_time = float(new_lines[i][3])

		return self.Locations, self.start, self.end

	def generate_times(self, n):

		times = [ [ 0 ]*(i+1)+[random.randint(0,60)/60.0 for j in range(i,n) if j > i] for i in range(n) ]
		
		for i in range(1,n):
			for j in range(n):
				if j < i:
					times[i][j] = times[j][i]

		return times

	"""
	def generate_times(self, n,h):

		times = [
		#0     1     2    3  4
		[0,   0.5, 1.3, 1.5, 1], # 0
		[0.5, 0,   0.8, 2,   1], # 1
		[1.3, 0.8, 0,   1,   1], # 2
		[0.3, 2,   1,   0,   1], # 3
		[1,   1,   1,   1,   0]  # 4
		]

		return times
	"""


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
				self.Locations[i].opening = random.randint(8,11)
				self.Locations[i].closing = random.randint(self.Locations[i].opening,20)+1
				self.Locations[i].score = random.randint(1,5)
				self.Locations[i].wait = 0
				self.Locations[i].max_shift = 0
				self.Locations[i].shift = 0
				self.Locations[i].ratio = 0
				self.Locations[i].arrival = 0
				self.Locations[i].leave = 0

		return self.Locations

	"""
	def generate(self, n, start, end,h):

		Locations = []

		for e in range(5):
			Locations.append(location())

		#Instance of 5 elements
		Locations[0].id_location = 0
		Locations[0].name = "start"
		Locations[0].opening = start
		Locations[0].closing = end
		Locations[0].score = 0
		Locations[0].max_shift = 0
		Locations[0].shift = 0
		Locations[0].ratio = 0
		Locations[0].arrival = 0
		Locations[0].leave = 0

		Locations[1].id_location = 1		
		Locations[1].name = "Loc2"
		Locations[1].opening = 9
		Locations[1].closing = 20
		Locations[1].score = 5
		Locations[1].max_shift = 0
		Locations[1].shift = 0
		Locations[1].ratio = 0
		Locations[1].arrival = 0
		Locations[1].leave = 0


		Locations[2].id_location = 2
		Locations[2].name = "Loc3"
		Locations[2].opening = 12
		Locations[2].closing = 23
		Locations[2].score = 3
		Locations[2].max_shift = 0
		Locations[2].shift = 0
		Locations[2].ratio = 0
		Locations[2].arrival = 0


		Locations[3].id_location = 3
		Locations[3].name = "Loc4"
		Locations[3].opening = 10
		Locations[3].closing = 19
		Locations[3].score = 4
		Locations[3].wait = 0
		Locations[3].max_shift = 0
		Locations[3].shift = 0
		Locations[3].ratio = 0
		Locations[3].arrival = 0
		Locations[3].leave = 0


		Locations[4].id_location = 4
		Locations[4].name = "End"
		Locations[4].opening = start
		Locations[4].closing = end
		Locations[4].score = 0
		Locations[4].wait = 0
		Locations[4].max_shift = 0
		Locations[4].shift = 0
		Locations[4].ratio = 0
		Locations[4].arrival = 0
		Locations[4].leave = 0

		return Locations
	"""


					

