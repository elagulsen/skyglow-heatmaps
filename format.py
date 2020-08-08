#!/usr/bin/python

# formats Dark Sky Meter CSV file into the correct format (i.e. same as globe at night files)
# for the CMU skyglow class, summer 2020
# by Ela Gulsen
# using data sets provided by Dark Sky Meter and Globe At Night

# This needs to be run every time you re-download the Dark Sky Meter data set.
# It also removes excess entries from the Globe at Night data sets.

import csv

# Data points to ignore (for reasons including inaccurate measurements)
bad_dates = ['2015-03-28 21:30:27', '2015-03-28 22:47:01', '2017-05-15 21:51:37', '2017-04-26 22:18:43', \
             '2017-05-15 21:55:00']

#Pittsburgh coordinates
LAT_MIN = 40.35
LAT_MAX = 40.55
LONG_MIN = -80.15
LONG_MAX = -79.8

read_ds = input('Name of data set to read (from datasets folder): ')
write_ds = input('Name of data set to write (from datasets folder): ')

with open('datasets/' + read_ds, 'r') as infile, open('datasets/' + write_ds, 'w') as outfile:
    # output dict needs a list for new column ordering
    if 'GaN' in read_ds:
        fieldnames = ['ID','ObsType','ObsID','Latitude','Longitude','Elevation(m)','LocalDate','LocalTime','UTDate','UTTime','LimitingMag','SQMReading','Country','SQMSerial','CloudCover','Constellation','LocationComment','SkyComment']
    else:
        fieldnames = ['_date', '_moon', '_deviceangle', '_lat', '_lng', '_typedesc', '_device', '_nelm','_type','_clouds','_user_tag','_sqm']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    # reorder the header first
    writer.writeheader()
    for row in csv.DictReader(infile):
        lat,long,date = 0,0,0
        r_list = list(row.items())
        for item in r_list:
            #print(item)
            if '_lat' in item or 'Latitude' in item:
                lat = float(item[1])
            elif '_lng' in item or 'Longitude' in item:
                long = float(item[1])
            elif '_date' in item or 'SQMReading' in item:
                date = item[1]
        if lat > LAT_MIN and lat < LAT_MAX and long > LONG_MIN and long < LONG_MAX and not date in bad_dates:
            # writes the reordered rows to the new file
            writer.writerow(row)
