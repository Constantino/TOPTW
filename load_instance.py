file = open('c101.txt', 'r')

lines = file.readlines()

new_lines = []

for line in lines:
	new_lines.append( line.split() )

for i in range(5):
	print new_lines[i]
