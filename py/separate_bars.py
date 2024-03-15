# takes a stave and separates it into bars

# PARAMETERS:
#   - numbers in for-loops's range in row_is_black()
#   - "enough" in is_black_enough() needs to be relatively lenient
#   - "enough" in is_white_enough() seems to be good-natured
#   - "exp_width" and "exp_height" for scale of exported pictures (needs to be consistent for NN)
#   - "min_dist_between_barlines" is the minimum distance between bars (avoids thick barlines creating pseudo-bars)

import math
from pathlib import Path
import os
import shutil
from PIL import Image, ImageColor

# if the sum of R, G and B is lesser than "enough", the pixel is considered as black
def is_black_enough (pixel):
    enough = 450
    if pixel[0]+pixel[1]+pixel[2] < enough:
        return True
    return False

# if the sum of R, G and B is greater than "enough", the pixel is considered as white
def is_white_enough (pixel):
    enough = 600
    if pixel[0]+pixel[1]+pixel[2] > enough:
        return True
    return False

# check if partial row is white
def part_row_is_white(point_y, left_border, right_border):
    for point_x in range(left_border, right_border):
        if is_white_enough( in_image.getpixel((point_x, point_y)) ) == False:
            return False
    return True

# check if entire row is black
def row_is_black (y_coord, width):
    for x_coord in range(int(0.4*width), int(0.6*width)):
        if is_black_enough( in_image.getpixel((x_coord, y_coord)) ) == False:
            return False
    return True

# check if this is a barline
def is_bar_line (x_coord, top_end, bot_end):
    # barline extends from top_end of the stave to the bot_end
    for y_coord in range(top_end, bot_end):
        if not is_black_enough( in_image.getpixel((x_coord, y_coord)) ):
            return False
    # barline does not go beyond stave
    if is_black_enough(in_image.getpixel((x_coord, top_end-2))) or is_black_enough(in_image.getpixel((x_coord, bot_end+2))):
        return False
    return True

##########################################################################################
##########################################################################################
##########################################################################################

# create folder for the images we want to export
if os.path.isdir('bars'):
    shutil.rmtree('bars')
os.makedirs('bars')

# top and bottom ends of the stave
top_end = 0
bot_end = 0

# list that holds positions of all the detected barlines
bar_lines = []

# barlines need to be min_dist_between_barlines apart from each other; don't set zero, or thick barlines will create pseudo-bars!
min_dist_between_barlines = 42

# size of exported images
exp_width = 100
exp_height = 25

##########################################################################################
##########################################################################################
##########################################################################################

print('Exporting bars... ', end='')

detected_bars = 0

for in_file in os.listdir(Path('lines')):
    in_image = Image.open(Path('lines') / in_file)
    width, height = in_image.size
    bar_lines.clear()

    # start at top center
    x_coord = math.floor(width/2)
    y_coord = 0

    # find top end of the stave
    while y_coord < height:
        if row_is_black (y_coord, width):
            top_end = y_coord
            break
        y_coord += 1
    if top_end == 0:
        print('Top end of stave not found, results useless.')

    # find bottom end of the stave
    y_coord = height - 1
    while y_coord > 0:
        if row_is_black (y_coord, width):
            bot_end = y_coord
            break
        y_coord -= 1
    if bot_end == 0:
        print('Bottom end of stave not found, results useless.')

    # find the beginning of the first bar (has no barline, so we aim for the center stave line)
    # if the line is not detected (eg tilted page), the clef should catch this
    x_coord = 0
    y_coord = int((top_end+bot_end)/2)
    for x_coord in range(width):
        if is_black_enough(in_image.getpixel((x_coord, y_coord))):
            bar_lines.append(x_coord)
            break

    # search for all barlines within the stave
    y_coord = int((7*top_end+bot_end)/8)
    for x_coord in range(width):
        if is_black_enough(in_image.getpixel((x_coord, y_coord))) \
        and is_bar_line(x_coord, top_end, bot_end) \
        and x_coord-bar_lines[-1] > min_dist_between_barlines:
            bar_lines.append(x_coord)

    # export the bars one by one
    while len(bar_lines) > 1:
        # shave away white rows
        top = 0
        while part_row_is_white(top, bar_lines[0], bar_lines[1]):
            top += 1
        bottom = height
        while part_row_is_white(bottom-1, bar_lines[0], bar_lines[1]):
            bottom -= 1

        # export the cropped picture
        file_name = str(detected_bars)
        while len(file_name) < 3:
            file_name = '0' + file_name
        file_name += '.png'
        out_image = in_image.crop((bar_lines[0], top-2, bar_lines[1], bottom+2))
        out_image = out_image.resize((exp_width, exp_height))
        out_image.save(Path('bars') / file_name)

        # preparations for next bar
        del bar_lines[0]
        detected_bars += 1

# done
print('DONE')

