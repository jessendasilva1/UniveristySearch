import sys
import os
import json

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import course_util
import graph
import validateGraph

# NOTICE: ONLY PRINTS OUT FAILED TESTS, IF NOT PRINTED IT PASSED TEST

###########
# IMPORTANT# moved example.json out of examples file in local testing
###########
fileName = './examples/example.json'
i = 0
courseList = course_util.get_courses(fileName)
if not (isinstance(courseList, list)):  # Test to see if list is returned from json
    print("Test 1 FAIL: courseList is type", type(courseList))

for course in courseList:
    if not (isinstance(course, dict)):  # Test to see if all items in list are dictionaries
        print("Test 2 FAIL: Some course in courseList is type", type(course))

for course in courseList:
    i += 1
    if not (course_util.is_valid_course(course)):  # Test if all courses are valid dictionaries
        print("Test 3 FAIL: Course", i, "is invalid")

###################
# SUBJECT TESTING #
###################
if not (course_util.is_in_course_dict(courseList[0], "subject", "ANTH")):  # Test for expected subject
    print("Test 4 FAIL: Course 0 rejects expected subject.")

if course_util.is_in_course_dict(courseList[0], "subject", "CIS"):  # Test for not-expected subject
    print("Test 5 FAIL: Course 0 accepts non-expected subject.")

# case handled by CLI
if course_util.is_in_course_dict(courseList[0], "subject", ""):  # Test for empty subject
    print("Test 6 FAIL: Course 0 accepts empty subject.")

#######################
# COURSE_NAME TESTING #
#######################
if not (
        course_util.is_in_course_dict(courseList[0], "course_name",
                                      "Regional Ethnography")):  # Test for expected course_name
    print("Test 7 FAIL: Course 0 rejects expected course_name.")

if (course_util.is_in_course_dict(courseList[0], "course_name",
                                  "Software Engineering")):  # Test for non-expected course_name
    print("Test 8 FAIL: Course 0 accepts non-expected course_name.")

if course_util.is_in_course_dict(courseList[0], "course_name", ""):  # Test for empty course_name
    print("Test 9 FAIL: Course 0 accepts empty course_name.")

####################
# OFFERING TESTING #
####################
# tests case outside scope, will only ever search for a term, not the lack of one
# if not(course_util.is_in_course_dict(courseList[0], "offering", None)):  #Test for expected offering
#     print("Test 10 FAIL: Course 0 rejects expected offering.")

if course_util.is_in_course_dict(courseList[0], "offering", "Never Offered"):  # Test for non-expected offering
    print("Test 11 FAIL: Course 0 accepts non-expected offering.")

if course_util.is_in_course_dict(courseList[0], "offering", ""):  # Test for empty offering
    print("Test 12 FAIL: Course 0 accepts empty offering.")

########################
# OFFERED_FALL TESTING #
########################
if not (course_util.is_in_course_dict(courseList[0], "is_offered_fall", True)):  # Test for expected fall offering
    print("Test 13 FAIL: Course 0 rejects expected fall offering.")

if course_util.is_in_course_dict(courseList[0], "is_offered_fall", False):  # Test for non-expected fall offering
    print("Test 14 FAIL: Course 0 accepts non-expected fall offering.")

if course_util.is_in_course_dict(courseList[0], "is_offered_fall", "t-rue"):  # Test for invalid fall offering
    print("Test 15 FAIL: Course 0 accepts invalid fall offering.")

if course_util.is_in_course_dict(courseList[0], "is_offered_fall", ""):  # Test for empty fall offering
    print("Test 16 FAIL: Course 0 accepts empty fall offering.")

##########################
# OFFERED_WINTER TESTING #
##########################
if not (course_util.is_in_course_dict(courseList[0], "is_offered_winter", False)):  # Test for expected winter offering
    print("Test 17 FAIL: Course 0 rejects expected winter offering.")

if course_util.is_in_course_dict(courseList[0], "is_offered_winter", True):  # Test for non-expected winter offering
    print("Test 18 FAIL: Course 0 accepts non-expected winter offering.")

if course_util.is_in_course_dict(courseList[0], "is_offered_winter", "t-rue"):  # Test for invalid winter offering
    print("Test 19 FAIL: Course 0 accepts invalid winter offering.")

if course_util.is_in_course_dict(courseList[0], "is_offered_winter", ""):  # Test for empty winter offering
    print("Test 20 FAIL: Course 0 accepts empty winter offering.")

