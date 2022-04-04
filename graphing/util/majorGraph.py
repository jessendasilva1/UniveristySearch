# CLI for creating graph of a major

import argparse
import course_util
import graph
import generate_pdf
from pathlib import Path


def majorGraph(parser, args, courseFileIn: str, majorFileIn: str, fileOut: str):
    args = parser.parse_args()
    if not args.subject:
        parser.error('major cannot be empty')
    # if not args.degreeCode:
    #     parser.error('degree cannot be empty')

    # check if files exist
    courseCheck = Path(courseFileIn)
    majorCheck = Path(majorFileIn)

    if not courseCheck.is_file():
        parser.error('Courses must be parsed')
        # maybe add script to parse instead of error
    if not majorCheck.is_file():
        parser.error('Majors must be parsed')
        # maybe add script to parse instead of error

    # get all courses from utility function course_util
    results = course_util.get_courses(courseFileIn)

    # Creates a set of the courses within the searched major
    majorDict = course_util.getMajors(majorFileIn, args.subject)

    if not majorDict:
        print('No major was found')
        return

    # uses major dict to create a graph
    graph.generateMajorGraph(courseFileIn, '{}.dot'.format(fileOut), majorDict)

    try:
        generate_pdf.pdfView('{}.dot'.format(fileOut), fileOut)  # attempt to create pdf from .dot
        graphCheck = True
    except PermissionError:
        print('ERROR: Failed to write to File')

    if not graphCheck:
        if len(results) < 1:
            print('No major was found')  # no course found


def majorGraphV2(args, majorFileIn: str):
    majorDict = course_util.getMajorsV2(majorFileIn, args)

    if len(majorDict) == 0:
        return "{msg: No major found}"

    return majorDict
