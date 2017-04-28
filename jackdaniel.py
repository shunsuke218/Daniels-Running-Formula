#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import codecs
import json 
import re

from datetime import time
from datetime import timedelta
import sqlite3

class Pace():
    def __init__(self):
        try:
            vdot = float(input("Please input your VDOT: "))
            vdot = float(int( 5 * round(float(vdot * 10) / 5))) / 10
            if vdot < 30 or vdot > 70 :
                raise Exception
        except:
            print "error!!"
            exit()

        self.vdot = vdot
        con = sqlite3.connect("jackdaniel.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM t WHERE VDOT=?", (str(vdot),))
        result = cur.fetchone()
        km_time = lambda t : \
                  time(0,*( int(num) for num in divmod( (t.minute * 60.0 + t.second) / 1.60934, 60 )))
        
        self.easy_mi = time(*tuple(int(elem) for elem in result[10].split(':')))
        self.easy_mph = float(result[11])
        self.easy_km = km_time(self.easy_mi)
        self.easy_kph = self.easy_mph * 1.60934
        
        self.marathon_mi = time(*tuple(int(elem) for elem in result[12].split(':')))
        self.marathon_mph = float(result[13])
        self.marathon_km = km_time(self.marathon_mi)
        self.marathon_kph = self.marathon_mph * 1.60934
        
        self.threshold_mi = time(*tuple(int(elem) for elem in result[14].split(':')))
        self.threshold_mph = float(result[15])
        self.threshold_km = km_time(self.threshold_mi)
        self.threshold_kph = self.threshold_mph * 1.60934
        
        self.interval_mi = time(*tuple(int(elem) for elem in result[16].split(':')))
        self.interval_mph = float(result[17])
        self.interval_km = km_time(self.interval_mi)
        self.interval_kph = self.interval_mph * 1.60934
        
        self.repetition_mi = time(*tuple(int(elem) for elem in result[18].split(':')))
        self.repetition_mph = float(result[19])
        self.repetition_km = km_time(self.repetition_mi)
        self.repetition_kph = self.repetition_mph * 1.60934
        
        self.reference = \
                         {
                          "E": (self.easy_mi, self.easy_km, self.easy_mph, self.easy_kph), \
                          "M": (self.marathon_mi, self.marathon_km, self.marathon_mph, self.marathon_kph), \
                          "T": (self.threshold_mi, self.threshold_km, self.threshold_mph, self.threshold_kph), \
                          "I": (self.interval_mi, self.interval_km, self.interval_mph, self.interval_kph), \
                          "H": (self.interval_mi, self.interval_km, self.interval_mph, self.interval_kph), \
                          "R": (self.repetition_mi, self.repetition_km, self.repetition_mph, self.repetition_kph), \
                         }
        
