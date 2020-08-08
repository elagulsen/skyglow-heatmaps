#!/usr/bin/python

# pittsburgh light pollution heat map generation
# for the CMU skyglow class, summer 2020
# by Ela Gulsen
# using data sets provided by Dark Sky Meter and Globe At Night

import csv
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import math
import matplotlib.image as mpimg
import os
import sys
from PIL import Image

#SYNTAX: heatmap.py DIM, RADIUS, SIGMA, ALPHA

#these are aesthetic and can be adjusted as you see fit
#higher dimensions can take a while so use 100 and 5 for testing

import time
start = time.time()

DIM,RADIUS,SIGMA,ALPHA = None,None,None,None
for arg in sys.argv:
    if 'DIM=' in arg or 'D=' in arg:
        DIM = int(arg.split('=')[1])
    elif 'RADIUS=' in arg or 'RAD=' in arg or 'R=' in arg:
        RADIUS = int(arg.split('=')[1])
    elif 'SIGMA=' in arg or 'SIG=' in arg or 'S=' in arg:
        SIGMA = float(arg.split('=')[1])
    elif 'ALPHA=' in arg or 'A=' in arg:
        ALPHA = float(arg.split('=')[1])

DIM = 300 if not DIM else DIM
RADIUS = int(DIM/30) if not RADIUS else RADIUS
SIGMA = float(RADIUS/4) if not SIGMA else SIGMA
ALPHA = 0.7 if not ALPHA else ALPHA

print('Generating heatmap now with dimension ' + str(DIM) + ', radius ' + str(RADIUS) + ', sigma ' + str(SIGMA) + ', and alpha ' + str(ALPHA) + '.')
if DIM>500:
    print('Since your dimension is greater than 500, this may take a bit! Please be patient.')

#border of pittsburgh
LAT_MIN = 40.35
LAT_MAX = 40.55
LONG_MIN = -80.15
LONG_MAX = -79.8

#latitude = row[3]
#longitude = row[4]
#sqm = row[11]

file_names = ['GaN2019_2.csv', 'GaN2018_2.csv', 'GaN2017_2.csv', 'GaN2016_2.csv', 'GaN2015_2.csv', 'GaN2014_2.csv', 'reordered_dsm.csv']

data = np.zeros((DIM, DIM))

averages = [[0] * DIM for i in range(DIM)]

def NonLinCdict(steps, hexcol_array):
    cdict = {'red': (), 'green': (), 'blue': ()}
    for s, hexcol in zip(steps, hexcol_array):
        rgb =matplotlib.colors.hex2color(hexcol)
        cdict['red'] = cdict['red'] + ((s, rgb[0], rgb[0]),)
        cdict['green'] = cdict['green'] + ((s, rgb[1], rgb[1]),)
        cdict['blue'] = cdict['blue'] + ((s, rgb[2], rgb[2]),)
    return cdict
#without countours

hc = ['#0000ff', '#ffffff', '#FF69B4', '#f7163f', '#f7a325', '#f7b016', '#f7e816', '#bde204', '#16f734', '#168ef7', '#939596'] #COLORS
th = [0, 0.001, 0.2, 0.25, 0.36, 0.45, 0.55, 0.65, 0.7, 0.8, 1]

cdict = NonLinCdict(th, hc)
cm = matplotlib.colors.LinearSegmentedColormap('test', cdict)

def add_data_pt(avg_list, lat, long, sqm):
    if isinstance(avg_list[lat][long], list):
        cur_val = avg_list[lat][long][0]
        num_data_pts = avg_list[lat][long][1]
        avg_list[lat][long][0] = sqm #((num_data_pts*cur_val)+sqm)/(num_data_pts+1) #average
        avg_list[lat][long][1] += 1
    else:
        avg_list[lat][long] = [sqm, 1]

def add_radius(avg_list, lat, long, sqm, radius):
    for x in range(DIM):
        for y in range(DIM):
            distance = math.sqrt((x-long)**2 + (y-lat)**2)
            if distance <= radius:
                add_data_pt(avg_list, x, y, sqm)

for file_name in file_names:
    with open('datasets/' + file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            try: #some of the rows are empty/have missing values which causes errors, we can skip those lines
                if float(row[3]) < LAT_MAX and float(row[3]) > LAT_MIN and float(row[4]) < LONG_MAX and float(row[4]) > LONG_MIN:
                    #remember that since longitude is negative, the heatmap is actually reversed.
                    #^ this problem is solved by subtracting long from DIM.
                    lat = DIM*(LAT_MAX-float(row[3]))/(LAT_MAX-LAT_MIN)
                    long = DIM - DIM*(LONG_MAX-float(row[4]))/(LONG_MAX-LONG_MIN)
                    #print(lat, long)
                    add_radius(averages, long, lat, float(row[11]), RADIUS)
            except:
                pass

for x in range(DIM):
    for y in range(DIM):
        try:
            data[x][y] = averages[x][y][0]
        except:
            data[x][y] = 0

from scipy.ndimage.filters import gaussian_filter
data = gaussian_filter(data, sigma=SIGMA)

with open("fulldataset.csv", 'w+') as dataset:
    dataWriter = csv.writer(dataset,delimiter=',')
    dataWriter.writerows(data)

plt.subplots(figsize=(22.5,15))
heat_map = sb.heatmap(data, cmap=cm, vmin=14, vmax=23, alpha=1, xticklabels=False, yticklabels=False)
#plt.show()

# get the map image as an array so we can plot it
import matplotlib.image as mpimg
map_img_bottom = mpimg.imread('img/bigger-map-all.png')
map_img_top = mpimg.imread('img/bigger-map-gray.png')
map_img_mid = mpimg.imread('img/bigger-map-gray-border-only2.png')

hmax = heat_map

hmax.imshow(map_img_mid,
          aspect = hmax.get_aspect(),
          extent = hmax.get_xlim() + hmax.get_ylim(),
          zorder = 0)

plt.savefig("heatmap2.png")
#plt.show()

# get the map image as an array so we can plot it

map_img = mpimg.imread('heatmap2.png')

hmax = heat_map

HMAP_UNDERLAY = "img/heatmap-underlay2.png"

img = Image.open('heatmap2.png')
img = img.resize((1620, 1080))
img = img.convert("RGBA")

pixdata = img.load()

def remove_border(width, height):
    for y in range(height):
        for x in range(width):
            px = pixdata[x,y]
            if px[2] > px[0]*2 and px[2] > px[1]*2\
                or (px[0] > 220 and px[1] > 220 and px[2] > 220):
                pixdata[x, y] = (255, 255, 255, 0)
            else:
                pixdata[x, y] = (px[0], px[1], px[2], int(255*ALPHA))
    img.save("midlay.png", "PNG")

remove_border(img.size[0], img.size[1])

underlay = Image.open(HMAP_UNDERLAY)
overlay = Image.open('img/border-overlay1.png')
overlay2 = Image.open('img/border-overlay2.png')
midlay = Image.open('midlay.png')

underlay = Image.alpha_composite(underlay, Image.alpha_composite(midlay, Image.alpha_composite(overlay, overlay2)))

os.remove("midlay.png")
os.remove("heatmap2.png")

underlay.save("heatmap.png", "PNG")
print('Finished! Heatmap is saved under heatmap.png.')

end = time.time()
print('That took ' + str(round(end - start, 3)) + ' seconds!')
