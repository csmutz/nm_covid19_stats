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

days = 90
zip_codes = ["87008","87015","87016","87032","87035","87047","87056","87059"]
population_by_zip = {   "87008": 2600,
                        "87015": 13100,
                        "87016": 3700,
                        "87032": 300,
                        "87035": 7300,
                        "87047": 4900,
                        "87056": 1000,
                        "87059": 9600 }

now = time.time()
basedir = "/var/log/covid/"
outdir = "/var/www/html/covid19/"
total_population = 42500
rows = []
rows_100k = []
delta_rows = []
delta_rows_100k = []
last_row = None
count_14_day = 0
count_7_day = 0
count_10_day = 0

for i in range(days):
    date_downloaded = datetime.datetime.utcfromtimestamp(now-86400*(days-i-1)).strftime("%Y-%m-%d")
    date_actual =  datetime.datetime.utcfromtimestamp(now-86400*(days-i)).strftime("%Y-%m-%d")
    p = basedir + date_downloaded + ".json"
    row = {}
    delta_row = {}
    row_100k = {}
    delta_row_100k = {}
    delta_row['date'] = date_actual
    delta_row_100k['date'] = date_actual
    if os.path.isfile(p):
        with open(p) as f:
            data = json.load(f)
        if "data" in data:
            for r in data['data']:
                if r["zip"] in zip_codes:
                    row[r["zip"]] = r["cases"]
                    row_100k[r["zip"]] = round(int(r["cases"])*100000/population_by_zip[r["zip"]])

    if row:
        if last_row:
            for z in zip_codes:
                delta_row[z] = row[z] - last_row[z]
                delta_row_100k[z] = round((row[z] - last_row[z])*100000/population_by_zip[z])
                if i >= (days - 14):
                    count_14_day = count_14_day + delta_row[z]
                if i >= (days - 10):
                    count_10_day = count_10_day + delta_row[z]
                if i >= (days - 7):
                    count_7_day = count_7_day + delta_row[z]
        else:
            for z in zip_codes:
                delta_row[z] = 0
        row['date'] = date_actual
        row_100k['date'] = date_actual
        rows.append(row)
        last_row = row
        rows_100k.append(row_100k)
        delta_rows.append(delta_row)
        delta_rows_100k.append(delta_row_100k)

        
with open(outdir + "covid.csv", 'w') as outfile:
    fieldnames = ['date']
    fieldnames.extend(zip_codes)
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)

    writer.writeheader()
    for r in rows:
        writer.writerow(r)

with open(outdir + "covid_100k.csv", 'w') as outfile:
    fieldnames = ['date']
    fieldnames.extend(zip_codes)
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)

    writer.writeheader()
    for r in rows_100k:
        writer.writerow(r)


with open(outdir + "covid_delta.csv", 'w') as outfile:
    fieldnames = ['date']
    fieldnames.extend(zip_codes)
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)

    writer.writeheader()
    for r in delta_rows:
        writer.writerow(r)

with open(outdir + "covid_delta_100k.csv", 'w') as outfile:
    fieldnames = ['date']
    fieldnames.extend(zip_codes)
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)

    writer.writeheader()
    for r in delta_rows_100k:
        writer.writerow(r)



#14 day new cases per 100K (not daily average)
with open(outdir + "14_day.json", 'w') as outfile:
    json.dump(int(count_14_day * 100000.0 / total_population), outfile)

#10 day new cases per capita
with open(outdir + "10_day.json", 'w') as outfile:
        json.dump((count_10_day / total_population), outfile)

#7 day daily average new cases per 1M
with open(outdir + "7_day.json", 'w') as outfile:
        json.dump(int(count_7_day * 1000000.0 / total_population / 7), outfile)


