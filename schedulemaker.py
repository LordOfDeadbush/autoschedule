'''
the following is a python version of https://github.com/ogvenocity/Class-Schedule, specifically main.cpp

would branch but tbh im too lazy

'''

##########################################
# objectives:
# 1) make a seperate data point for every meeting 
# 2) make sure none conflict each other (modified version of all_possible_schedules)
# 3) get optimal schedules (do the same as in main)
# 4) return the most optional schedule
#
#
# side note: doing this in 24h time may be beneficial because we might add a gui later

        
from ast import Constant


class Class:
    class Classtime:
        # 0 to 0 will be an async class
        _day = -1 # -1 is async, 0-6 are days of week
        _start = 0 # represented as number between 0 and 24 (exclusive) with a decimal
        _end = 0
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        def __init__(self, start = 0, end = 0, day = 0):
            self._start = float(start)
            self._end = float(end)
            self._day = int(day)
            
        def toString(self):
            if self.start == 0 and self.end == 0:
                return "ASYNCHRONOUS"
            day = self.days[self._day]
            startHour = int(self.start)
            startMin = (self.start * 60) % 60
            endHour = int(self.end)
            endMin = (self.end * 60) % 60
            return day + " , " + str(startHour) + ":" + str(startMin) + " -> " + str(endHour) + ":" + str(endMin)

        def has_overlap(self, other):
            if self._day != other.day:
                return False
            if self._start == 0 and self._end == 0:
                return False
            if other._start == 0 and other._end == 0:
                return False   
            if self._start > other._end:
                return False
            if other._start > self._end:
                return False
            return True

    times = [Classtime(0, 0)] # array of ClassTimes
    data = {} # all data that we don't need until to_string is kept here

    def check_for_conflict(self, other): #true means there is no conflict
        for i in self.times:
            if i._start == 0 and i._end == 0:
                continue
            for j in other.times:
                if (i.has_overlap(j)):
                    return False
        return True
    
