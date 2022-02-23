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
    time = 0
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
        
    def toString(self): 
        if self._start == 0 and self._end == 0:
            return "ASYNC"
        day = self.days[self._day]
        startHour = int(self._start)
        startMin = int((self._start * 60) % 60)
        endHour = int(self._end)
        endMin = int((self._end * 60) % 60)
        if startMin < 10: 
            startMin = "0" + str(startMin)
        if endMin < 10: 
            endMin = "0" + str(endMin)
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
    times = [] # array of ClassTimes
    _data = {} # all data that we don't need until to_string is kept here
    _rating = 0

    def __init__(self, data):
        self._data = data
        self._rating = data["rating"]
        self.set_times()
        return

    def check_for_conflict(self, other): #true means there is no conflict
        for i in self.times:
            if i[0]._start == 0 and i[0]._end == 0:
                continue
            for j in other.times:
                if (i[0].has_overlap(j[0])):
                    return False
        return True

    def set_times(self):
        days = ""
        poss_days = "AMTWHFS"
        for i in range(len(self._data["times"])):
            lecture = self._data["times"][i]
            days = lecture["days"]
            if days == "TBA":
                self.times.append((Classtime(), i))
            else:
                days = days.replace("Th","H")
                for day in days:
                    self.times.append([Classtime(time_to_decimal(lecture["start_time"]), time_to_decimal(lecture["end_time"]), poss_days.find(day)), i])
        return

    def toString(self):
        # displays as follows: (with dummy values)
        #######################################################
        # 123456 CS 2A: Object Oriented C++
        # John Doe - 3.5 / 5 on RMP (0 means no data found)
        # times: [Classtime toString]
        #    [Mon, 12:00 -> 15:30] ..... Lecture @ Foothill, Main Campus 5015
        #    [Tue, 13:12 -> 23:59] ..... Lab @ Foothill, Main Campus ONLINE
        #    [ASYNC]
        #######################################################
        returnstring = ""
        data = self._data
        returnstring += str(data["CRN"]) + " " + data["dept"] + " " + data["course"] + ": " + data["title"] + " \n"
        returnstring += data['times'][0]['instructor'][0] + " - " + str(self._rating) + " / 5 on RMP (0 means no data found) \n"
        returnstring += "times: \n"
        for i in self.times:
            s = i[0].toString()
            if s == "ASYNC":
                returnstring +=  "   " + s + " \n"
            else:
                returnstring += "   " + s + " ..... " + data["times"][i[1]]["type"] + " @ " + data["times"][i[1]]["location"] + " \n"
        return returnstring



############################
#TESTING CODE


#course = Class(
#    {"CRN":40091,"raw_course":"ART F001.01Y","dept":"ART","course":"1","section":"01Y","title":"Introduction to Art","units":4.5,"start":"04/04/2022","end":"06/24/2022","times":[{"type":"Lecture","days":"TTh","start_time":"10:00 AM","end_time":"11:50 AM","instructor":["Cynthia Aurora Brannvall"],"location":"Foothill, Main Campus 5015"},{"type":"Lab","days":"TBA","start_time":"TBA","end_time":"TBA","instructor":["Cynthia Aurora Brannvall"],"location":"Foothill, Main Campus ONLINE"}],"status":"open","seats":49,"wait_seats":10,"wait_cap":10, "rating": 3.0}
#    )

#print(course.toString())