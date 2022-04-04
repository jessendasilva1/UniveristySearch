# Collection of utility functions for Course dictionary structure #
# Converts a course dictionary object to a user-friendly readable string

# importing json
import json
import re

"""
converting course title to string
"""


def course_title_to_string(course: dict) -> str:
    courseStr = '{} {} {}'.format(course['subject'], course['course_num'], course['course_name'])

    return courseStr


"""
converts a course dict into a readable string
"""


def courseToString(course: dict) -> str:
    semestersOffered = ''
    # puts semester offered for
    if course['is_offered_fall']:
        if course['is_offered_winter']:
            if course['is_offered_summer']:
                semestersOffered = 'Fall, Winter, and Summer'
            else:
                semestersOffered = 'Fall and Winter'
        elif course['is_offered_summer']:
            semestersOffered = "Fall and Summer"
        else:
            semestersOffered = 'Fall Only'
    elif course['is_offered_winter']:
        if course['is_offered_summer']:
            semestersOffered = 'Winter and Summer'
        else:
            semestersOffered = 'Winter Only'
    elif course['is_offered_summer']:
        semestersOffered = 'Summer Only'
    else:
        semestersOffered = "Unspecified"

    # course string
    courseStr = '{} {} {}\tOffered in: {}\t(LEC: {}, LAB:{}) [{}]\nDescription: {}\n'.format(
        course['subject'], course['course_num'], course['course_name'],
        semestersOffered, course['lectures'], course['labs'], course['credits'],
        course['description'])

    # if a course offering is true - concatenate to course string
    if course['offering']:
        courseStr += 'Offering(s): {}\n'.format(course['offering'])

    # course prerequisite is none
    if len(course['prereqs']) < 1:
        courseStr += 'Prerequisite(s): None\n'
    elif len(course['prereqs']) == 1:  # course prereqs exists
        courseStr += 'Prerequisite(s): {}'.format(course['prereqs'][0] + '\n')
    else:
        courseStr += 'Prerequisite(s): '
        for item in course['prereqs']:
            if isinstance(item, list):
                for prereq in item:
                    if isinstance(prereq, list):
                        courseStr += ', '.join(prereq)
                    else:
                        courseStr += prereq + ', '
            else:
                courseStr += item + ', '
        courseStr = courseStr[:-2]
        courseStr += '\n'

    # course equates
    if len(course['equates']) < 1:
        courseStr += 'Co-Reqrequisite(s): None\n'
    elif course['co_reqs'] == 1:
        courseStr += 'Co-Reqrequisite(s): {}'.format(course['co_reqs'][0] + '\n')
    else:
        courseStr += 'Co-Reqrequisite(s): {}'.format(', '.join(course['co_reqs']))
        courseStr = courseStr[:-2]
        courseStr += '\n'

    if len(course['equates']) < 1:
        courseStr += 'Equate(s): None\n'
    elif len(course['equates']) == 1:
        courseStr += 'Equate(s): {}'.format(course['equates'][0] + '\n')
    else:
        courseStr += 'Equate(s): {}'.format(', '.join(course['equates']))
        courseStr = courseStr[:-2]
        courseStr += '\n'

    # course restrictions
    if len(course['restrictions']) < 1:
        courseStr += 'Restrictions(s): None\n'
    elif len(course['restrictions']) == 1:
        courseStr += 'Restrictions(s): {}'.format(course['restrictions'][0] + '\n')
    else:
        courseStr += 'Restrictions(s): {}'.format(', '.join(course['restrictions']))
        courseStr = courseStr[:-2]
        courseStr += '\n'

    # course dept
    if len(course['dept']) < 1:
        courseStr += 'Department(s): Unspecified\n'
    elif len(course['dept']) == 1:
        courseStr += 'Department(s): {}'.format(course['dept'][0] + '\n')
    else:
        courseStr += 'Department: {}'.format(', '.join(course['dept']))
        courseStr = courseStr[:-2]
        courseStr += '\n'

    # course location
    if len(course['location']) < 1:
        courseStr += 'Location(s): Unspecified\n'
    elif len(course['location']) == 1:
        courseStr += 'Location(s): {}'.format(course['location'][0] + '\n')
    else:
        courseStr += 'Location(s): {}'.format(', '.join(course['location']))
        courseStr = courseStr[:-2]
        courseStr += '\n'

    return courseStr


# print the results of each course
def print_search_results(results: list) -> None:
    for course in results:
        print(course_title_to_string(course))


