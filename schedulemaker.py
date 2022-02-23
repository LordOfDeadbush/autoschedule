'''
Alright. This is the SAUCE. the place where all the shit happens. The program you actually use to make the schedule. Finally. 
The functions in this file will:
 - make all possible schedules from an input (via coursefetch & courses)
 - validate the schedules, thinning the herd from the last item in this list
 - analyze the "worth" of each schedule based on weight and RMP score
 - get the best schedule

see https://en.m.wikipedia.org/wiki/Knapsack_problem for how some of this works


'''

from coursefetch import *
from courses import *


# will put clientside code here