##########################
# OFFERED_SUMMER TESTING #
##########################
if not (course_util.is_in_course_dict(courseList[0], "is_offered_summer", False)):  # Test for expected summer offering
    print("Test 21 FAIL: Course 0 rejects expected summer offering.")

if course_util.is_in_course_dict(courseList[0], "is_offered_summer", True):  # Test for non-expected summer offering
    print("Test 22 FAIL: Course 0 accepts non-expected summer offering.")

if course_util.is_in_course_dict(courseList[0], "is_offered_summer", "true"):  # Test for invalid summer offering
    print("Test 23 FAIL: Course 0 accepts invalid summer offering.")

if course_util.is_in_course_dict(courseList[0], "is_offered_summer", ""):  # Test for empty summer offering
    print("Test 24 FAIL: Course 0 accepts empty summer offering.")

####################
# PREREQS TESTING #
###################
if not (course_util.is_in_course_dict(courseList[0], "prereqs", "ANTH*1150")):  # Test for expected prereqs
    print("Test 25 FAIL: Course 0 rejects expected prereqs.")

if course_util.is_in_course_dict(courseList[0], "prereqs", "CIS*1300"):  # Test for non-expected prereqs
    print("Test 26 FAIL: Course 0 accepts non-expected prereqs.")

if course_util.is_in_course_dict(courseList[0], "prereqs", ""):  # Test for empty prereqs
    print("Test 27 FAIL: Course 0 accepts empty prereqs.")

######################
# COURSE NUM TESTING #
#####################
if not (course_util.is_in_course_dict(courseList[0], "course_num", 2230)):  # Test for expected course_num
    print("Test 28 FAIL: Course 0 rejects expected course_num.")

if course_util.is_in_course_dict(courseList[0], "course_num", "3750"):  # Test for non-expected course_num
    print("Test 29 FAIL: Course 0 accepts non-expected course_num.")

if course_util.is_in_course_dict(courseList[0], "course_num", "aaa"):  # Test for invalid course_num
    print("Test 30 FAIL: Course 0 accepts invalid course_num.")

if course_util.is_in_course_dict(courseList[0], "course_num", ""):  # Test for empty course_num
    print("Test 31 FAIL: Course 0 accepts empty course_num.")

###################
# CREDITS TESTING #
###################
if not (course_util.is_in_course_dict(courseList[0], "credits", 0.5)):  # Test for expected credits
    print("Test 33 FAIL: Course 0 rejects expected credits.")

if course_util.is_in_course_dict(courseList[0], "credits", 0.75):  # Test for non-expected credits
    print("Test 34 FAIL: Course 0 accepts non-expected credits.")

if course_util.is_in_course_dict(courseList[0], "credits", "aaa"):  # Test for invalid credits
    print("Test 35 FAIL: Course 0 accepts invalid credits.")

if course_util.is_in_course_dict(courseList[0], "credits", ""):  # Test for empty credits
    print("Test 36 FAIL: Course 0 accepts empty credits.")

####################
# LECTURES TESTING #
####################
if not (course_util.is_in_course_dict(courseList[0], "lectures", 3)):  # Test for expected lectures
    print("Test 37 FAIL: Course 0 rejects expected lectures.")

if course_util.is_in_course_dict(courseList[0], "lectures", 5):  # Test for non-expected lectures
    print("Test 38 FAIL: Course 0 accepts non-expected lectures.")

if course_util.is_in_course_dict(courseList[0], "lectures", "aaa"):  # Test for invalid lectures
    print("Test 39 FAIL: Course 0 accepts invalid lectures.")

if course_util.is_in_course_dict(courseList[0], "lectures", ""):  # Test for empty lectures
    print("Test 40 FAIL: Course 0 accepts empty lectures.")

################
# LABS TESTING #
################
if not (course_util.is_in_course_dict(courseList[0], "labs", 0)):  # Test for expected labs
    print("Test 41 FAIL: Course 0 rejects expected labs.")

if course_util.is_in_course_dict(courseList[0], "labs", 5):  # Test for non-expected labs
    print("Test 42 FAIL: Course 0 accepts non-expected labs.")

if course_util.is_in_course_dict(courseList[0], "labs", "aaa"):  # Test for invalid labs
    print("Test 43 FAIL: Course 0 accepts invalid labs.")

if course_util.is_in_course_dict(courseList[0], "labs", ""):  # Test for empty labs
    print("Test 44 FAIL: Course 0 accepts empty labs.")

###################
# EQUATES TESTING #
###################

