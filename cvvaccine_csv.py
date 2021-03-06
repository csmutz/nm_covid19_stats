#!/usr/bin/env python3
'''
install to /usr/local/bin
make sure directories are right
'''

import json
import csv
import datetime
import time
import os

days = 90
now = time.time()
basedir = "/var/log/covid/"
outdir = "/var/www/html/covid19/"
rows = []
columns = ["lastDate", "percentFullyVaccinated", "percentPartiallyVaccinated",  "percentRegistered"]
new_columns = ["date", "Fully Vaccinated", "Partially Vaccinated", "Registered"]
column_lookup = dict(zip(columns,new_columns))
county = "Torrance"

last_date = None
for i in range(days):
    date_downloaded = datetime.datetime.utcfromtimestamp(now-86400*(days-i-1)).strftime("%Y-%m-%d")
    date_actual =  datetime.datetime.utcfromtimestamp(now-86400*(days-i)).strftime("%Y-%m-%d")
    p = basedir + "vaccine-" + date_downloaded + ".json"
    row = {}
    if os.path.isfile(p):
        with open(p) as f:
            data = json.load(f)
        if "data" in data:
            for r in data['data']:
                if r["county"] == county:
                    for k in r:
                        #print(r)
                        if k in columns:
                            row[column_lookup[k]] = r[k]

        row['date'] = date_actual
        rows.append(row)
        

        
with open(outdir + "vaccine.csv", 'w') as outfile:
    fieldnames = new_columns
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)

    writer.writeheader()
    for r in rows:
        writer.writerow(r)
