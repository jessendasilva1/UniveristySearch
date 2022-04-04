# This script is developed by Team 11 CIS 3760
# Parser - to parse the plain text file into json file

import sys
import re
import json
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))
import course_util

uOCourseCodeIsolatedPat = re.compile(r'^\w{3}[ ]?\d{4}$')
uOCourseCodePat = re.compile(r'\w{3}[ ]?\d{4}')
uOOneOfCondPat = re.compile(r'One of .+', re.IGNORECASE)
uOAntiReqPat = re.compile(r'The courses? (\w{3}\w?[ ]?\d{4},?[ ]?)+', re.IGNORECASE)

uOCarlAltPat = re.compile(r'\w{3}[ ]?\d{4} \(\w{4}[ ]?\d{4}(?:(?: or | ou | and | et )\w{4}[ ]?\d{4})+\)')

uOOrListPat = re.compile(r'\(\w{3,4}[ ]?\d{4}(?:(?: or | ou )\w{3,4}[ ]?\d{4})\)')
uOOrListNoBracketPat = re.compile(r'\w{3}[ ]?\d{4}(?:(?: or | ou )\w{3}[ ]?\d{4})+')

uOOrCondNoBracketIsoPat = re.compile(r'^\w{3,4}[ ]?\d{4}(?:(?: or | ou )\w{3}[ ]?\d{3,4})[.]?$')

uOEnglishCoursePat = re.compile(r'\w{3}[ ]?\d[1234]\d{2}')

uOAndListIsoPat = re.compile(r'^\w{3,4}[ ]?\d{4}(?:(?: and | et |, )\w{3,4}[ ]?\d{4})+$')
uOAndCondIsoPat = re.compile(r'^\w{3,4}[ ]?\d{4}(?:(?: and | et |, )\w{3,4}[ ]?\d{4})$')
uOAndCondPat = re.compile(r'\w{3,4}[ ]?\d{4}(?:(?: and | et |, )\w{3,4}[ ]?\d{4})')

uOAndOptionPat = re.compile(r'^\(?\w{3}[ ]?\d{4}(?:(?: and | et |, )\w{3}[ ]?\d{4})\)?$')
uOAndListPat = re.compile(r'^\(?\w{3}[ ]?\d{4}(?:(?: and | et |, )\w{3}[ ]?\d{4})+\)?$')

uONotCombineFRPat = re.compile(r'^Les cours \w{3}[ ]?\d{3,4}(?:(?: or | ou | and | et |, )\w{3,4}[ ]?\d{4})+ ne peuvent être combinés pour l\'obtention de crédits[.;]?', re.IGNORECASE)
uONotCombineENGPat = re.compile(r'^\w{3}[ ]?\d{3,4}(?:(?: or | ou | and | et |, )\w{3,4}[ ]?\d{4})+ cannot be combined for units[.;]?', re.IGNORECASE)

uOSingleThirdPartyOptPat = re.compile(r'^\w{3}[ ]?\d{4} \(\w{4}[ ]?\d{4}\)$')
uOThirdPartyCourseListPat = re.compile(r'\(?\w{4}[ ]?\d{4}(?:(?: or | ou | and | et |, )\w{4}[ ]?\d{4})\)?')

uOCreditPrereqENGPat = re.compile(r'^\d+ university units[.;]?$')
uOCreditPrereqFRPat = re.compile(r'^\d+ crédits universitaires[.;]?$')

# splits string by commas not appearing within () or []
stringListSplitterPat = re.compile(r'(?=,\s*(?![^\[\]\[\]]*[\]\]]))(?=,\s*(?![^()\[\]]*[\)\]]))')

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

def splitOnPeriod(string : str):
    splitList = re.split(r'\.', string)
    return splitList

def splitOnComma(string : str):
    newList = re.split(stringListSplitterPat, string)
    for i, item in enumerate(newList):
        if item.startswith(', '):
                newList[i] = item[2:]
        if item == '':
            newList.pop(i)
    
    return newList


def normalizeUnicodeString(string : str) -> str:
    string = string.replace(u'\xa0', ' ')
    # item = unicodedata.normalize('NFKC', item)
    string = string.strip()
               
    string = string.replace('Préalable : ', '')
    string = string.replace('Préalables : ', '')
    string = string.replace('Prerequisite: ', '')
    string = string.replace('Prerequisites: ', '')

    return string