if not (course_util.is_in_course_dict(courseList[0], "equates", "[]")):  # Test for expected equates
    print("Test 45 FAIL: Course 0 rejects expected equates.")

if course_util.is_in_course_dict(courseList[0], "equates", "[]"):  # Test for non-expected equates
    print("Test 45 FAIL: Course 0 accepts non-expected equates.")  # equates should never accept  if list is empty

if course_util.is_in_course_dict(courseList[0], "equates", "CIS*1300"):  # Test for non-expected equates
    print("Test 46 FAIL: Course 0 accepts non-expected equates.")

if course_util.is_in_course_dict(courseList[0], "equates", ""):  # Test for empty equates
    print("Test 47 FAIL: Course 0 accepts empty equates.")

########################
# RESTRICTIONS TESTING #
########################

if not (course_util.is_in_course_dict(courseList[0], "restrictions", "")):  # Test for expected restrictions
    print("Test 48 FAIL: Course 0 rejects expected restrictions.")

if course_util.is_in_course_dict(courseList[0], "restrictions", "[]"):  # Test for expected restrictions
    print(
        "Test 48 FAIL: Course 0 accepts non-expected restrictions.")  # restrictions should never accept  if list is empty

if course_util.is_in_course_dict(courseList[0], "restrictions", "No Restriction"):  # Test for non-expected restrictions
    print("Test 49 FAIL: Course 0 accepts non-expected restrictions.")

if course_util.is_in_course_dict(courseList[0], "restrictions", ""):  # Test for empty restrictions
    print("Test 50 FAIL: Course 0 accepts empty restrictions.")

######################
# DEPARTMENT TESTING #
######################
if not (course_util.is_in_course_dict(courseList[0], "dept",
                                      "Department of Sociology and Anthropology")):  # Test for expected department
    print("Test 51 FAIL: Course 0 rejects expected department.")

if course_util.is_in_course_dict(courseList[0], "dept", "No Restriction"):  # Test for non-expected department
    print("Test 52 FAIL: Course 0 accepts non-expected department.")

if course_util.is_in_course_dict(courseList[0], "dept", ""):  # Test for empty department
    print("Test 53 FAIL: Course 0 accepts empty department.")

####################
# LOCATION TESTING #
####################
if not (course_util.is_in_course_dict(courseList[0], "location", "Guelph")):  # Test for expected location
    print("Test 54 FAIL: Course 0 rejects expected location.")

if course_util.is_in_course_dict(courseList[0], "location", "Online"):  # Test for non-expected location
    print("Test 55 FAIL: Course 0 accepts non-expected location.")

if course_util.is_in_course_dict(courseList[0], "location", ""):  # Test for empty location
    print("Test 56 FAIL: Course 0 accepts empty location.")

###################
# CO_REQS TESTING #
###################

if not (course_util.is_in_course_dict(courseList[0], "co_reqs", "[]")):  # Test for expected co_reqs
    print("Test 57 FAIL: Course 0 rejects expected co_reqs.")

if course_util.is_in_course_dict(courseList[0], "co_reqs", "[]"):  # Test for expected co_reqs
    print("Test 57 FAIL: Course 0 accepts non-expected co_reqs.")  # co reqs should never accept  if list is empty

if course_util.is_in_course_dict(courseList[0], "co_reqs", "CIS*1300"):  # Test for non-expected co_reqs
    print("Test 58 FAIL: Course 0 accepts non-expected co_reqs.")

if course_util.is_in_course_dict(courseList[0], "co_reqs", ""):  # Test for empty co_reqs
    print("Test 59 FAIL: Course 0 accepts empty co_reqs.")

if course_util.is_in_course_dict(courseList[0], "co_reqs", "{}"):  # Test for empty dictionary co_reqs
    print("Test 60 FAIL: Course 0 accepts empty dictionary co_reqs.")

if course_util.is_in_course_dict(courseList[0], "co_reqs", "[[]]"):  # Test for list within list
    print("Test 61 FAIL: Course 0 accepts list within list co_reqs.")

if course_util.is_in_course_dict(courseList[0], "co_reqs", "['CIS*1300']"):  # Test for ["CIS*1300]
    print("Test 62 FAIL: Course 0 accepts list within list co_reqs.")

##############
# Validation #
##############