pace = Pace()
    
        
class Rap():
    def __init__(self, *args):
        global pace
        self.time = self.distance_mi = None
        if args[0].isdigit():
            self.time = args[0]
            self.pace = args[1]
        else:
            self.pace = args[0]
            if len(args) > 1 and float(args[1]) < 100:
                self.distance_mi = args[1]
            elif len(args) > 1:
                self.distance_mi = round(float(args[1]) * 0.000621371, 3)
            else:
                self.distance_mi = None
        self.rest = args[2] if len(args) > 2 else None

        self.pacetime_mi = pace.reference[self.pace][0]
        self.pacetime_km = pace.reference[self.pace][1]

        if self.distance_mi is None:
            self.distance_mi = round(float(self.time) / 60 * pace.reference[self.pace][2], 3)
            self.distance_km = round(float(self.time) / 60 * pace.reference[self.pace][3], 3)

        if self.time is None:
            self.time = float(self.distance_mi) * (self.pacetime_mi.minute * 60 + self.pacetime_mi.second)/60
            self.time = int(self.time) if self.time - int(self.time) == 0.0 else int(self.time) + 1
        self.calculate_km()
        
    def __str__(self):
        if all([self.pacetime_mi, self.pace, self.distance_mi, self.distance_km, self.rest, self.time]):
            output = "%s/mi (%s/km) (%s) x %s mi (%s km) (%s min) \n%s min rest" % \
                     (self.pacetime_mi.strftime("%M:%S"), self.pacetime_km.strftime("%M:%S"), self.pace, self.distance_mi, self.distance_km, self.time, self.rest)
        elif all([self.pacetime_mi, self.pace, self.distance_mi, self.distance_km, self.rest]):
            output = "%s/mi (%s/km) (%s) x %s mi (%s km) + %s min rest" % \
                     (self.pacetime_mi.strftime("%M:%S"), self.pacetime_km.strftime("%M:%S"), self.pace, self.distance_mi, self.distance_km, self.rest)
        elif all([self.pacetime_mi, self.pace, self.distance_mi, self.rest]):
            output = "%s/mi (%s/km) (%s) x %s mi + %s min rest" % \
                     (self.pacetime_mi.strftime("%M:%S"), self.pacetime_km.strftime("%M:%S"), self.pace, self.distance_mi, self.rest)
        elif all([self.pacetime_mi, self.pace, self.time, self.rest]):
            output = "%s/mi (%s/km) (%s) x %s min + %s min rest" % \
                     (self.pacetime_mi.strftime("%M:%S"), self.pacetime_km.strftime("%M:%S"), self.pace, self.time, self.rest)
        elif all([self.pace, self.distance_mi, self.distance_km, self.rest]):
            output = "%s x %s mi (%s km) + %s min rest" % \
                     (self.pace, self.distance_mi, self.distance_km, self.rest)
        elif all([self.pace, self.distance_mi, self.rest]):
            output = "%s x %s mi + %s min rest" % \
                     (self.pace, self.distance_mi, self.rest)
        elif all([self.pace, self.time, self.rest]):
            output = "%s x %s min + %s min rest" % \
                     (self.pace, self.time, self.rest)
        elif all([self.pacetime_mi, self.pace, self.distance_mi, self.distance_km, self.time]):
            output = "%s/mi (%s/km) (%s) x %s mi (%s km) (%s min)" % \
                     (self.pacetime_mi.strftime("%M:%S"), self.pacetime_km.strftime("%M:%S"), self.pace, self.distance_mi, self.distance_km, self.time)
        elif all([self.pacetime_mi, self.pace, self.distance_mi, self.distance_km]):
            output = "%s/mi (%s/km) (%s) x %s mi (%s km)" % \
                     (self.pacetime_mi.strftime("%M:%S"), self.pacetime_km.strftime("%M:%S"), self.pace, self.distance_mi, self.distance_km)
        elif all([self.pacetime_mi, self.pace, self.distance_mi]):
            output = "%s/mi (%s/km) (%s) x %s mi" % \
                     (self.pacetime_mi.strftime("%M:%S"), self.pacetime_km.strftime("%M:%S"), self.pace, self.distance_mi)
        elif all([self.pacetime_mi, self.pace, self.time]):
            output = "%s/mi (%s/km) (%s) x %s min" % \
                     (self.pacetime_mi.strftime("%M:%S"), self.pacetime_km.strftime("%M:%S"), self.pace, self.time)
        elif all([self.pace, self.distance_mi, self.distance_km]):
            output = "%s x %s mi (%s km)" % \
                     (self.pace, self.distance_mi, self.distance_km)
        elif all([self.pace, self.distance_mi]):
            output = "%s x %s mi" % \
                     (self.pace, self.distance_mi)
        elif all([self.pace, self.time]):
            output = "%s x %s min" % \
                     (self.pace, self.time)
        elif all([self.pacetime_mi]):
            output = "%s/mi (%s/km) (%s)" % \
                     (self.pacetime_mi.strftime("%M:%S"), self.pacetime_km.strftime("%M:%S"), self.pace)
        else:
            output = "%s" % (self.pace)
        return output

    def calculate_km(self):
        self.distance_km = round(float(self.distance_mi) * 1.60934, 3) \
                           if self.distance_mi is not None else None
    #def add_pacing(self, pacing):
        
        
class Session():
    def __init__(self, week, percent):
        self.week = week
        self.percent = float(percent) * 100
        #self.session = session
        self.rap = []

    def __str__(self):
        self.total_dist()
        return "Week: " + str(self.week) + '\n' \
            + "%: " + str(self.percent) + "%\n" \
            + "distance: " + str(self.total_mi) + " mi (" + str(self.total_km) + "km)\n" \
            + '\n'.join([(str(self.dist_list(index)) + "km").rjust(8, ' ') + "  " +\
                         str(rap) for index, rap in enumerate(self.rap)]) \
            + "\n---------------"
            #+ "Q: Q" + str(self.session) + '\n' \

    def add_rap(self, rap):
        self.rap.append(rap)

    def total_dist(self):
        total_mi = 0.0; total_km = 0.0
        for rap in self.rap:
            total_mi += float(rap.distance_mi) if rap.distance_mi is not None else 0
            total_km += float(rap.distance_km) if rap.distance_km is not None else 0
        self.total_mi = total_mi
        self.total_km = total_km

    def dist_list(self, num):
        total = 0.0
        for rap in self.rap[:num]:
            total += rap.distance_km if rap.distance_km is not None else 0
        return total
        
def main():
    with open("jackdaniel2.txt",'r') as original:
        for line in original.read().splitlines():
            line = line.split('\t')
            session = Session(line[0],line[1])
            for rap in line[2].split(','):
                session.add_rap(Rap(*rap.split(' ')))
            print session

    
if __name__ == '__main__':
    main()