def parseUOttawaPrereqElm(prereqString : str):
    prereqList = []
    splitList = splitOnPeriod(prereqString)
    # print('splitList:', splitList)
    for item in splitList:
        item = normalizeUnicodeString(item)
        if item == ''   or re.search(uOAntiReqPat, item) or re.match(uONotCombineENGPat, item) \
                        or re.match(uONotCombineFRPat, item):
            continue
        # Case where or condition list in the form 'One of Calculus and Vectors (MCV4U) or MAT 1339'
        if re.match(uOOneOfCondPat, item):
            temp = item[7:]
            orList = splitCourseOrCond(temp, r' or | ou ')
            newList = []
            numCourses = len(orList)
            for newElem in orList:
                newList.append(parseUOttawaPrereqElm(newElem))
            
            prereqList.append((numCourses, newList))
        
        commaSplitList = splitOnComma(item)
        for element in commaSplitList:
            # Single isolated couse code
            if re.match(uOCourseCodeIsolatedPat, element):
                prereqList.append(element)
            # Message regarding 'cannot be combined' -- ignore case
            elif re.match(uONotCombineFRPat, element) or re.match(uONotCombineENGPat, element):
                continue
            # premission required case (2 of several) -- rest ignored
            elif re.match(r'Permission de l\'Institut', element) \
                    or re.match(r'permission of the instructor', element):
                prereqList.append(element)
            
            elif re.match(uOCreditPrereqENGPat, element) or re.match(uOCreditPrereqFRPat, element):
                prereqList.append(element)

            elif    re.search(r'This course is (?:primarily )?intended', element) \
                    or re.search(r'principalement aux étudiants', element) \
                    or re.search(r'cours est destiné', element) or re.search(r'cours ne peut pas', element)\
                    or re.search(r'an equivalent', element) \
                    or re.search(r'verify your program', element) \
                    or re.search(r'cannot count', element):
                pass
            # case of a list with third party courses
            elif re.search(uOThirdPartyCourseListPat, element):
                temp = re.split(uOThirdPartyCourseListPat, element)
                for item in temp:
                    if re.search(r'\w{4}[ ]?\d{4}', item):
                        pass
                    else:
                        prereqList.append(parseUOttawaPrereqElm(item))
            # case where single course code has third party alternative
            elif re.match(uOSingleThirdPartyOptPat, element):
                newCourse = re.search(uOCourseCodePat, element).group()
                prereqList.append(newCourse)
            # single or condition without brackets
            elif re.match(uOOrCondNoBracketIsoPat, element):
                orList = splitCourseOrCond(element, r' or | ou ')
                tempList = []
                for item in orList:
                    if re.match(uOCourseCodeIsolatedPat, item):
                        tempList.append(item)
                
                # case where something other than a course code is part of an OR group
                # which then becomes of length 1
                if len(tempList) == 1:
                    prereqList.append(tempList[0])
                elif len(tempList) > 1:
                    prereqList.append(tempList)
            # and list, possibly multiple
            elif re.match(uOAndListIsoPat, element):
                # single and condition (two courses)
                if re.match(uOAndCondIsoPat, element):
                    andList = splitCourseOrCond(element, r' and | et |, ')
                    
                    for item in andList:
                        if re.match(uOCourseCodeIsolatedPat, item):
                            prereqList.append(item)
            # Ontario Highschool course code
            elif re.search(r'[ \(][A-Z]{3}[ ]?\d[A-Z]', element):
                newItem = re.search(r'[ \(][A-Z]{3}[ ]?\d[A-Z]', element).group()
                if newItem.startswith('(') or newItem.startswith(' '):
                    newItem = newItem[1:]
                prereqList.append(newItem)
            # check if brackets surrounding text exist
            elif re.search(r'\(.+\)', element):
                #case where there is an OR list
                if re.match(uOOrListPat, element):
                    prereqList.append(splitCourseOrCond(element, r' or | ou ', uOCourseCodePat))
                # check if a uOttawa course code exists
                elif re.search(uOCourseCodePat, element):
                    #split by commas outside of brackets
                    bracketSplitList = re.split(stringListSplitterPat, element)
                    tempList = []
                    for item in bracketSplitList:
                        # filter out split prereqs starting with 'or'
                        if re.search(r' or | ou ', item):
                            if item.startswith('or'):
                                pass
                            splitList = splitCourseOrCond(item, r' or | ou ', uOCourseCodePat)
                            for ele in splitList:
                                tempList.append(parseUOttawaPrereqElm(ele)) 
                        # filter out coreq cases
                        elif re.search(r'coreq', item) or re.search(r'concomitant', item):
                            pass
                        # if starting with a uOttawa course code, add it
                        elif re.match(r'^[a-zA-Z]{3}[ ]?\d{4}', item):
                            prereqList.append(re.match(r'^[a-zA-Z]{3}[ ]?\d{4}', item).group())
                        
                    prereqList.append(tempList)
                # filter everything else
                else:
                    pass
    return prereqList
   

def parseUOttawaPrereqs(courseData : list):

    for i, element in enumerate(courseData):
        # print('subject:', element['course_name'])
        prereqString = element['prereqs']
        # print('prereqstring:', prereqString)
        if len(prereqString) == 0:
            continue

        prereqList = []

        for ele in prereqString:
            # if it is not an english course split and discard english translations if they exist
            # potentially breaking if the ` / ` sequence exists for a different purpose
            if not re.match(uOEnglishCoursePat, element['course_num']):
                ele = ele.split(' / ', 2)[0]
            prereq = parseUOttawaPrereqElm(ele)
            if len(prereq) == 1 and prereq[0] == '':
                pass
            else:
                if isinstance(prereq, list):
                    for item in prereq:
                        prereqList.append(item)
                else:
                    prereqList.append(prereq)

        #
        #TODO: convert prereq to new object as per #115
        #print(newPrereq)
        #
        courseData[i]['prereqs'] = prereqList

##################################


if __name__ == "__main__":

    if not len(sys.argv) == 3:
        exit('Invalid Arguments')

    fileIn = sys.argv[1]  # plain text file
    fileOut = sys.argv[2]    # output JSON file

    
    tempList = []
    courseDataList = course_util.get_courses(fileIn)
   
    parseUOttawaPrereqs(courseDataList)
    
    json_object = json.dumps(courseDataList, indent=2, ensure_ascii=False)     # dumping into JSON
    # Writing to sample.json
    with open(fileOut, "w") as outfile:        # writing to JSON file
        outfile.truncate(0)
        outfile.write(json_object)

