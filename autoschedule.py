import requests;

def format_input(input): # input should be formatted as "MATH 1A, PSYCH 2B..."
    classes = input.split(", ") # seperates multiple course names
    classes = [i.split(" ") for i in classes] # seperates MATH from 1A
    return classes

def get_RMP(teacher):
    #will break if multiple teachers have the same name but fuck you anyways
    teacher = teacher.replace(" ", "%20")
    r = requests.get("https://www.ratemyprofessors.com/search/teachers?query=" + teacher + "&sid=U2Nob29sLTE1ODE=")
    s = r.text
    index = s.find("avgRating")
    if (index == -1): # delete middle name, try again
        return 0
    if (s[index+11] == '0'): 
        return 0
    rating = float(s[index+11:index+14]) # if this doesnt work return 0
    return rating

def get_course_info(crn): # gets all course info and returns in dictionary
    r = requests.get("https://opencourse.dev/fh/classes/"+str(crn))
    info = r.json() # look at the opencourse API for more info (or just go to the link and look at the formatting)
    rating = get_RMP(info['times'][0]['instructor'][0]) # TODO: fix this its not working aaaaaaaaaaaa
    info.update({"Rating": rating})
    return info # return a dictionary with course data

def get_courses(name): #gets all crns and calls course info for each one
    # name should be a list with [0] being the department and [1] being the course (e.g. ["MATH", "1A"])
    r = requests.get("https://opencourse.dev/fh/depts/" + name[0].upper() + "/courses/" + name[1].upper())
    data = r.json()
    coursedata = [get_course_info(i) for i in data["classes"]]
    return coursedata

print(get_courses(["MATH", "2A"]))



# maybe check for middle name????????????