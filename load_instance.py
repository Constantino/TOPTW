from location import location
from insertion_step import insertion_step
from ILS import ILS
from instance_generator import random_instance
"""
file = open('c101.txt', 'r')

lines = file.readlines()

new_lines = []

for line in lines:
	new_lines.append( line.split() )



for i in range(5):
	print new_lines[i]

"""

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
		print "-- x: ",e.x
		print "-- y: ",e.y
		print " "


start = 0 #hours
end = 1236 #hours
n = 100 #no. elements


instance = random_instance()


locations = instance.load_instance(n,start,end)

print_locations(locations)

