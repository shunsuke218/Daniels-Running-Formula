#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv, sqlite3

#con = sqlite3.connect(":memory:")
con = sqlite3.connect("jackdaniel.db")
cur = con.cursor()
cur.execute("CREATE TABLE t (VDOT,\"1500m\",Mile,\"3000m\",\"2-mile\",\"5K\",\"10K\",\"15K\",\"Half Marathon\",\"Marathon\",\"Easy/Long\",\"Easy/Long(mph)\",\"Marathon Pace\",\"Marathon Pace(mph)\",\"Threshold Pace\",\"Threshold Pace(mph)\",\"Interval Pace\",\"Interval Pace(mph)\",\"Repetition Pace\",\"Repetition Pace(mph)\");") # use your column names here

with open('jackdaniel_vdot.txt','rb') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default

    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['VDOT'], i['1500m'], i['Mile'], i['3000m'], i['2-mile'], i['5K'], i['10K'], i['15K'], i['Half Marathon'], i['Marathon'], i['Easy/Long'], i['Easy/Long(mph)'], i['Marathon Pace'], i['Marathon Pace(mph)'], i['Threshold Pace'], i['Threshold Pace(mph)'], i['Interval Pace'], i['Interval Pace(mph)'], i['Repetition Pace'], i['Repetition Pace(mph)']) for i in dr]

cur.executemany("INSERT INTO t  (\"VDOT\", \"1500m\", \"Mile\", \"3000m\", \"2-mile\", \"5K\", \"10K\", \"15K\", \"Half Marathon\", \"Marathon\", \"Easy/Long\", \"Easy/Long(mph)\", \"Marathon Pace\", \"Marathon Pace(mph)\", \"Threshold Pace\", \"Threshold Pace(mph)\", \"Interval Pace\", \"Interval Pace(mph)\", \"Repetition Pace\", \"Repetition Pace(mph)\") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
con.commit()
con.close()