# Validate course dict
def is_valid_course(course: dict) -> bool:
    keys = ['subject', 'course_num', 'course_name', 'is_offered_fall', 'is_offered_winter', 'is_offered_summer',
            'lectures', 'labs',
            'credits', 'description', 'offering', 'unknown', 'prereqs', 'co_reqs', 'equates', 'restrictions', 'dept',
            'location']

    for i in range(len(keys)):  # Check that all required keys are present
        if not keys[i] in course:
            return False
    for key in course:
        if key == 'subject' or key == 'course_name' or key == 'description':
            if not (isinstance(course.get(key), str)):  # Check correct str values
                return False
        elif key == 'course_num' or key == 'lectures' or key == 'labs' or key == 'credits':
            if not (isinstance(course.get(key), int) or isinstance(course.get(key), float)):  # Check correct num values
                return False
        elif key == 'prereqs' or key == 'equates' or key == 'restrictions' or key == 'dept' or key == 'location' or key == 'co_reqs' or key == 'offering':
            if isinstance(course.get(key), list):
                if course.get(key) is None:  # Check if list is none
                    return False
        elif key == 'is_offered_fall' or key == 'is_offered_winter' or key == 'is_offered_summer':
            if not isinstance(course.get(key), bool):
                return False
        elif key == 'unknown':
            if not course.get(key) and not isinstance(course.get(key), str):  # check if unknown is empty (None)
                if not (course.get(key) is not None):
                    return False
        else:  # Check correct list values
            return False
        # if not key in keys: #Check for keys that aren't required
        # return False
    return True


# Read in text file from scraper and return a validated list of course dict
def get_courses(file_in: str) -> list:
    f = open(file_in, mode='r', encoding='utf-8')
    jsonString = f.read()
    jsonData = json.loads(jsonString)
    f.close()
    # for course in jsonData:
    #     if not is_valid_course(course):
    #        pass
    # raise ValueError('Invalid course data. Please re-run parser.py')
    return jsonData


# search course dictionary for key, value return true if found, false otherwise
# refer to examples/course_arr_example.py for dict structure
def is_in_course_dict(dictionary: dict, key: str, value) -> bool:
    string_keys = [
        "subject", "course_name", "description", "unknown"
    ]

    list_keys = [
        "prereqs", "equates", "restrictions", "dept", "location", "offering", "co_reqs"
    ]

    int_keys = [
        "course_num", "lectures", "labs", "credits"
    ]
    bool_keys = [
        "is_offered_fall", "is_offered_winter", "is_offered_summer"
    ]

    # if key is in string key list, if not found return false else return true
    if key in string_keys:
        if len(value) == 0:
            return False
        elif value.lower() in dictionary[key].lower():
            return True
        else:
            return False
    elif key in int_keys:  # if key in int key list and value exists return true else false
        if value == str(dictionary[key]):
            return True
        else:
            return False
    elif key in bool_keys:  # if key is boolean and value is found return true else false
        return dictionary[key] == value
    elif key in list_keys:  # if key in list_keys return and value is found return rtrue
        if not value:
            return False
        for element in dictionary[key]:
            if value.lower() in element.lower():
                return True
        return False

    else:  # Key is not found raise an ValueError
        raise ValueError('key given is not specified in arrays')


"""
filter the course away based on a key-value pair
"""


def filter_course_arr(courses: list, key: str, value) -> list:
    """
    running queries based on key-value pair
    """
    filtered_list = []
    for index in range(len(courses)):
        if is_in_course_dict(courses[index], key, value):
            filtered_list.append(courses[index])
    return filtered_list


# checks if string is float exists
def try_float(string: str) -> bool:
    try:
        float(string)
        return True
    except ValueError:
        return False
    except TypeError:
        return False


# clears prefixes and suffixes from string
def stringClean(string: str) -> str:
    string = string.strip("[.]' ")
    string = string.strip(".")

    if string.find("credits", len(string) - 8) != -1:
        string = string.replace("credits", "")

    if string.find("is strongly recommended", len(string) - 23) != -1:
        string = string.replace("is strongly recommended", "")

    if string.find("is recommended", len(string) - 15) != -1:
        string = string.replace("is recommended", "")

    if string.find("including", 0, 10) != -1:
        string = string.replace("including", "")

    if string.find("including", len(string) - 11) != -1:
        string = string.replace("including", "")

    string = string.strip("[.]' ")

    return string


