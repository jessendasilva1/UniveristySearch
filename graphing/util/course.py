# CLI for displaying the complete information about a course
# Script for command line interface to run queries for course information

# imports
import argparse
import course_util

def course(args, fileIn : str):
    
    # get all courses in array
    coursesArr = course_util.get_courses(fileIn)

    # find course
    result = course_util.filter_course_arr(coursesArr, 'subject', args.subject)
    tempArr = course_util.filter_course_arr(result, 'course_num', args.number)
    result = tempArr
    
    # course codes should always be unique
    if len(result) > 1:
        print('ERROR: Course Code is not unique')
    elif len(result) < 1:         # if no such course found
        print('The course {} {} was not found.'.format(args.subject, args.number))
    else:                       # display course information
        print(course_util.courseToString(result[0]))
