# This script is developed by Team 11 CIS 3760
# Parser - to parse the plain text file into json file

import csv
from hashlib import new
import re
import json
import os
import sys

from numpy import true_divide

sys.path.insert(1, os.path.join(sys.path[0], '..'))
import course_util

#### GLOBAL USE REGEX PATTERNS ###

# CIS*3760 or HIST*1000
courseCodePat   = re.compile(r'[A-Z]{3}[A-Z]?\*[0-9]{4}')
isolatedCourseCodePat = re.compile(r'^[A-Z]{3}[A-Z]?\*[0-9]{4}$')

# ECON*3710, ECON*3740
courseCodeListPat = re.compile(r'[A-Z]{3}[A-Z]?\*[0-9]{4}(,[ ]?[A-Z]{3}[A-Z]?\*[0-9]{4})+')

#single OR condition
courseOrCondPat = re.compile(r'\([A-Z]{3}[A-Z]?\*[0-9]{4},? or [A-Z]{3}[A-Z]?\*[0-9]{4}\)')   
courseOrCondNoBrackPat = re.compile(r'[A-Z]{3}[A-Z]?\*[0-9]{4},? or [A-Z]{3}[A-Z]?\*[0-9]{4}')   

#  nested OR/AND 
nestedCondPat = re.compile(r'\[.*?\]')

# 2.00 credits
creditCountIsoaltedPat  = re.compile(r'^([0-9]+.[0-9]+|[0-9]+) credits$')

# 2.00 credits, including 0.50 credits in History at the 1000 level
creditCountdPat  = re.compile(r'([0-9]+.[0-9]+|[0-9]+) credits')

#10.00 credits including 1.50 credits in History at the 3000-level
# creditCountWRequiredPat  = re.compile(r'[0-9]+.[0-9]+ credits including')

#7.50 credits including (1 of FREN*2060, HIST*2100, HIST*2600, POLS*2300)
# courseSelectionGroupPat = re.compile(r'[0-9]+.[0-9]+ credits[,]? including[ ]*?[0-9]+')

courseSelectionGroupSinglePat = re.compile(r'^[0-9]+.[0-9]+ credits[,]? including[ ]*?[0-9]+(.[0-9]+)? credits in \w+( \w+ \w+ \d+ \w+)?')

# splits string by commas not appearing within () or []
stringListSplitterPat = re.compile(r'(?=,\s*(?![^\[\]\[\]]*[\]\]]))(?=,\s*(?![^()\[\]]*[\)\]]))')
    
# floatPat = re.compile(r'[0-9]+.[0-9]+')
# numberPat = re.compile(r'[0-9]+.[0-9]+|[0-9]+')

# select number of courses from list
selectNumCoursePat = re.compile(r'\([0-9]+ of ([A-Z]{3}[A-Z]?\*[0-9]{4}|[0-9]+(.[0-9]+)? credits in \w+)(,[ ]?[A-Z]{3}[A-Z]?\*[0-9]{4})*?\)')

selectNumCourseNoBrackPat = re.compile(r'[0-9]+ of ([A-Z]{3}[A-Z]?\*[0-9]{4}|[0-9]+(.[0-9]+)? credits in \w+)(,[ ]?[A-Z]{3}[A-Z]?\*[0-9]{4})*?')
#### END OF GLOBAL USE REGEX PATTERNS ###



def makeList(element: str) -> list:
    if element:
        return [element]
    else:
        return []

