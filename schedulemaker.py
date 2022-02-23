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




def time_to_decimal(s):
    if not ("AM" in s and s[0:1] == "12"):
        time += int(s[0:1])
    time += float(s[3:4]) / 60
    if "PM" in s:
        time += 12
    return time


class Classtime:
    # 0 to 0 will be an async class
    _day = -1 # 0 is async, 1-7 are days of week (sunday can only be accessed manually as of right now)
    _start = 0 # represented as number between 0 and 24 (exclusive) with a decimal
    _end = 0
    days = ["Async", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    def __init__(self, start = 0, end = 0, day = 0):
        self._start = float(start)
        self._end = float(end)
        self._day = int(day)
        
    def toString(self): # TODO: make it do 00 if the hour is on the hour
        if self._start == 0 and self._end == 0:
            return "ASYNC"
        day = self.days[self._day]
        startHour = int(self._start)
        startMin = int((self._start * 60) % 60)
        endHour = int(self._end)
        endMin = int((self._end * 60) % 60)
        if startMin == 0:
            startMin = "00"
        if endMin == 0:
            endMin = "00"
        return day + ", " + str(startHour) + ":" + str(startMin) + " -> " + str(endHour) + ":" + str(endMin)

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


class Class:
    times = [Classtime(0, 0)] # array of ClassTimes
    _data = {} # all data that we don't need until to_string is kept here

    def __init__(self, data):
        self._data = data
        self.set_times()
        return

    def check_for_conflict(self, other): #true means there is no conflict
        for i in self.times:
            if i._start == 0 and i._end == 0:
                continue
            for j in other.times:
                if (i.has_overlap(j)):
                    return False
        return True

    def set_times(self):
        days = ""
        poss_days = "AMTWHFS"
        for lecture in self._data["times"]:
            days = lecture["days"]
            if days == "TBA":
                self.times = [self.Classtime()]
                continue
            days = days.replace("Th","H")
            for day in days:
                self.times.append(Classtime(time_to_decimal(lecture["start_time"]), time_to_decimal(lecture["end_time"]), poss_days.find(day)))
        
        return