#courseData = course_util.get_courses('./courseData.json')
#print("Validation of graph ACCT")
#validateGraph.validate(graph.graphMake('ACCT', None))
#print("Validation of graph CIS")
#validateGraph.validate(graph.graphMake('CIS', None))
#print("Validation of graph BIOL")
#validateGraph.validate(graph.graphMake('BIOL', None))
#print("Validation of graph MATH")
#validateGraph.validate(graph.graphMake('MATH', None))
#print("Validation of graph STAT")
#validateGraph.validate(graph.graphMake('STAT', None))


#########################
# Validaiton of prereqs #
#########################
#Only prints if there is an error

courseData = course_util.get_courses('./tests/courseData_bak.json')

#Test case 1:   HTM*2020, MCS*1000 --> [['HTM*2020'], ['MCS*1000']]
if not (str(courseData[0]['prereqs']).strip() == "[['HTM*2020'], ['MCS*1000']]"):
    print("Test 63 Failed: ", courseData[0]['prereqs'], " != [['HTM*2020'],['MCS*1000']]")

#Test case 2:   2.00 credits including (MGMT*1000 or MGMT*2150) --> ['1.5', ['MGMT*1000', 'MGMT*2150']]
if not (str(courseData[1]['prereqs']).strip() == "['1.5', ['MGMT*1000', 'MGMT*2150']]"):
    print("Test 64 Failed: ", courseData[1]['prereqs'], " )!= ['1.5', ['MGMT*1000', 'MGMT*2150']]")

#Test case 3:   1 of HTM*1000, HTM*1160, HTM*1700, HTM*2020 --> [['HTM*1000', 'HTM*1160', 'HTM*1700', 'HTM*2020']]
if not (str(courseData[2]['prereqs']).strip() == "[['HTM*1000', 'HTM*1160', 'HTM*1700', 'HTM*2020']]"):
    print("Test 65 Failed: ", courseData[2]['prereqs'], " != [['HTM*1000', 'HTM*1160', 'HTM*1700', 'HTM*2020']]")

#Test case 4:   9.00 credits including HTM*2010, (HTM*1160 or HTM*2100) --> ['8.0', ['HTM*2010'], ['HTM*1160', 'HTM*2100']]
if not (str(courseData[3]['prereqs']).strip() == "['8.0', ['HTM*2010'], ['HTM*1160', 'HTM*2100']]"):
    print("Test 66 Failed: ", (courseData[3]['prereqs']), " != ['8.0', ['HTM*2010'], ['HTM*1160', 'HTM*2100']]")

#Test case 5:   (ACCT*1220 or ACCT*2220), (1 of ECON*2740, PSYC*1010, STAT*2040, STAT*2060, STAT*2080) --> [['ACCT*1220', 'ACCT*2220'], ['ECON*2740', 'PSYC*1010', 'STAT*2040', 'STAT*2060', 'STAT*2080']]
if not (str(courseData[4]['prereqs']).strip() == "[['ACCT*1220', 'ACCT*2220'], ['ECON*2740', 'PSYC*1010', 'STAT*2040', 'STAT*2060', 'STAT*2080']]"):
    print("Test 68 Failed: ", (courseData[4]['prereqs'])," != [['ACCT*1220', 'ACCT*2220'], ['ECON*2740', 'PSYC*1010', 'STAT*2040', 'STAT*2060', 'STAT*2080']]")


#Test case 6:   (CIS*1300 or CIS*1500), (1 of IPS*1510, MATH*1090, MATH*1210, MATH*2080) --> [['CIS*1300', 'CIS*1500'], ['IPS*1510', 'MATH*1090', 'MATH*1210', 'MATH*2080']]
if not (str(courseData[5]['prereqs']).strip() == "[['CIS*1300', 'CIS*1500'], ['IPS*1510', 'MATH*1090', 'MATH*1210', 'MATH*2080']]"):
    print("Test 69 Failed: ", (courseData[5]['prereqs'])," != [['CIS*1300', 'CIS*1500'], ['IPS*1510', 'MATH*1090', 'MATH*1210', 'MATH*2080']]")

#Test case 7:   1 of 4U Calculus and Vectors, 4U Advanced Functions and Calculus or Grade 12 Calculus --> [['4U Calculus and Vectors', '4U Advanced Functions and Calculus', 'Grade 12 Calculus']]
if not (str(courseData[6]['prereqs']).strip() == "[['4U Calculus and Vectors', '4U Advanced Functions and Calculus', 'Grade 12 Calculus']]"):
    print("Test 70 Failed: ", (courseData[6]['prereqs'])," != [['4U Calculus and Vectors', '4U Advanced Functions and Calculus', 'Grade 12 Calculus']]")

