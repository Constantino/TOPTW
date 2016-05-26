from location import location
from insertion_step import insertion_step
from ILS import ILS
from instance_generator import random_instance
import math
import time

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
		

def getTourRatio(Locations):
	ratio = 0
	for e in Locations:
		ratio += e.ratio

	return ratio


def getTour(Locations, times, start, end):
	
	if len(Locations) == 0:
		return [],[]

	#Initialize all locations as if each of them where inserted between start and end of tour
	Locations = InsertionStep.update_locations(Locations,times,start,end)

	#print_locations(Locations)
	#print "........"
	selected_locations = []


	#Add start location to the tour
	selected_locations.append(Locations[0])
	selected_locations.append(Locations[len(Locations)-1])

	req_t = 1
	loopCounter = 0
	while len(Locations) > 2:
		#print "***-- loop --***"

		potential_inserts,local_information = InsertionStep.simulate_insertion(Locations, selected_locations, times)
		#print "potential_inserts:"
		#print_locations( potential_inserts )
		#print "</potential_inserts"

		selected_one =  InsertionStep.select_potential_location(potential_inserts)
		
		if selected_one != []:
			
			#print "selected one : ",selected_one.id_location

			before = local_information[selected_one.id_location]
			#print "insert after : ",before
			selected_locations.insert(before+1,selected_one)
			Locations.remove(selected_one)
			#print "***---***"
			selected_locations = InsertionStep.update_stuff(selected_locations,times,start)
		else:
			break

	selected_locations = InsertionStep.update_stuff(selected_locations,times,start)
	#print_locations(selected_locations)

	return selected_locations, Locations

def completeTour(Locations, selected_locations, times, start, end):
	
	if len(Locations) == 0:
		return [], Locations

	while len(Locations) > 2:
		#print "***---***"
		potential_inserts,local_information = InsertionStep.simulate_insertion(Locations, selected_locations, times)
		#print "potential_inserts:"
		#print_locations( potential_inserts )
		#print "</potential_inserts"
		selected_one =  InsertionStep.select_potential_location(potential_inserts)

		if selected_one != []:
		
			#print "selected one : ",selected_one.id_location
			before = local_information[selected_one.id_location]
			#print "insert after : ",before
			
			#if not IsDuplicate():
			selected_locations.insert(before+1,selected_one)
			Locations.remove(selected_one)
			#print "***---***"
			selected_locations = InsertionStep.update_stuff(selected_locations,times,start)

		else:
			break

	selected_locations = InsertionStep.update_stuff(selected_locations,times,start)

	return selected_locations, Locations

def IsDuplicate(Tour, element):
	for e in Tour:
		if e.id_location == element.id_location:
			return True
	return False	

def shake(RestOfLocations, Locations, R,S):
	S += 1
	for l in range(S,S+R):
		ln_loc = len(Locations) 
		i = 1 if l >= (ln_loc-1) else l
		if ln_loc > 2 and i < (ln_loc-1) and i > 0 :
			#print "shake -> removing location: ",Locations[i].id_location

			if Locations[i].name.lower() != "end" or Locations[i].name.lower() != "start":
				RestOfLocations.append( Locations[i] )

			Locations.remove( Locations[i] )

	return Locations


"""
start = 0 #hours
end = 1236 #hours
n = 100 #no. elements

instance = random_instance()

Locations = instance.generate(n,start,end)

times = instance.generate_times(n)

print_locations(Locations)
"""

##########################
#NEW INVOCATION
##########################

#start counting time
start_time = time.time()

start = 0 #hours
end = 1236 #hours
n = 100 #no. elements

instance = random_instance()

Locations = instance.load_instance(n,start,end)

times = instance.generate_times_for_instances(len(Locations),Locations)

#print_locations(Locations)

##########################
#END NEW INVOCATION
##########################

"""
print "times:"
for e in times:
	print e
"""

InsertionStep = insertion_step()


###########################################
#########			ILS			 ##########
###########################################

#tour = getTour(Locations, times, start, end)
#print "Tour ratio: ", getTourRatio(tour)

S = 1
R = 1

NoImprovementCounter = 0
SmallestTourSize = -1
TourFlag = 0

NewTour, RestOfLocations = getTour(Locations, times, start, end)
OriginalSolution = NewTour[:]

BestFound = {"ratio": getTourRatio(NewTour), "tour":NewTour}

tour = []

#Print new tour
#print_locations(BestFound['tour'])


RestOfLocations.remove( RestOfLocations[0])
RestOfLocations.remove( RestOfLocations[-1])

#print "OriginalSolution: ", getTourRatio( OriginalSolution )

TourRatio = getTourRatio(NewTour)

#print "#############################"
#print "#########	ILS	   #########"
#print "#############################"

while NoImprovementCounter < 50:
	"""
	print "--- <RestOfLocations> ---"
	print_locations(RestOfLocations)
	print "--- </RestOfLocations> ---"
	"""

	#CompleteTour
	if TourFlag == 1:
		#print "completeTour"
		NewTour, RestOfLocations = completeTour(RestOfLocations, tour, times, start, end)

		#print_locations(NewTour)
		TourRatio = getTourRatio(NewTour)
	
	
	ln_NewTour = len(NewTour)

	if SmallestTourSize == -1 or ln_NewTour < SmallestTourSize:
		SmallestTourSize = ln_NewTour

	#print "++++++++++++++++++++++++++++++++++"
	if BestFound['ratio'] < TourRatio:
		#Assign new tour as local optimum
		#print "======================================"
		#print "new best found"
		BestFound['tour'] = NewTour
		BestFound['ratio'] = TourRatio

		R = 1
		NoImprovementCounter = 0

	else:
		NoImprovementCounter += 1
	
	#print "++++++++++++++++++++++++++++++++++"

	#tour = shake(RestOfLocations, BestFound['tour'][:], R, S)
	tour = shake(RestOfLocations, NewTour[:], R, S)
	TourFlag = 1

	S = S + R
	R = R + 1

	if S >= SmallestTourSize:
		S = S - SmallestTourSize

	if R >= ( len(BestFound['tour'])/2.0 ) - 2: #No eliminar > del 50% de elementos en el tour
		R = 1


#print "** NoImprovementCounter = ",NoImprovementCounter

#print "###########################"
#print "###      BEST FOUND     ###"
#print "###########################"

BestFound['tour'] = InsertionStep.update_stuff(BestFound['tour'][:],times,start)
#print_locations(BestFound['tour'])

nombre_instancia = "c101"
bk = getTourRatio( OriginalSolution )
ils = getTourRatio( BestFound['tour'] )
elapsed_time = time.time() - start_time
gap = (bk-ils)/bk
#print "OriginalSolution: ", getTourRatio( OriginalSolution )
#print "EnhancedSolution: ", getTourRatio( BestFound['tour'] )
print nombre_instancia,", ",bk,",",ils,",",abs(gap)*100,",",elapsed_time


