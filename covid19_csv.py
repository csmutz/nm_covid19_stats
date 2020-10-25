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
zip_codes = ["87008","87015","87016","87032","87035","87047","87056","87059"]
now = time.time()
basedir = "/var/log/covid/"
outdir = "/var/www/html/covid19/"
total_population = 42500
rows = []
delta_rows = []
last_row = None
count_14_day = 0
count_7_day = 0

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
                if i >= (days - 14 - 1):
                    count_14_day = count_14_day + delta_row[z]
                if i >= (days - 7 - 1):
                    count_7_day = count_7_day + delta_row[z]
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

#14 day new cases per 100K (not daily average)
with open(outdir + "14_day.json", 'w') as outfile:
    json.dump(int(count_14_day * 100000.0 / total_population), outfile)

#7 day daily average new cases per 1M
with open(outdir + "7_day.json", 'w') as outfile:
        json.dump(int(count_7_day * 1000000.0 / total_population / 7), outfile)


