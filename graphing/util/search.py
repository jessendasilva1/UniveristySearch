# CLI for searching for courses
# Command line interface to search courses

import course_util
import subject_util
import graph


def search(parser, args, fileIn: str):
    # convert lists to string
    if args.name and len(args.name) > 0:
        args.name = "".join(args.name)
    if args.dept and len(args.dept) > 0:
        args.dept = "".join(args.dept)
    if args.location and len(args.location) > 0:
        args.location = "".join(args.location)

    # get all courses from utility function course_util
    results = course_util.get_courses(fileIn)

    # Ordered by search priority
    if args.name:
        if args.name == "":
            parser.error('name cannot be empty')  # course name cannot be empty
        tempArr = course_util.filter_course_arr(results, 'course_name', args.name)
        results = tempArr
    if args.subject:
        if args.subject == "":
            parser.error('subject cannot be empty')  # subject name cannot be empty
        tempArr = course_util.filter_course_arr(results, 'subject', args.subject)
        results = tempArr
    if args.number:  # course number
        tempArr = course_util.filter_course_arr(results, 'course_num', args.number)
        results = tempArr
    if args.credit:  # credit
        tempArr = course_util.filter_course_arr(results, 'credits', args.credit)
        results = tempArr
    if args.summer:  # offered in summer
        tempArr = course_util.filter_course_arr(results, 'is_offered_summer', args.summer)
        results = tempArr
    if args.fall:  # offered in fall
        tempArr = course_util.filter_course_arr(results, 'is_offered_fall', args.fall)
        results = tempArr
    if args.winter:  # offered in winter
        tempArr = course_util.filter_course_arr(results, 'is_offered_winter', args.winter)
        results = tempArr
    if args.dept:  # department
        if args.dept.strip() == "":
            parser.error('name cannot be empty')
        tempArr = course_util.filter_course_arr(results, 'dept', args.dept)
        results = tempArr
    if args.lecture:  # lectures
        tempArr = course_util.filter_course_arr(results, 'lectures', args.lecture)
        results = tempArr
    if args.lab:  # labs
        tempArr = course_util.filter_course_arr(results, 'labs', args.lab)
        results = tempArr
    if args.location:
        if args.location.strip() == "":
            parser.error('location cannot be empty')  # location cannot be empty
        tempArr = course_util.filter_course_arr(results, 'location', args.location)
        results = tempArr

    if len(results) < 1:
        print('No course was found')  # no course found
    else:
        course_util.print_search_results(results)  # else print search results


def searchV2(args, fileIn: str):
    results = course_util.get_courses(fileIn)

    # Ordered by search priority
    if "name" in args.keys():
        tempArr = course_util.filter_course_arr(results, 'course_name', args['name'])
        results = tempArr
    if "subject" in args.keys():
        tempArr = course_util.filter_course_arr(results, 'subject', args['subject'])
        results = tempArr
    if "course_num" in args.keys():  # course number
        tempArr = course_util.filter_course_arr(results, 'course_num', args['course_num'])
        results = tempArr
    if "credits" in args.keys():  # credit
        tempArr = course_util.filter_course_arr(results, 'credits', args['credits'])
        results = tempArr
    if "is_offered_summer" in args.keys():  # offered in summer
        tempArr = course_util.filter_course_arr(results, 'is_offered_summer',
                                                True if args['is_offered_summer'] == 'true' else False)
        results = tempArr
    if "is_offered_fall" in args.keys():  # offered in fall
        tempArr = course_util.filter_course_arr(results, 'is_offered_fall',
                                                True if args['is_offered_fall'] == 'true' else False)
        results = tempArr
    if "is_offered_winter" in args.keys():  # offered in winter
        tempArr = course_util.filter_course_arr(results, 'is_offered_winter',
                                                True if args['is_offered_winter'] == 'true' else False)
        results = tempArr
    if "dept" in args.keys():  # department
        tempArr = course_util.filter_course_arr(results, 'dept', args['dept'])
        results = tempArr
    if "lectures" in args.keys():  # lectures
        tempArr = course_util.filter_course_arr(results, 'lectures', args['lectures'])
        results = tempArr
    if "labs" in args.keys():  # labs
        tempArr = course_util.filter_course_arr(results, 'labs', args['labs'])
        results = tempArr
    if "location" in args.keys():
        tempArr = course_util.filter_course_arr(results, 'location', args['location'])
        results = tempArr
    if "prereqs" in args.keys():
        tempArr = course_util.filter_course_prereqs(results, 'prereqs', args['prepreqs'])
        results = tempArr

    return results


def searchAllSubjects(is_ottawa: str, is_guelph: str):
    l = []
    res = subject_util.getAllSubjects(is_ottawa, is_guelph)

    for sub in res:
        l.append(sub.toString())

    return l


def searchAllMajorSubjects(is_ottawa: str, is_guelph: str):
    l = []
    res = subject_util.getAllMajorSubjects(is_ottawa, is_guelph)

    for sub in res:
        l.append(sub.toString())

    return l


def getJSONGraph(is_ottawa: str, is_guelph: str, subject: str, blocked, courseNum=None):

    if is_ottawa == 'true':
        return graph.newGraphMake('graphing/generated/uOttawaCourseData.json', '', subject, courseNum, True, blocked)
    elif is_guelph == 'true':
        return graph.newGraphMake('graphing/generated/courseData.json', '', subject, courseNum, False, blocked)
        


def getJSONMajorGraph(is_ottawa: str, is_guelph: str, major_code: str):

    if is_guelph == 'true':
        requiredCourses = course_util.getMajorsV2('graphing/generated/degreeProgramCourses.json', {'majorCode': major_code})
        result = requiredCourses[0]
        return graph.generateMajorGraphToJSON('graphing/generated/courseData.json', result, is_ottawa, is_guelph)

    if is_ottawa == 'true':
        return graph.getGraphJSON('graphing/generated/courseData.json', major_code, is_ottawa, is_guelph)