# Redesigned parse function with for more readability and consistency
# reflects changes made to scraper output
def parse(file: str, subjects : list) -> list:
    """
        This function reads the plain text from courseData.txt
        and parse data into json file
    """
    courseList = []
    searchTerms = ['(LEC:', '(LAB:']        # search terms used to parse Lectures and Labs
    with open(file, encoding='utf-8') as csvFile:        # reading file
        csvReader = csv.reader(csvFile, delimiter='\t')
        for course in csvReader:          # looping through courses
            newCourse = {}
            subject = course[0].split('*')[0]           # subject name
            tempList = course[0].split('*')[1].split(u'\xa0')           # splitting courses into individual fields
            tempList[:] = [x for x in tempList if x]

            if len(tempList) == 5:
                courseNum, courseName, semestersOfferedStr, lecLabsStr, creditsStr = tempList
            elif len(tempList) == 4:
                hasLecLabs = False         # checking if lab and lecture exists for particular course
                for item in searchTerms:
                    if len([s for s in tempList if item in s]):
                        hasLecLabs = True
                if not hasLecLabs:                 # if no  lec labs leave it empty
                    courseNum, courseName, semestersOfferedStr, creditsStr = tempList
                    lecLabsStr = ""
                else:
                    raise ValueError('Bad Input - missing field')   # else there exists some bad characters

            description, offering, something, prereqs, coReqs, equates, restrictions, department, location = [course[i]
                                                                                                              for i in
                                                                                                              range(1,
                                                                                                                    10)]
            is_offered_summer = False  # boolean values for course offering(s)
            is_offered_fall = False
            is_offered_winter = False

            # updating boolean values for courses offered in Winter,Fall,Summer
            if semestersOfferedStr.find("Winter") >= 0:
                is_offered_winter = True
            if semestersOfferedStr.find("Fall") >= 0:
                is_offered_fall = True
            if semestersOfferedStr.find("Summer") >= 0:
                is_offered_summer = True

            # converting lectures, labs, credits to float
            try:
                creditsFloat = float(creditsStr.strip("[]"))
            except ValueError:
                creditsFloat = 0

            lecLabArr = lecLabsStr.strip("(LECAB:)").replace("LAB: ", '').replace(",",
                                                                                  '').split()  # creates array of two or 1 nums in string form

            lectures = 0
            labs = 0
            if lecLabsStr:             # parsing lab and lec
                if "LEC" in lecLabsStr and "LAB" in lecLabsStr:
                    try:           # if lab and lec exists parse lab and lec to int
                        lectures = int(lecLabArr[0])
                    except ValueError:
                        lectures = 0
                    try:
                        labs = int(lecLabArr[1])
                    except ValueError:
                        labs = 0
                elif "LEC" in lecLabsStr:
                    try:
                        lectures = int(lecLabArr[0])
                    except ValueError:
                        lectures = 0
                elif "LAB" in lecLabsStr:
                    try:
                        labs = int(lecLabArr[0])
                    except ValueError:
                        labs = 0
            try:
                courseNumInt = int(courseNum)
            except ValueError:
                courseNumInt = 0

            # convert array fields to list, arrays should be empty (len = 0) if they have no data
            offeringList = makeList(offering)
            prereqsList = makeList(prereqs)
            coReqsList = makeList(coReqs)
            equatesList = makeList(equates)
            restrictionsList = makeList(restrictions)
            departmentList = makeList(department)
            locationList = makeList(location)

            # adding fields into dictionary
            newCourse['subject'] = subject
            newCourse['course_num'] = courseNumInt
            newCourse['course_name'] = courseName
            newCourse['is_offered_fall'] = is_offered_fall
            newCourse['is_offered_winter'] = is_offered_winter
            newCourse['is_offered_summer'] = is_offered_summer

            # Changed into two floats as in example.json
            newCourse['lectures'] = lectures
            newCourse['labs'] = labs

            # change to float

            newCourse['credits'] = creditsFloat

            newCourse['description'] = description

            # change all the below to arrays -- except 'unknown' leave as string.
            newCourse['offering'] = offeringList
            newCourse['unknown'] = something
            newCourse['prereqs'] = prereqsList
            newCourse['co_reqs'] = coReqsList
            newCourse['equates'] = equatesList
            newCourse['restrictions'] = restrictionsList
            newCourse['dept'] = departmentList
            newCourse['location'] = locationList
            newCourse['University'] = 'University of Guelph'
            newCourse['subject_name'] = subjects[subject]
            courseList.append(newCourse)
    
    newParser(courseList)
    return courseList


def extractFloat(raw : str) -> float:
    # will return 0 if it is not valid
    temp = raw.strip('\'( \t\r\f')
    num = float(temp[0])
    if num == 0:
        raise ValueError('Bad value recieved by extractFloat')
    return num

def getCourseCodes(raw : str) -> list:
    
    return re.findall(courseCodePat, raw)

def splitSelectNumCourse(raw : str):
    
    multiStep = re.match(r'\[.*?\]', raw)
    if multiStep:
        raise ValueError('Multistep select num')
    else:
        splitStr = re.split(r' of ', raw)
        for i, item in enumerate(splitStr):
            if i == 0:
                splitStr[i] = str(extractFloat(splitStr[i]))
            else:
                splitStr[i] = getCourseCodes(splitStr[i])
    
    return tuple(splitStr)


def splitCourseOrCond(raw : str, pattern, coursePat=None) -> list:
    courseOrList = []
    splitOrCond = re.split(pattern, raw)
    for courseCode in splitOrCond:
        # remove any parenthesis
        courseCode = courseCode.replace('(', '')
        courseCode = courseCode.replace(')', '')
        if coursePat:
            if re.search(pattern, courseCode):
                courseOrList.append(courseCode.strip())
        else:
            courseOrList.append(courseCode.strip())
    return courseOrList

