import json
def validateGuelph(file):
    f = open(file, mode='r')
    jsonString = f.read()
    jsonData = json.loads(jsonString)
    f.close()

    keys = ['subject', 'course_num', 'course_name', 'is_offered_fall', 'is_offered_winter', 'is_offered_summer',
            'lectures', 'labs',
            'credits', 'description', 'offering', 'unknown', 'prereqs', 'co_reqs', 'equates', 'restrictions', 'dept',
            'location']
    for course in jsonData:
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
    return True

def validateOttawa(file):
    f = open(file, mode='r')
    jsonString = f.read()
    jsonData = json.loads(jsonString)
    f.close()

    keys = ['subject', 'course_num', 'course_name', 'is_offered_fall', 'is_offered_winter', 'is_offered_summer',
            'lectures', 'labs',
            'credits', 'description', 'offering', 'unknown', 'prereqs', 'co_reqs', 'equates', 'restrictions', 'dept',
            'location']
    for course in jsonData:
        for i in range(len(keys)):  # Check that all required keys are present
            if not keys[i] in course:
                return False
        for key in course:
            if key == 'subject' or key == 'course_name' or key == 'description':
                if not (isinstance(course.get(key), str)):  # Check correct str values
                    return False
            elif key == 'lectures' or key == 'labs':
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
            elif key == 'course_num' or key == 'credits':
                if not (isinstance(course.get(key), int) or isinstance(course.get(key), str)):  # Check correct num values
                    return False

    return True

def validateProgram(file):
    f = open(file, mode='r')
    jsonString = f.read()
    jsonData = json.loads(jsonString)
    f.close()

    keys = ['degreeName', 'degreeCode', 'majorName', 'majorCode', 'requiredCourses', 'totalRequiredWeight',
            'totalElectiveWeight', 'electives']
    for program in jsonData:
        for i in range(len(keys)):  # Check that all required keys are present
            if not keys[i] in program:
                return False
        for key in program:
            if key == 'degreeName' or key == 'degreeCode' or key == 'majorName' or key == 'majorCode':
                if not (isinstance(program.get(key), str)):  # Check correct str values
                    return False
            elif key == 'requiredCourses' or 'electives':
               if isinstance(program.get(key), list):
                    if program.get(key) is None:  # Check if list is none
                        return False
            elif key == 'totalRequiredWeight' or key == 'totalElectiveWeight':
                if not (isinstance(program.get(key), int)):  # Check correct int values
                    return False
    return True

        
if __name__ == "__main__":
    with open('results.txt', 'r+') as f:
        f.truncate(0)
    f.close()
    g = 0
    o = 0
    p = 0
    if (validateGuelph('graphing/generated/courseData.json')): #run guelph course test
        g = 1
    if (validateOttawa('graphing/generated/uOttawaCourseData.json')): #run ottawa course test
        o = 1
    if(validateProgram('graphing/generated/degreeProgramCourses.json')): #run programs test
        p = 1
    
    #takes the json output from jessen's GUI testing and gets the output
    with open('graphing/scraper/test/test-results.json', 'r') as file:
        jsonString = file.read()
        jsonData = json.loads(jsonString)

        for i in jsonData['suites']:
            for j in i['suites']:
                for k in j['specs']:
                    for l in k['tests']:
                        for key in l:
                            if key == 'status':
                                if l.get(key) != "expected":
                                    with open('results.txt', 'a') as f:
                                        f.write("FRONTEND Test ")
                                        f.write(k.get('title'))
                                        f.write(': Fail\n')
    file.close()

    with open('results.txt', 'a') as file:
        #only writes to file if a test failed
        #this allows the email to only send if something goes wrong
        if g == 0:
            file.write("BACKEND Test #1 Guelph Course: Fail")
            file.write('\n')
        if o == 0:
            file.write("BACKEND Test #2 Ottawa Course: Fail")
            file.write('\n')
        if p == 0:
            file.write("BACKEND Test #3 Program: Fail")
            file.write('\n')