#Test case 8:   15.00 Credits including MCS*3030, MCS*3500, MCS*3620 -->  [['15.00 Credits including MCS*3030'], ['MCS*3500'], ['MCS*3620']]
if not (str(courseData[7]['prereqs']).strip() == "[['15.00 Credits including MCS*3030'], ['MCS*3500'], ['MCS*3620']]"):
    print("Test 71 Failed: ", (courseData[7]['prereqs'])," != [['15.00 Credits including MCS*3030'], ['MCS*3500'], ['MCS*3620']]")

#Test case 9:    15.00 Credits including one of MCS*3030, MCS*3500, MCS*3620 -->  [['15.00 Credits including one of MCS*3030'], ['MCS*3500'], ['MCS*3620']]
if not (str(courseData[8]['prereqs']).strip() == "[['15.00 Credits including one of MCS*3030'], ['MCS*3500'], ['MCS*3620']]"):
    print("Test 72 Failed: ", (courseData[8]['prereqs'])," !=  [['15.00 Credits including one of MCS*3030'], ['MCS*3500'], ['MCS*3620']]")

#Test case 10:   XSEN*4030. Restricted to BSCH.BPCH and BSCH.BPCH:C --> ["XSEN*4030. Restricted to BSCH.BPCH and BSCH.BPCH:C"]
if not (str(courseData[9]['prereqs']).strip() == "[['XSEN*4030. Restricted to BSCH.BPCH and BSCH.BPCH:C']]"):
    print("Test 73 Failed: " , (courseData[9]['prereqs'])," !=  [['XSEN*4030. Restricted to BSCH.BPCH and BSCH.BPCH:C']]")


#Testing updated scraper for Majors
majorsFile = open('./scraper/degreeProgramCourses.json')
majorsString = majorsFile.read()
majorsJSON = json.loads(majorsString)
majorsFile.close()
#print(majorsJSON)
flag = 0
flag2 = 0
flag3 = 0
#Test set 1: Check for correct info in a basic test case (CIS)
for major in majorsJSON:
    if 'degreeName' in major.keys():
        if major['degreeName'] == 'Bachelor of Computing (B.Comp.)':
            flag = 1
    if 'degreeCode' in major.keys():
        if major['degreeCode'] == 'B.Comp.':
            flag2 = 1
            if 'MATH*1160' in major['requiredCourses']:
                flag3 = 1

if flag == 0:
    print("Test 74 Failed: Bachelor of Computing (B.Comp.) not found for degreeName")
if flag2 == 0:
    print("Test 75 Failed: B.Comp not found for degreeCode")
if flag3 == 0:
    print("Test 76 Failed: MATH*1160 Not found in requiredCourses")
flag = 0
flag2 = 0
flag3 = 0
flag4 = 0
#Test set 2: Check for correct info in a COOP test case
for major in majorsJSON:
    if 'degreeName' in major.keys():
        if major['degreeName'] == 'Bachelor of Engineering (B.Eng.)':
            flag = 1
    if 'majorName' in major.keys():
        if major['majorName'] == 'Engineering Systems and Computing Program Co-op (ESC:C)':
            flag2 = 1
        if 'COOP*1000' not in major['requiredCourses']:
            flag3 = 1
        if 'ENGG*4000' not in major['requiredCourses']:
            flag4 = 1
if flag == 0:
    print("Test 77 Failed: Bachelor of Engineering (B.Eng.) not found for degreeName")
if flag2 == 0:
    print("Test 78 Failed: ESC:C not found for degreeCode")
if flag3 == 0:
    print("Test 79 Failed: Missing 'COOP*1000' entry in requiredCourses")
if flag4 == 0:
    print("Test 80 Failed: Missing 'ENGG*4000' entry in requiredCourses")

#Test set 3: Check for various bits of data
if not (json.dumps(majorsJSON[0]['requiredCourses'][1]).strip() == '["HTM*2700", "NUTR*1010"]'):
    print('Test 81 Failed: Optional list ["HTM*2700", "NUTR*1010"] not found.')
if not (json.dumps(majorsJSON[5]['requiredCourses'][8]).strip() == '["FRHD*2060", "FRHD*2280"]'):
    print('Test 82 Failed: Optional list ["HTM*2700", "NUTR*1010"] not found.')
if  majorsJSON[0]['totalElectiveWeight'] != 7:
    print('Test 83 Failed: totalElectiveWeight ' + str(majorsJSON[0]['totalElectiveWeight']) + ' != 7')
