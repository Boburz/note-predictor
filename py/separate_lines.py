# takes a sheet of music and separates it into lines of music

# PARAMETERS (seem ok like this): nec_white_rows, enough (in is_black_enough() and is_white_enough())

import math
import shutil
from pathlib import Path
import os

from PIL import Image, ImageColor

# if the sum of R, G and B is lesser than "enough", the pixel is considered as black
def is_black_enough (pixel):
    enough = 120
    if pixel[0]+pixel[1]+pixel[2] < enough:
        return True
    return False

# if the sum of R, G and B is greater than "enough", the pixel is considered as white
def is_white_enough (pixel):
    enough = 600
    if pixel[0]+pixel[1]+pixel[2] > enough:
        return True
    return False

# check if entire row is white
def row_is_white (y_coord, width):
    for x_coord in range(width):
        if is_white_enough( score_image.getpixel((x_coord, y_coord)) ) == False:
            return False
    return True

print('Exporting lines... ', end='')

# create folder for the images we want to export
if os.path.isdir('lines'):
    shutil.rmtree('lines')
os.makedirs('lines')

# open file
score_image = Image.open(Path('input.jpg'))
width, height = score_image.size
top = 0
bottom = height
left = 0
right = width

# start at top center
x_coord = int(width/2)
y_coord = 0
detected_lines = 0
num_white_rows = 0
nec_white_rows = 10

while y_coord < height:
    # move down until a black pixel is found, which indicates some sort of stave/note/whatever
    while y_coord < height:
        if is_black_enough( score_image.getpixel((x_coord, y_coord)) ) == True:
            break
        y_coord += 1

    # now move down until you find a white pixel again, which could be the end of the stave
    while y_coord < height:
        y_coord += 1

        # is the entire row white?
        if row_is_white (y_coord, width):
            num_white_rows += 1
        else:
            num_white_rows = 0

        # if some (meaning nec_white_rows) rows have been white, we have reached the end of the stave
        if num_white_rows == nec_white_rows:
            #end of stave has been found, print output
            file_name = 'output_' + str(detected_lines) + '.jpg'
            out_image = score_image.crop((left, top, right, y_coord))
            out_image.save(Path('lines') / file_name)

            # preparations for next line
            detected_lines += 1
            top = y_coord
            break

print('DONE')

