'''
Alright. This is the SAUCE. the place where all the shit happens. The program you actually use to make the schedule. Finally. 
The functions in this file will:
 - make all possible schedules from an input (via coursefetch & courses)
 - validate the schedules, thinning the herd from the last item in this list
 - analyze the "worth" of each schedule based on weight and RMP score
 - get the best schedule

see https://en.m.wikipedia.org/wiki/Knapsack_problem for how some of this works


'''

from re import T
import sched
from coursefetch import *
from courses import *

class Schedule:

    def __init__(self, classes):
        self._classes = classes
        self._possible = self.is_possible()
        self._score = self.find_score()
        return

    def is_possible(self):
        for i in self._classes:
            for j in self._classes:
                if i._data["CRN"] == j._data["CRN"]:
                    continue
                if not i.check_for_conflict(j):
                    return False
        return True
    
    def find_score(self):
        score = 0
        denominator = 0
        for i in self._classes:
            score += i._rating
            #print(i.toString())
            denominator += float(i._data["units"])
        if denominator == 0:
            return 0
        return float(score) / float(denominator)

    def toString(self):
        s = "Schedule: \n"
        for i in self._classes:
            s += i.toString()
            s += "\n\n"
        return s
        

def get_courses_formatted(s):
    l = get_courses_from_input(s)
    courses = []
    for i in range(len(l)):
        for j in range(len(l[i])):
            # courses.append(Class(j))
            l[i][j] = Class(l[i][j])

    return l

def make_all_possible_schedules(s):
    courses = get_courses_formatted(s)
    combinations = []
    combinations2 = []
    schedules = []
    for i in courses:
        if combinations == []:
            combinations = [[j] for j in i]
            continue
        for j in combinations:
            for k in i:
                temp = j[:]
                temp.append(k)
                combinations2.append(temp)
        combinations = combinations2[:]
        combinations2.clear()
    schedules = [Schedule(i) for i in combinations]
    return schedules
    
def get_optimal_schedule(s):
    schedules = make_all_possible_schedules(s)
    best = schedules[0]
    for i in schedules: #all schedules
        if not i._possible:
            continue
        if i._score > best._score:
            i = best
            continue
    return best

###########################################
# TEST CODE

# print("\n".join([i.toString() for i in get_courses_formatted("CS 2A,CS 2B")])) # doesnt work anymore because of how this is indiced
# print(get_courses_formatted("CS 2A,CS 2B"))
#courselist = [
#    {'CRN': 40165, 'raw_course': 'C S F002A01Z', 'dept': 'CS', 'course': '2A', 'section': '01Z', 'title': 'Object-Oriented Programming Methodologies in C++', 'units': 4.5, 'start': '04/04/2022', 'end': '06/24/2022', 'times': [{'type': 'Lecture', 'days': 'TTh', 'start_time': '08:00 AM', 'end_time': '09:50 AM', 'instructor': ['Anand Venkataraman'], 'location': 'Foothill, Main Campus ONLINE'}, {'type': 'Lab', 'days': 'TBA', 'start_time': 'TBA', 'end_time': 'TBA', 'instructor': ['Anand Venkataraman'], 'location': 'Foothill, Main Campus ONLINE'}], 'status': 'open', 'seats': 40, 'wait_seats': 10, 'wait_cap': 10, 'rating': 3.6},  
#    {'CRN': 40166, 'raw_course': 'C S F002A03W', 'dept': 'CS', 'course': '2A', 'section': '03W', 'title': 'Object-Oriented Programming Methodologies in C++', 'units': 4.5, 'start': '04/04/2022', 'end': '06/24/2022', 'times': [{'type': 'Lecture', 'days': 'TBA', 'start_time': 'TBA', 'end_time': 'TBA', 'instructor': ['David Lee Harden'], 'location': 'Foothill, Main Campus ONLINE'}, {'type': 'Lab', 'days': 'TBA', 'start_time': 'TBA', 'end_time': 'TBA', 'instructor': ['David Lee Harden'], 'location': 'Foothill, Main Campus ONLINE'}], 'status': 'open', 'seats': 38, 'wait_seats': 10, 'wait_cap': 10, 'rating': 2.7},
#]

#sched = Schedule([Class(i) for i in courselist])
#print(sched.toString())

# print("\n".join([i.toString() for i in make_all_possible_schedules("MATH 1A,CS 2A")]))

# print(get_optimal_schedule("MATH 1A,CS 2A").toString())