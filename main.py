from location import location
from insertion_step import insertion_step

def print_locations(Locations):
	print "TOUR: "
	print "Start: ",start
	print "End: ",end
	print "Locations:"
	for e in Locations:
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
		

start = 9 #hours
end = 13#hours

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


Locations[4].id_location = 3
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

times = [
#0     1     2    3  4
[0,   0.5, 1.3, 0.3, 1], # 0
[0.5, 0,   0.8, 2,   1], # 1
[1.3, 0.7, 0,   1,   1], # 2
[0.3, 2,   1,   0,   1], # 3
[1,   1,   1,   1,   0]  # 4
]

InsertionStep = insertion_step()

Locations = InsertionStep.update_locations(Locations,times,start,end)

print_locations(Locations)
print "........"
selected_locations = []


#Add start location to the tour
selected_locations.append(Locations[0])

while len(Locations) > 2: #number of index > 2; where "2" represents start and end location never removed

	#Select location for the tour
	selected = InsertionStep.select_to_insert(Locations)
	print "selected: ",selected
	
	#Add the new location to the tour
	selected_locations.append(selected)
	print "selected_locations.append( ",selected.id_location
	#Remove it from the common locations list
	print "removed l_location: ",selected.id_location
	Locations.remove(selected)

#Add end location to the tour
print "append: ",Locations[len(Locations)-1].id_location
selected_locations.append(Locations[len(Locations)-1])

selected_locations = InsertionStep.update_max_shift(selected_locations)
selected_locations = InsertionStep.update_leave(selected_locations)

print "up arrival"
selected_locations = InsertionStep.update_arrival(selected_locations,times)
print "up wait"
selected_locations = InsertionStep.update_wait(selected_locations)
print "up shift"
selected_locations = InsertionStep.update_shift(selected_locations,times)

"""
#Update Tour Locations after location_j
for x in range(selected_locations.index(selected_locations[1]),len(selected_locations)-2):
	selected_locations = InsertionStep.update_after_insertion(x,selected_locations,times,start,end)
"""

"""	
#Update Tour Locations before location_j
for x in range(0,selected_locations.index(selected_locations[1])-1):
	selected_locations[x].max_shift = maxShift(selected_locations, 0, selected_locations[x].opening, Locations[x].closing, Locations[x].arrival, times,start,end)
"""

#_Locations = InsertionStep.update_locations(selected_locations,times,start,end)

print_locations(selected_locations)

