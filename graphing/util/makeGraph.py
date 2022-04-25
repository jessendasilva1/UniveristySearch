# CLI for searching for courses
# Command line interface to search courses

import argparse
import course_util
import graph
import generate_pdf

def makeGraph(parser, args, fileIn : str, fileOut : str):

    if not args.subject and not args.isOttawa:
        parser.error('course subject cannot be empty')
    if args.number and int(args.number) == 0:
        parser.error('course number must be a 4 digit number')

    # get all courses from utility function course_util
    results = course_util.get_courses(fileIn)

    courseNum = None
    # Ordered by search priority
    if args.subject:
        if args.subject == "":
            parser.error('subject cannot be empty')  # subject name cannot be empty
        tempArr = course_util.filter_course_arr(results, 'subject', args.subject)
        results = tempArr
    if args.number:  # course number
        tempArr = course_util.filter_course_arr(results, 'course_num', args.number)
        results = tempArr
        courseNum = args.number

    if len(results) < 1:
            print('No course was found')  # no course found
            return

    
    graph.newGraphMake(fileIn, '{}.dot'.format(fileOut), args.subject, courseNum, args.isOttawa)

    try:
        if args.isOttawa:
            generate_pdf.ottawaView('{}.dot'.format(fileOut), fileOut)
        else:
            generate_pdf.pdfView('{}.dot'.format(fileOut), fileOut) #attempt to create pdf from .dot
        graphCheck = True
    except PermissionError:
        print('ERROR: Failed to write to File')
        
