#catan_board.py

from PIL import Image
import random
import os

players = 0
possible_players = [3, 4, 5, 6]
while players not in possible_players:
	players = input("How many players? (3-6)...  ")

# Load Resources
resources = './Resources/'
hex_directory = resources + 'Hexes/'
# Hexes
hex_dict = {"field" : Image.open(hex_directory + "field.png"),
	"forest" : Image.open(hex_directory + "forest.png"),
	"pasture" : Image.open(hex_directory + "pasture.png"),
	"mountain" : Image.open(hex_directory + "mountain.png"),
	"hill" : Image.open(hex_directory + "hill.png"),
	"desert" : Image.open(hex_directory + "desert.png")}

num_directory = resources + 'Numbers/'
num_dict = {} # contains all the number token images
for x in xrange(len(os.listdir(num_directory))):
	num_filename = os.listdir(num_directory)[x]
	try:
		num_dict[num_filename.rstrip(".png")] = Image.open(num_directory + num_filename)
	except:
		pass

other = resources + 'Other/'
board_path = resources + 'Board/board.png'
if players in [3, 4]:
	coords_path = other + 'coords_base_3-4.txt'
	adj_path = other + 'adj_base_3-4.txt'
	num_list_path = other + 'nums_base_3-4.txt'
	hex_list_path = other + 'tiles_base_3-4.txt'
elif players in [5, 6]:
	coords_path = other + 'coords_base_5-6.txt'
	adj_path = other + 'adj_base_5-6.txt'
	num_list_path = other + 'nums_base_5-6.txt'
	hex_list_path = other + 'tiles_base_5-6.txt'

hex_coords = {}
coord_file = open(coords_path)
contents = coord_file.readlines()
for line in contents:
	line_list = line.split()
	hex_coords[int(line_list[0])] = (int(line_list[1]), int(line_list[2]))

hex_adj = {}
adj_file = open(adj_path)
contents = adj_file.readlines()
for line in contents:
	line_list = line.split('[')
	adj_list = line_list[1].split(',')
	hex_adj[int(line_list[0])] = []
	for number in adj_list:
		try:		 
			hex_adj[int(line_list[0])].append(int(number.rstrip(',]')))
		except:
			pass

num_list = []
num_list_file = open(num_list_path)
contents = num_list_file.readlines()
for line in contents:
	num_list.append(int(line))

hex_list = []
hex_list_file = open(hex_list_path)
contents = hex_list_file.readlines()
for line in contents:
	hex_list.append(hex_dict[line.rstrip()])

random.shuffle(hex_list)
random.shuffle(num_list)

tokencounter = 0
desert_hexes = []
number_assignments = {}
#board = Image.new("RGBA", (1920, 1200), (255, 255, 255))
# board = Image.new("RGBA", (1920, 1080), (255, 255, 255))
board = Image.open(board_path)
for i in xrange(len(hex_list)):
	hex_rotation = random.randint(0, 5) * 60
	hex_image = hex_list[i].rotate(hex_rotation)
	if players in [3, 4]:
		board.paste(hex_image, box = hex_coords[i], mask = hex_image)
	elif players in [5, 6]:
		board.paste(hex_image.resize())
	if hex_list[i] != hex_dict["desert"]: # assign a number to the hex if it's not a desert
		number_assignments[i] = num_list[tokencounter]
		tokencounter += 1
	else:
		desert_hexes.append(i)
	
def reset():
	random.shuffle(num_list)
	counter = 0
	for j in number_assignments:
		number_assignments[j] = num_list[counter]
		counter += 1
	return()

# test to make sure there aren't any adjacency problems
done = False
while not done:
	good = True
	for position in number_assignments: # keys in number_assignments
		for adj_pos in hex_adj[position]:
			if adj_pos not in desert_hexes:
				if number_assignments[position] in [6, 8] and number_assignments[adj_pos] in [6, 8]:
					good = False
				elif number_assignments[position] in [2, 12] and number_assignments[adj_pos] in [2, 12]:
					good = False
				else:
					pass
			if not good:
				break
		if not good:
			break
	if good:
		done = True
	else:
		reset()

for num in number_assignments:
	num_rotation = random.randint(0, 359)
	numtoken = num_dict[str(number_assignments[num])].resize((95, 95), Image.ANTIALIAS).rotate(num_rotation, Image.BICUBIC)
	if players in [3, 4]:
		board.paste(numtoken, box = (hex_coords[num][0] + 64, hex_coords[num][1]+ 82), mask = numtoken)
	elif players in [5, 6]:
		pass

board.save('temp.png')
board.show()