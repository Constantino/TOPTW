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
	

print_locations(selected_locations)
