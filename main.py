from location import location
from insertion_step import insertion_step
from ILS import ILS
from instance_generator import random_instance

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
		

start = 8 #hours
end = 23 #hours
n = 5 #no. elements
instance = random_instance()

Locations = instance.generate(n,start,end)

times = instance.generate_times(n)

print_locations(Locations)

print "times:"
for e in times:
	print e

InsertionStep = insertion_step()

#Initialize all locations as if each of them where inserted between start and end of tour
Locations = InsertionStep.update_locations(Locations,times,start,end)

print_locations(Locations)
print "........"
selected_locations = []


#Add start location to the tour
selected_locations.append(Locations[0])
#xprint "append: ",Locations[len(Locations)-1].id_location
selected_locations.append(Locations[len(Locations)-1])
#<exp>

req_t = 1

while len(Locations) > 2:
	print "***---***"
	potential_inserts,local_information = InsertionStep.simulate_insertion(Locations, selected_locations, times)
	print "potential_inserts:"
	print_locations( potential_inserts )
	print "</potential_inserts"

	selected_one =  InsertionStep.select_potential_location(potential_inserts)
	print "selected one : ",selected_one.id_location
	before = local_information[selected_one.id_location]
	print "insert after : ",before
	selected_locations.insert(before+1,selected_one)
	Locations.remove(selected_one)
	print "***---***"

	selected_locations = InsertionStep.update_stuff(selected_locations,times,start)

	"""
	for index in range(len(selected_locations)):
		if index > before:
			selected_locations[index].arrival = InsertionStep.estimateArrival(index-1,index,times,selected_locations[index-1].leave)	
			print "update - index: ",index," arrival: ",selected_locations[index].arrival
	"""

	#selected_locations = InsertionStep.update_locations(selected_locations,times,start,end)

	#print "updating shift"
	#selected_locations = InsertionStep.update_shift(selected_locations,times)
	
	#selected_locations = InsertionStep.update_max_shift(selected_locations)
	
	"""
	print "updating arrival"
	selected_locations = InsertionStep.update_arrival(selected_locations,times)
	print "updating wait"
	selected_locations = InsertionStep.update_wait(selected_locations)

	#selected_locations = InsertionStep.update_max_shift(selected_locations)
	#selected_locations = InsertionStep.update_shift(selected_locations,times)
	
	print "updating leave"	
	selected_locations = InsertionStep.update_leave(selected_locations)
	
	print "updating ratio"
	selected_locations = InsertionStep.update_ratio(selected_locations)
	"""

print_locations(selected_locations)




"""
while len(Locations)>3: #number of index > 2; where "2" represents start and end location never removed

	#Select location for the tour
	selected = InsertionStep.select_to_insert(Locations)
	print "selected: ",selected
	#Add the new location to the tour
	#selected_locations.append(selected)
	#print "selected_locations.append(",selected.id_location,")"
	#Remove it from the common locations list
	print "removed l_location: ",selected.id_location
	Locations.remove(selected)
	
	selected_locations = InsertionStep.insert_location(selected_locations,selected,times,start)
	print "len locations: ", len(Locations)

#</exp>
#print "last one: ", Locations[1].name
#selected_locations = InsertionStep.insert_location(selected_locations,Locations[1],times,start)
#Add end location to the tour
#print "append: ",Locations[len(Locations)-1].id_location
#selected_locations.append(Locations[len(Locations)-1])


#Update Tour Locations after location_j
for x in range(selected_locations.index(selected_locations[1]),len(selected_locations)-2):
	selected_locations = InsertionStep.update_after_insertion(x,selected_locations,times,start,end)

#Update Tour Locations before location_j
for x in range(0,selected_locations.index(selected_locations[1])-1):
	selected_locations[x].max_shift = maxShift(selected_locations, 0, selected_locations[x].opening, Locations[x].closing, Locations[x].arrival, times,start,end)


#_Locations = InsertionStep.update_locations(selected_locations,times,start,end)



print "Test of shake step"
ILS = ILS()
print_locations(ILS.shake(selected_locations,1,1))
"""

