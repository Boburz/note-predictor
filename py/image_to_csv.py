# reads all images from bars/ and exports a CSV file as grayscales

from pathlib import Path
import os
from PIL import Image, ImageColor
import csv

def make_it_grey(pixel):
    return int( (pixel[0]+pixel[1]+pixel[2]) / 3 )

print('Exporting to csv... ', end='')

# create output file
output_file = Path('..\\grayscales.csv')
if os.path.isfile(output_file):
    os.remove(output_file)

# read all the images in ../bars
for image_file in os.listdir(Path('..\\bars')):
    pixel_list = []

    # open image
    in_image = Image.open(Path('..\\bars') / image_file)
    width, height = in_image.size

    # make list with pixels
    (x_coord, y_coord) = (0, 0)
    for y_coord in range(height):
        for x_coord in range(width):
            pixel_list.append( make_it_grey( in_image.getpixel((x_coord, y_coord)) ) )

    # write into output file
    with open(output_file, 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(pixel_list)

print('DONE')
