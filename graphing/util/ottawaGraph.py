import argparse
import course_util
import graph
import generate_pdf
from pathlib import Path

if __name__ == '__main__':
    ottawaFile = './ottawaData.json'

    parser = argparse.ArgumentParser(description='Search for courseses to make a Graph')
    #check if files exist
    ottawaCheck = Path(ottawaFile)

    if not ottawaCheck.is_file():
        parser.error('Courses must be parsed')
        #maybe add script to parse instead of error

    #This gets every course from the ottawa json file
    allCourses = course_util.get_courses(ottawaFile)

    #A set to hold each subject offered at uOttawa
    uniqueSubjects = set()
    for course in allCourses:
        #Set properties state that each item is unique
        uniqueSubjects.add(course['subject'])

    rootList = list()
    for subject in uniqueSubjects:
        graph.newGraphMake(subject)
    generate_pdf.ottawaView("filename")