if len(majorsJSON[183]['requiredCourses']) != 0:
    print('Test 84 Failed: Expected length = 0, instead got ' + str(len(majorsJSON[183]['requiredCourses'])))

#Test set 4: Test some graph functionality
majorDict = course_util.getMajors('./scraper/degreeProgramCourses.json', 'ESC:C', 'B.Eng.')
if not majorDict:
    print('Test 85 Failed: Could not find major ESC:C with degree code B.Eng.')
if majorDict:
    graph.generateMajorGraph(majorDict)
    majorLines = open('./major_graph.dot', 'r').readlines()
    #Test out mandatory edges first
    if '"MATH*1210" -> "ENGG*2400" \n' not in majorLines:
        print('Test 86 Failed: Expected "MATH*1210" -> "ENGG*2400" in major_graph.dot')
    if '"ENGG*3640" -> "ENGG*4420" \n' not in majorLines:
        print('Test 87 Failed: Expected "ENGG*3640" -> "ENGG*4420" in major_graph.dot')
    if '"PHYS*1130" -> "ENGG*2120" \n' not in majorLines:
        print('Test 88 Failed: Expected "PHYS*1130" -> "ENGG*2120" in major_graph.dot')
    if '"ENGG*2400" -> "ENGG*4420" \n' not in majorLines:
        print('Test 89 Failed: Expected "ENGG2400" -> "ENGG*4420" in major_graph.dot')
    if '"ENGG*1210" -> "ENGG*2400" \n' not in majorLines:
        print('Test 90 Failed: Expected "COOP*2000" -> "COOP*3000" in major_graph.dot')
    if '"STAT*2120" -> "ENGG*3130" \n' not in majorLines:
        print('Test 91 Failed: Expected "STAT*2120" -> "ENGG*3130" in major_graph.dot')
    if '"ENGG*3100" -> "ENGG*4000" \n' not in majorLines:
        print('Test 92 Failed: Expected "ENGG*3100" -> "ENGG*4000" in major_graph.dot')
   
    #Test out optional edges
    if '"CIS*1300" -> "ENGG*3130" [style="dashed",color="grey",shape="odot"]\n' not in majorLines:
        print('Test 93 Failed: Expected "CIS*1300" -> "ENGG*3130" [style="dashed",color="grey",shape="odot"] in major_graph.dot')
    if '"CIS*1500" -> "ENGG*3130" [style="dashed",color="grey",shape="odot"]\n' not in majorLines:
        print('Test 94 Failed: Expected "CIS*1500" -> "ENGG*3130" [style="dashed",color="grey",shape="odot"] in major_graph.dot')
    if '"CIS*2500" -> "CIS*2520" [style="dashed",color="grey",shape="odot"]\n' not in majorLines:
        print('Test 95 Failed: Expected "CIS*2500" -> "ENGG*2520" [style="dashed",color="grey",shape="odot"] in major_graph.dot')
    #Seems like the optional edges have some inconsistent labelling 
    
    if '"MATH*1160" -> "MATH*2270" [style="dashed",color="grey",shape="odot"]\n' not in majorLines:
        print('Test 96 Failed: Expected "MATH*1160" -> "MATH*2270" [style="dashed",color="grey",shape="odot"] in major_graph.dot')
    if '"ENGG*1500" -> "MATH*2270" [style="dashed",color="grey",shape="odot"]\n' not in majorLines:
        print('Test 97 Failed: Expected "ENGG*1500" -> "MATH*2270" [style="dashed",color="grey",shape="odot"] in major_graph.dot')
    if '"CIS*2420" -> "ENGG*4450" [style="dashed",color="grey",shape="odot"]\n' not in majorLines:
        print('Test 98 Failed: Expected "CIS*2420" -> "ENGG*4450" [style="dashed",color="grey",shape="odot"] in major_graph.dot')
    if '"CIS*2520" -> "ENGG*4450" [style="dashed",color="grey",shape="odot"]\n' not in majorLines:
        print('Test 99 Failed: Expected "CIS*2520" -> "ENGG*4450" [style="dashed",color="grey",shape="odot"] in major_graph.dot')
    
    #Niche case with label
    if '"MATH*1210" -> "ENGG*3240" [style="dashed",color="grey",shape="odot",label="10.25 credits including"]\n' not in majorLines:
        print('Test 100 Failed: Expected "MATH*1210" -> "ENGG*3240" [style="dashed",color="grey",shape="odot",label="10.25 credits including"] in major_graph.dot')
    