# Splits the prequsite list into a list split by arguments to be passed into graph
def prereqSplitter(prereqListString: list) -> list:
    if (len(prereqListString) > 0):  # Checks if list empty
        prereqString = prereqListString[0]
        prereqList = []
        matched = re.match("^[0-9]?[0-9]\.[0-9][0-9] +credits$", prereqString)  # check if base case of XX.XX credits
        if (matched):
            prereqList.append(prereqString[
                              matched.start():matched.end() - 7].strip())  # append the numbers at the start of the string to pre reqs
            return prereqList
        matched = re.search("^[0-9]?[0-9]\.[0-9][0-9] +credits +including",
                            prereqString)  # check secondary case of XX.XX credits including
        if (matched):
            prereqList.append(prereqString[
                              matched.start():matched.end() - 18].strip())  # append the numbers at the start of the string and process the remaing portion
            prereqString = prereqString[matched.end():]
        prereqBracketMatch = re.findall('\((.*?)\)', prereqString)  # get list of all strings contained inside brackets
        prereqListProcess = re.split("[\(\)]", prereqString)  # get list of the string seperated by brackets

        for string in prereqListProcess:  # runs for each string
            if string in prereqBracketMatch:  # checks if current string is inside bracke
                string = string.strip()
                matched = re.search("^[1-9] +of", string)
                if (matched):
                    string = string[matched.end():]  # remove X of from string
                # print('stringraw', string)
                newString = re.split(r' or |,| and ', string)  # split string by all possible delimeters
                # print('string', newString)
                for x in range(len(newString)):
                    newString[x] = stringClean(newString[x])  # removes common pre/post fixes from string
                if newString != ['']:
                    if len(prereqList) > 0 and prereqList[0][len(prereqList[
                                                                     0]) - 1] == "":  # checks if previous string ended in a space and if so join the current list to said string
                        prereqList[0][len(prereqList[0]) - 1] = newString
                    else:
                        prereqList.append(newString)

            else:  # runs if string not in brackets
                matched = re.search("^[1-9] +of", string)  # check if case X of
                if (matched):
                    string = string[matched.end():]
                    string = re.split(r' or |,| and ', string)  # split string by all possible delimeters
                    for x in range(len(string)):
                        string[x] = stringClean(string[x])  # removes common pre/post fixes from strings
                    if string != ['']:
                        prereqList.append(string)
                else:
                    string = string.split(",| and ")  # loop through string based on ands/ commas
                    for sub in string:
                        sub = sub.split(" or ")  # splits by or
                        for x in range(len(sub)):
                            sub[x] = stringClean(sub[x])  # removes common pre/post fixes from strings
                        if sub != ['']:
                            if len(sub) > 1 and sub[0] == "":  # add elements to previous sub if first element is "".
                                if len(prereqList) > 0:
                                    del sub[0]
                                    prereqList[len(prereqList) - 1].extend(sub)
                                else:
                                    del sub[0]
                                    prereqList.append(sub)
                            else:
                                prereqList.append(sub)
        course_weight = 0
        if (
                len(prereqList) > 0):  # converts course weight into a float. In some cases its stored as string or string in list.
            if (isinstance(prereqList[0], str) and try_float(prereqList[0])):
                course_weight = float(prereqList[0])
            elif (isinstance(prereqList[0], list) and try_float(prereqList[0][0])):
                course_weight = float(prereqList[0][0])

        if course_weight != 0:  # reduce course weight by other courses in list
            for x in prereqList:
                flag = False
                for y in x:
                    if isinstance(y, str) and re.match("^[A-Z]{3,4}[/*][0-9]{4}",
                                                       y):  # checks if the string contains a valid course
                        flag = True
                if flag and course_weight >= 1:
                    course_weight = course_weight - 0.5  # reduces course weight by 0.5
            prereqList[0] = str(course_weight)  # puts course weight back into string

        return prereqList
    # is never reached // This is reached if the list is empty
    else:
        return prereqListString


def listToPrereqs(courses: list) -> list:
    """"
    convert list of courses to dictionairy of coursenames to prerequisites
    """
    for index in range(len(courses)):
        courses[index]["prereqs"] = prereqSplitter(courses[index]["prereqs"])
    return courses


def findCourse(courseList: list, subject: str, courseNum: int) -> dict:
    # finds course dict from list
    courses = filter_course_arr(courseList, 'subject', subject)
    temp = filter_course_arr(courses, 'course_num', courseNum)

    if len(temp) > 1:
        raise ValueError('Course code is not unique')
    elif len(temp) == 0:
        raise ValueError('No Course Found')
    else:
        return temp[0]


# Takes a major's name and creates a set of it's required courses
def getMajors(fileIn: str, majorCode: str, degreeName=None) -> dict:
    f = open(fileIn)
    jsonString = f.read()
    jsonData = json.loads(jsonString)
    f.close()

    majorDict = {}
    for major in jsonData:

        try:
            majorName = major['majorName']
            code = str(re.match(r'^.*\((.*)\).*$', majorName).group(1))
            if code == majorCode:
                majorDict = major
            if degreeName:
                if not majorDict['degreeCode'] == degreeName:
                    return None
        except AttributeError:
            pass
        except KeyError:
            pass
    return majorDict


def getMajorsV2(fileIn: str, args) -> list:
    f = open(fileIn)
    jsonString = f.read()
    jsonData = json.loads(jsonString)
    f.close()

    majorDict = []
    for major in jsonData:
        if "majorCode" in args.keys() and "degreeCode" in args.keys():
            if args['majorCode'] == major['majorCode'] and args['degreeCode'] == major['degreeCode']:
                majorDict.append(major)
        elif "majorCode" in args.keys() and args['majorCode'] == major['majorCode']:
            majorDict.append(major)
        elif "degreeCode" in args.keys() and args['degreeCode'] == major['degreeCode']:
            majorDict.append(major)
    return majorDict


def filter_course_prereqs(courses, prereqs, value):
    res = []
    for course in courses:
        if "prereqs" in course.keys():
            dictionary = course.get('prereqs')
            if type(dictionary) == type({}) and "options" in dictionary.keys():
                for c in dictionary.get('options'):
                    if value == c:
                        res.append(c)

    return res