def splitCourseCodeListStr(string : str) -> list:
    '''Splits a comma seperated string into a list of elements delimited by a comma'''

    courseList = re.split(stringListSplitterPat, string)

    for i, course in enumerate(courseList):
        # remove starting ', '
       
        if course.startswith(', '):
            courseList[i] = course[2:]
        courseList[i] = courseList[i].strip('\' \t\r\f')
        
        courseOrCond = re.match(courseOrCondPat, courseList[i])
        if courseOrCond:
            courseList[i] = splitCourseOrCond(courseOrCond.group(), r' or ')

        if re.match(selectNumCoursePat, course):
            courseList[i] = splitSelectNumCourse(courseList[i])
        if not re.match(courseCodePat, course):
            pass
            # raise ValueError('Not a course code seperated list')

    return courseList

def parsePrereq(prereq : str):
    parsedList = []
    
    #NOTE: Priority is important
    if re.match(courseSelectionGroupSinglePat, prereq):
        matched = re.split(r' credits[,]? including ', prereq, maxsplit=2)
        if len(matched) == 2:
            newFormat = {}
            options = parsePrereq(matched[1])
            newFormat['num_options'] = len(options)
            newFormat['is_credits'] = True
            newFormat['num_credits'] = float(matched[0])
            newFormat['options'] = options
            parsedList.append(newFormat)
            #parsedList.append( (float(matched[0]), parsePrereq(matched[1])) )
    # handles the case of having x credits including y
    elif 'including' in prereq:
        #print(prereq)
        creditNum = 0
        options = []
        prereqList = re.split('including', prereq)
        for item in prereqList:
            item = item.strip()
            newList = re.split(stringListSplitterPat, item)
            for elem in newList:
                if re.match(selectNumCoursePat, elem):
                    newItem = splitSelectNumCourse(elem)
                    #X of COURSE COURSE COURSE
                    #print(newItem)
                    newFormat = {}
                    newFormat['num_options'] = int(float(len(newItem[0])))
                    newFormat['is_credits'] = False
                    newFormat['num_credits'] = 0.0
                    newFormat['options'] = newItem[1]
                    options.append(newFormat)
                    #options.append(newItem)

                # case where there is only a list of course codes following the "including"
                elif re.match(courseCodeListPat, elem):
                    #print(elem)
                    #Not sure what this does as with courseData there is 0 cases
                    options = splitCourseCodeListStr(elem)
                # extract credit count required
                elif re.match(creditCountIsoaltedPat, elem):
                    temp = elem.split(' ')
                    #print(elem)
                    creditNum = float(temp[0])
                # split on OR condition
                elif re.match(courseOrCondPat, elem):
                    #print(splitCourseOrCond(elem, r' or '))
                    newFormat = {}
                    newFormat['num_options'] = len(splitCourseOrCond(elem, r' or '))
                    newFormat['is_credits'] = False
                    newFormat['num_credits'] = 0.0
                    newFormat['options'] = splitCourseOrCond(elem, r' or ')
                    options.append(newFormat)
                    #options.append(splitCourseOrCond(elem, r' or '))

                else:
                    remainder = re.split(stringListSplitterPat, elem)
                    #print(remainder)
                    for next in remainder:
                        if next.startswith(', '):
                            next = next[2:]
                        next = next.strip()
                        if len(next) > 0:
                            result = parsePrereq(next)
                            if len(result) > 0:
                                options.append(result)
        #print(creditNum, options)
        newFormat = {}
        newFormat['num_options'] = len(options)
        newFormat['is_credits'] = False
        newFormat['num_credits'] = 0.0
        if creditNum > 0:
            newFormat['is_credits'] = True
            newFormat['num_credits'] = creditNum
        newFormat['options'] = options
        parsedList.append(newFormat)
        #parsedList.append((creditNum, options))
    
    # split by commas outside () or []
    else:
        # case example: 1 of IPS*1500, MATH*1080, MATH*1160, MATH*1200  
        if re.match(selectNumCourseNoBrackPat, prereq):
            parsed = splitSelectNumCourse(prereq)
            #print(parsed)
            newFormat = {}
            newFormat['num_options'] = int(float(parsed[0]))
            newFormat['is_credits'] = False
            newFormat['num_credits'] = 0.0
            newFormat['options'] = parsed[1]
            parsedList.append(newFormat)
            #parsedList.append(splitSelectNumCourse(prereq))
        elif re.match(r'^All Phase [0-9]+ courses', prereq):
            #print(prereq)
            #Not sure what to do with this case
            parsedList.append(prereq)
        else:
            prereqList = re.split(stringListSplitterPat, prereq)
            for item in prereqList:
                # remove starting ', '
                if item.startswith(', '):
                    item = item[2:]
                item = item.strip()
                # if it is a (x of many courses)
                if re.match(nestedCondPat, item):
                    subList = re.split(stringListSplitterPat, item)
                    for temp in subList:
                        if temp.startswith('['):
                            temp = temp[1:]
                        if temp.endswith(']'):
                            temp = temp[:-1]
                        parsedList.append(parsePrereq(temp))
                
                # case: x credits
                elif re.match(creditCountIsoaltedPat, item):
                    #temp = re.search(r'credits', item)
                    #print(item)
                    newFormat = {}
                    newFormat['num_options'] = 0
                    newFormat['is_credits'] = True
                    newFormat['num_credits'] = float(item.split(' ')[0])
                    newFormat['options'] = []
                    parsedList.append(newFormat)
                    #parsedList.append(item)

                elif re.match(selectNumCoursePat, item):
                    # print('matches select num')
                    #print(item)
                    parsed = splitSelectNumCourse(item)
                    #print(parsed)
                    newFormat = {}
                    newFormat['num_options'] = int(float(parsed[0]))
                    newFormat['is_credits'] = False
                    newFormat['num_credits'] = 0.0
                    newFormat['options'] = parsed[1]
                    parsedList.append(newFormat)

                elif re.match(courseOrCondPat, item) or re.match(courseOrCondNoBrackPat, item):
                    #COURSE or COURSE / (COURSE or COURSE)
                    #print(splitCourseOrCond(item, r' or '))
                    newFormat = {}
                    newFormat['num_options'] = len(splitCourseOrCond(item, r' or '))
                    newFormat['is_credits'] = False
                    newFormat['num_credits'] = 0.0
                    newFormat['options'] = splitCourseOrCond(item, r' or ')
                    parsedList.append(newFormat)

                # single course
                elif re.match(isolatedCourseCodePat, item):
                    newFormat = {}
                    newFormat['num_options'] = 1
                    newFormat['is_credits'] = False
                    newFormat['num_credits'] = 0.0
                    newFormat['options'] = [item]
                    parsedList.append(newFormat)
                    #parsedList.append(item)

                # see if a course code exists in the string
                elif re.search(r'minimum of [0-9]+ credits', item):
                    #print(item)
                    tempList = re.split(r'minimum of ', item)
                    for temp in tempList:
                        match = re.search(creditCountdPat, temp)

                        if match:
                            prereqStr = '{} credits'.format(extractFloat(match.group()))
                            #print(match.group())
                            #I have no idea what this is doing. match.group() = "12 credits", prereqStr = "1.0 credits"
                            parsedList.append(prereqStr)
                        else:
                            match = re.search(courseCodePat, temp)
                            if match:
                                #print(match.group())
                                newFormat = {}
                                newFormat['num_options'] = 1
                                newFormat['is_credits'] = False
                                newFormat['num_credits'] = 0.0
                                newFormat['options'] = [match.group()]
                                parsedList.append(newFormat)

                elif re.match(r'[0-9]+.[0-9]+ credits in', item):
                    # print(item)
                    #X.XX credits in SUBJECT
                    newFormat = {}
                    newFormat['num_options'] = 1
                    newFormat['is_credits'] = True
                    newFormat['num_credits'] = float(item.split(' credits in ')[0])
                    newFormat['options'] = [item.split(' credits in ')[1]]
                    parsedList.append(newFormat)
                
                elif re.match(r'[A-Z]{3}[A-Z]?\*[0-9]{4} or \([A-Z]{3}[A-Z]?\*[0-9]{4} and [A-Z]{3}[A-Z]?\*[0-9]{4}\)', item):
                    newItem = re.split(r' or ', item)
                    newItem[1] = newItem[1].replace('(', '')
                    newItem[1] = newItem[1].replace(')', '')
                    #print(newItem)
                    newFormat = {}
                    newFormat['num_options'] = len(newItem)
                    newFormat['is_credits'] = False
                    newFormat['num_credits'] = 0.0
                    newFormat['options'] = newItem
                    #COURSE or (COURSE and COURSE)
                    parsedList.append(newFormat)

  
    return parsedList

def newParser(courseList : list) :

    for courseIndex, course in enumerate(courseList):
        for prereq in course['prereqs']:
            newPrereq = parsePrereq(prereq)
            
            #
            #TODO: convert prereq to new object as per #115
            #
            courseList[courseIndex]['prereqs'] = newPrereq


if __name__ == "__main__":

    if not len(sys.argv) == 4:
        exit('Invalid Arguments')

    fileIn = sys.argv[1]  # plain text file
    subjectFileIn = sys.argv[2]
    fileOut = sys.argv[3]    # output JSON file
    
    if not os.path.exists(fileIn):
        print(fileIn)
        print("Error: File Not Found!")
        exit(0)

    subjects = {}
    with open(subjectFileIn) as json_file:
        subjects = json.load(json_file)

    # parsing plain text into json
    # Serializing json
    courseList = parse(fileIn, subjects)
    
    
    json_object = json.dumps(courseList, indent=2)     # dumping into JSON
    # Writing to sample.json
    with open(fileOut, "w") as outfile:        # writing to JSON file
        outfile.truncate(0)
        outfile.write(json_object)


