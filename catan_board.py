# catan_board.py

import PIL
import PIL.Image
from PIL import Image
import random
import os

RESOURCE_DIR = './Resources/'
HEX_DIR = RESOURCE_DIR + 'Hexes/'
NUM_DIR = RESOURCE_DIR + 'Numbers/'
OTHER_DIR = RESOURCE_DIR + 'Other/'


hex_img_dict = {"field": Image.open(HEX_DIR + "field.png"),
                "forest": Image.open(HEX_DIR + "forest.png"),
                "pasture": Image.open(HEX_DIR + "pasture.png"),
                "mountain": Image.open(HEX_DIR + "mountain.png"),
                "hill": Image.open(HEX_DIR + "hill.png"),
                "desert": Image.open(HEX_DIR + "desert.png")}


def make_num_img_dict():
    num_img_dict = {}
    for num_filename in os.listdir(NUM_DIR):
        try:  # wrap in try/except because of those annoying little ".DS_store" files
            num_img_dict[num_filename.rstrip(".png")] = Image.open(
                NUM_DIR + num_filename)
        except:
            pass
    return num_img_dict


num_img_dict = make_num_img_dict()


num_players = 3  # until I can figure out input again
POSSIBLE_PLAYERS = [3, 4, 5, 6]
while num_players not in POSSIBLE_PLAYERS:
    num_players = input("How many players? (3-6)...  ")

BOARD_PATH = RESOURCE_DIR + 'Board/board.png'  # TODO make a 5-6 player board


def select_other_resources():
    if num_players in [3, 4]:
        suffix = "3-4.txt"
    else:
        suffix = "5-6.txt"
    image_coords_path = OTHER_DIR + "coords_base_" + suffix
    adjacent_path = OTHER_DIR + "adj_base_" + suffix
    num_list_path = OTHER_DIR + "nums_base_" + suffix
    hex_list_path = OTHER_DIR + "tiles_base_" + suffix
    return image_coords_path, adjacent_path, num_list_path, hex_list_path


COORDS_PATH, ADJ_PATH, NUM_LIST_PATH, HEX_LIST_PATH = select_other_resources()


def make_hex_coords():
    hex_coords = {}
    for line in open(COORDS_PATH).readlines():
        split_line = line.split()
        hex_coords[int(split_line[0])] = (
            int(split_line[1]), int(split_line[2]))
    return hex_coords


def make_hex_adj():
    hex_adj = {}
    for line in open(ADJ_PATH).readlines():
        split_at_bracket = line.strip().rstrip(',]').split('[')
        hex_adj[int(split_at_bracket[0])] = list(
            map(int, split_at_bracket[1].split(',')))
    return hex_adj


def make_num_list():
    contents = open(NUM_LIST_PATH).readlines()
    num_list = list(map(int, contents))
    return num_list


def make_hex_list():
    hex_img_list = []
    contents = open(HEX_LIST_PATH).readlines()
    for line in contents:
        hex_img_list.append(hex_img_dict[line.rstrip()])
    return hex_img_list


hex_coords = make_hex_coords()
hex_adj = make_hex_adj()
num_list = make_num_list()
hex_img_list = make_hex_list()

random.shuffle(hex_img_list)
random.shuffle(num_list)

tokencounter = 0
desert_hexes = []
number_assignments = {}

board_img = Image.open(BOARD_PATH)

# TODO
"""
def paste_hexes():
    for i in hex_img_list:
        hex_rotation = random.randint(0, 5) * 60
        if num_players in [3, 4]:
            board_img.paste
            """

for i in range(len(hex_img_list)):
    hex_rotation = random.randint(0, 5) * 60
    hex_image = hex_img_list[i].rotate(hex_rotation)
    if num_players in [3, 4]:
        board_img.paste(hex_image, box=hex_coords[i], mask=hex_image)
    elif num_players in [5, 6]:
        board_img.paste(hex_image.resize())
    # assign a number to the hex if it's not a desert
    if hex_img_list[i] != hex_img_dict["desert"]:
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
    for position in number_assignments:  # keys in number_assignments
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
    numtoken = num_img_dict[str(number_assignments[num])].resize(
        (95, 95), Image.ANTIALIAS).rotate(num_rotation, Image.BICUBIC)
    if num_players in [3, 4]:
        board_img.paste(numtoken, box=(
            hex_coords[num][0] + 64, hex_coords[num][1] + 82), mask=numtoken)
    elif num_players in [5, 6]:
        pass

# board.save('temp.png')
board_img.show()
