#!/usr/bin/python

# formats Dark Sky Meter CSV file into the correct format (i.e. same as globe at night files)
# for the CMU skyglow class, summer 2020
# by Ela Gulsen
# using data sets provided by Dark Sky Meter and Globe At Night

# This needs to be run every time you re-download the Dark Sky Meter data set.

import csv

# Data points to ignore (for reasons including inaccurate measurements)
bad_dates = ['2015-03-28 21:30:27', '2015-03-28 22:47:01', '2017-05-15 21:51:37', '2017-04-26 22:18:43', \
             '2017-05-15 21:55:00']

#Pittsburgh coordinates
LAT_MIN = 40.35
LAT_MAX = 40.55
LONG_MIN = -80.15
LONG_MAX = -79.8

with open('datasets/dsm_database.csv', 'r') as infile, open('datasets/reordered_dsm.csv', 'w') as outfile:
    # output dict needs a list for new column ordering
    fieldnames = ['_date', '_moon', '_deviceangle', '_lat', '_lng', '_typedesc', '_device', '_nelm','_type','_clouds','_user_tag','_sqm']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    # reorder the header first
    writer.writeheader()
    for row in csv.DictReader(infile):
        lat = float(list(row.items())[2][1])
        long = float(list(row.items())[3][1])
        date = list(row.items())[0][1]
        if lat > LAT_MIN and lat < LAT_MAX and long > LONG_MIN and long < LONG_MAX and not date in bad_dates:
            # writes the reordered rows to the new file
            writer.writerow(row)
