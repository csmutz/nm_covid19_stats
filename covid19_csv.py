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

'''config'''

days = 60
zip_codes = ["87001","87002"]
now = time.time()
basedir = "/var/log/covid/"
outdir = "/var/www/html/covid19/"

rows = []
delta_rows = []
last_row = None

for i in range(days):
    date_downloaded = datetime.datetime.utcfromtimestamp(now-86400*(days-i-1)).strftime("%Y-%m-%d")
    date_actual =  datetime.datetime.utcfromtimestamp(now-86400*(days-i)).strftime("%Y-%m-%d")
    p = basedir + date_downloaded + ".json"
    row = {}
    delta_row = {}
    delta_row['date'] = date_actual
    if os.path.isfile(p):
        with open(p) as f:
            data = json.load(f)
        if "data" in data:
            for r in data['data']:
                if r["zip"] in zip_codes:
                    row[r["zip"]] = r["cases"]
    if row:
        if last_row:
            for z in zip_codes:
                delta_row[z] = row[z] - last_row[z]
        else:
            for z in zip_codes:
                delta_row[z] = 0
        row['date'] = date_actual
        rows.append(row)
        last_row = row
        delta_rows.append(delta_row)
        
with open(outdir + "covid.csv", 'w') as outfile:
    fieldnames = ['date']
    fieldnames.extend(zip_codes)
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)

    writer.writeheader()
    for r in rows:
        writer.writerow(r)


with open(outdir + "covid_delta.csv", 'w') as outfile:
    fieldnames = ['date']
    fieldnames.extend(zip_codes)
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)

    writer.writeheader()
    for r in delta_rows:
        writer.writerow(r)




