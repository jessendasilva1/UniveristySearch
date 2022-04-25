# global modules

import os
import argparse
import subprocess
from platform import system
import sys

sys.path.append(os.path.normpath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphing', 'util')))

import search
import course
import makeGraph
import majorGraph



IS_WINDOWS_HOST = system() == 'Windows'
IS_LINUX_HOST = system() == 'Linux'
IS_MAC_HOST = system() == 'Darwin'


ROOT_ABS_PATH = os.path.abspath('.')

# Primary Execution file wrappers

# Relative directories
GENERATED_FILES_ABS_DIR = os.path.join('graphing', 'generated')
SCRAPER_EXECUTABLE_ABS_DIR = os.path.join('graphing', 'scraper')
UTILITY_EXECUTABLE_ABS_DIR = os.path.join('graphing', 'util')
PARSER_EXECUTABLE_ABS_DIR = os.path.join(UTILITY_EXECUTABLE_ABS_DIR, 'parser')

# PROGRAM EXECUTABLE FILES
GUELPH_COURSE_SCRAPER = os.path.join(ROOT_ABS_PATH, SCRAPER_EXECUTABLE_ABS_DIR, 'index.js')
GUELPH_MAJOR_SCRAPER = os.path.join(ROOT_ABS_PATH, SCRAPER_EXECUTABLE_ABS_DIR, 'majorScrape.js')
OTTAWA_COURSE_SCRAPER = os.path.join(ROOT_ABS_PATH, SCRAPER_EXECUTABLE_ABS_DIR, 'ottawaScrape.js')

GUELPH_COURSE_PARSER = os.path.join(ROOT_ABS_PATH, PARSER_EXECUTABLE_ABS_DIR, 'guelphCourseParser.py')
OTTAWA_COURSE_PARSER = os.path.join(ROOT_ABS_PATH, PARSER_EXECUTABLE_ABS_DIR, 'ottawaCourseParser.py')

# Subject Data File
GUELPH_SUBECTS_DATA_JSON = os.path.join(ROOT_ABS_PATH, GENERATED_FILES_ABS_DIR,'guelphSubjects.json')

# Course data Files
GUELPH_COURSE_DATA_TXT = os.path.join(ROOT_ABS_PATH, GENERATED_FILES_ABS_DIR,'courseData.txt')
GUELPH_COURSE_DATA_JSON = os.path.join(ROOT_ABS_PATH, GENERATED_FILES_ABS_DIR,'courseData.json')

OTTAWA_RAW_COURSE_DATA_JSON = os.path.join(
        ROOT_ABS_PATH, GENERATED_FILES_ABS_DIR,'degreeProgramCoursesOttawa.json')

OTTAWA_PARSED_COURSE_DATA_JSON = os.path.join(
        ROOT_ABS_PATH, GENERATED_FILES_ABS_DIR,'uOttawaCourseData.json')

# Guelph Major data files
GUELPH_PROGRAM_LIST_JSON = os.path.join(ROOT_ABS_PATH, GENERATED_FILES_ABS_DIR,'degreeProgramsList.json')

GUELPH_PROGRAM_LINKS_JSON = os.path.join(ROOT_ABS_PATH, GENERATED_FILES_ABS_DIR,'degreeProgramRequirementsLinks.json')

GUELPH_MAJOR_COURSE_DATA_JSON = os.path.join(
        ROOT_ABS_PATH, GENERATED_FILES_ABS_DIR,'degreeProgramCourses.json')


GENERATED_FILES_LIST = [
            GUELPH_COURSE_DATA_TXT,
            GUELPH_COURSE_DATA_JSON,
            GUELPH_SUBECTS_DATA_JSON,
            OTTAWA_RAW_COURSE_DATA_JSON,
            OTTAWA_PARSED_COURSE_DATA_JSON,
            GUELPH_PROGRAM_LIST_JSON,
            GUELPH_PROGRAM_LINKS_JSON,
            GUELPH_MAJOR_COURSE_DATA_JSON
]

GENERATED_GUELPH_COURSE_FILES_LIST = [
            GUELPH_SUBECTS_DATA_JSON,
            GUELPH_COURSE_DATA_TXT,
            GUELPH_COURSE_DATA_JSON,
]

GENERATED_GUELPH_MAJOR_FILES_LIST = [
            GUELPH_PROGRAM_LIST_JSON,
            GUELPH_PROGRAM_LINKS_JSON,
            GUELPH_MAJOR_COURSE_DATA_JSON
]

GENERATED_OTTAWA_COURSE_DATA_LIST = [
            OTTAWA_RAW_COURSE_DATA_JSON,
            OTTAWA_PARSED_COURSE_DATA_JSON
]



def checkFileExists(fileName : str) -> bool:
    if not fileName:
        return False
    return os.path.isfile(fileName)

def deleteFile(fileName : str) -> None:
    if checkFileExists(fileName):
        os.remove(fileName)

def rebuildAllGuelphFiles(deleteFiles=True):
    rebuildGuelphCourseFiles(deleteFiles)
    rebuildGuelphMajorFiles(deleteFiles)

def rebuildAllOttawaFiles(deleteFiles=True):
    rebuildOttawaCourseFiles(deleteFiles)


def rebuildAllGeneratedFiles():

    for file in GENERATED_FILES_LIST:
        deleteFile(file)

    rebuildGuelphCourseFiles()

    rebuildGuelphMajorFiles()

    rebuildOttawaCourseFiles()


def rebuildGuelphCourseFiles(deleteFiles=True):
    if deleteFiles:
        for file in GENERATED_GUELPH_COURSE_FILES_LIST:
            deleteFile(file)
        scraperResult = runNodeCommand([GUELPH_COURSE_SCRAPER, GUELPH_COURSE_DATA_TXT, GUELPH_SUBECTS_DATA_JSON])
        if not scraperResult == 0:
            raise RuntimeError('An Error has occured when running {}.'.format(GUELPH_COURSE_SCRAPER))
    
    commandList = [ GUELPH_COURSE_PARSER, 
            GUELPH_COURSE_DATA_TXT, 
            GUELPH_SUBECTS_DATA_JSON, 
            GUELPH_COURSE_DATA_JSON]

    parserResult = runPythonCommand(commandList)
    if not parserResult == 0:
        raise RuntimeError('An Error has occured when running {}.'.format(GUELPH_COURSE_PARSER))


def rebuildGuelphMajorFiles(deleteFiles=True):
    if deleteFiles:
        for file in GENERATED_GUELPH_MAJOR_FILES_LIST:
            deleteFile(file)
        
        commandList = [ GUELPH_MAJOR_SCRAPER, GUELPH_PROGRAM_LIST_JSON, GUELPH_PROGRAM_LINKS_JSON, GUELPH_MAJOR_COURSE_DATA_JSON]
        scraperResult = runNodeCommand(commandList)
        if not scraperResult == 0:
            raise RuntimeError('An Error has occured when running {}.'.format(GUELPH_MAJOR_SCRAPER))

    parserResult = runPythonCommand([GUELPH_COURSE_PARSER, 
            GUELPH_COURSE_DATA_TXT, GUELPH_SUBECTS_DATA_JSON, GUELPH_COURSE_DATA_JSON])
    if not parserResult == 0:
        raise RuntimeError('An Error has occured when running {}.'.format(GUELPH_COURSE_PARSER))

def rebuildOttawaCourseFiles(deleteFiles=True):
    if deleteFiles:
        for file in GENERATED_OTTAWA_COURSE_DATA_LIST:
            deleteFile(file)

    scraperResult = runNodeCommand([OTTAWA_COURSE_SCRAPER, OTTAWA_RAW_COURSE_DATA_JSON])

    if not scraperResult == 0:
        raise RuntimeError('An Error has occured when running {}.'.format(OTTAWA_COURSE_SCRAPER))

    commandList = [ OTTAWA_COURSE_PARSER, OTTAWA_RAW_COURSE_DATA_JSON, OTTAWA_PARSED_COURSE_DATA_JSON]

    parserResult = runPythonCommand(commandList)
    if not parserResult == 0:
        raise RuntimeError('An Error has occured when running {}.'.format(OTTAWA_COURSE_PARSER))


def runPythonCommand(commandList : list) -> int:
    if IS_WINDOWS_HOST:
        commandList.insert(0, 'python')
    # elif IS_LINUX_HOST or IS_MAC_HOST:
    #     commandList.insert(0, 'python3')
    else:
        commandList.insert(0, 'python3')
    return runCommand(commandList)

def runNodeCommand(commandList : list) -> int:
    if IS_WINDOWS_HOST:
        commandList.insert(0, 'node')
    # elif IS_LINUX_HOST or IS_MAC_HOST:
    #     commandList.insert(0, 'node')
    else:
        commandList.insert(0, 'node')
    return runCommand(commandList)

def runCommand(commandList) -> int:
    print('Executing: {}'.format(' '.join(commandList)))
    result = subprocess.run(commandList)
    return result.returncode

def validateScraperDependancies() -> bool:
    return True


def rebuildDataFiles(parser, args):
    if args.all:
        if args.guelph:
            rebuildAllGuelphFiles()
        elif args.ottawa:
            rebuildAllOttawaFiles()
        else:
            rebuildAllGeneratedFiles()
    elif args.course:
        if args.guelph:
            rebuildGuelphCourseFiles()
        elif args.ottawa:
            rebuildOttawaCourseFiles()
        else:
           rebuildGuelphCourseFiles()
           rebuildOttawaCourseFiles()
    elif args.major:
        if args.guelph:
            rebuildGuelphMajorFiles()
        # Ottawa has no Major Files
        elif args.ottawa:
            pass
        else:
            rebuildGuelphMajorFiles()
    else:
        print('Must select one of the following: -a, -c, -m. Usage: `courseUtility.py rebuild -h` for help.')
    

def searchCourses(parser, args):
    search.search(parser, args, GUELPH_COURSE_DATA_JSON)

def displayCourses(parser, args):
    course.course(args, GUELPH_COURSE_DATA_JSON)


def graphCourses(parser, args):
    if args.out:
        fileOut = args.out
    else:
        if args.subject:
            fileOut = '{}_graph.pdf'.format(args.subject)
        else:
            fileOut = 'all_graph.pdf'

    if args.majors:
        if args.isOttawa:
            print('Graphing Ottawa Majors is not supported.')
            return
        else:
            courseFileIn = GUELPH_COURSE_DATA_JSON
            majorFileIn = GUELPH_MAJOR_COURSE_DATA_JSON
        majorGraph.majorGraph(parser, args, courseFileIn, majorFileIn, fileOut)
    else:
        if args.isOttawa:
            courseFileIn = OTTAWA_PARSED_COURSE_DATA_JSON
            
        else:
            courseFileIn = GUELPH_COURSE_DATA_JSON
        
        makeGraph.makeGraph(parser, args, courseFileIn, fileOut)
    

if __name__ == "__main__":
   
    if not IS_LINUX_HOST and not IS_WINDOWS_HOST and not IS_MAC_HOST:
        print("WARNING: Unrecongized Host OS. Assuming Linux-based.")


    parser = argparse.ArgumentParser(description='Uility to Graph Course Data')
    

    subParser = parser.add_subparsers(title='Utilities', description='Course display utilities')

    scraperParser = subParser.add_parser('rebuild')

    rebuildGroup = scraperParser.add_mutually_exclusive_group()

    rebuildGroup.add_argument('-a', '--all', action='store_true',  help='Rebuild all Data files')
    rebuildGroup.add_argument('-c', '--course', action='store_true',  help='Rebuild Course Data files')
    rebuildGroup.add_argument('-m', '--major', action='store_true', help='Rebuild Major Data files')

    SchoolGroup = scraperParser.add_mutually_exclusive_group()
    SchoolGroup.add_argument('-g', '--guelph', action='store_true',  help='Rebuild Guelph Data files')
    SchoolGroup.add_argument('-o', '--ottawa', action='store_true', help='Rebuild Ottawa Data files')
    scraperParser.set_defaults(func=rebuildDataFiles)

    searchParser = subParser.add_parser('search')
    searchParser.add_argument('-s', '--subject', type=str, help='The course subject')
    searchParser.add_argument('-n', '--number', type=int, help='The course number')
    searchParser.add_argument('-N', '--name', nargs='+', help="Name of the course")
    searchParser.add_argument('-c', '--credit', type=float, help='Credit weighting of the course')
    searchParser.add_argument('-S', '--summer', action='store_true', help='Course is offered in summer')
    searchParser.add_argument('-F', '--fall', action='store_true', help='Course is offered in fall')
    searchParser.add_argument('-W', '--winter', action='store_true', help='Course is offered in winter')
    searchParser.add_argument('-l', '--lecture', type=int, help='Number of lectures per week')
    searchParser.add_argument('-lab', '--lab', type=int, help='Number of labs per week')
    searchParser.add_argument('-loc', '--location', help="The location of the course")
    searchParser.add_argument('-d', '--dept', nargs='+', help="The department which offers the course")

    searchParser.set_defaults(func=searchCourses)

    
    courseParser = subParser.add_parser('course')
    courseParser.add_argument('subject', type=str, help='The course subject. ie. CIS')
    courseParser.add_argument('number', type=int, help='The course number. ie. 3760')
    courseParser.set_defaults(func=displayCourses)
    

    graphParser = subParser.add_parser('graph')
    graphParser.add_argument(
            '-M',
            '--majors',
            action='store_true',
            default=False,
            help = 'Flag for graphing majors.')

    graphParser.add_argument(
            '-O',
            '--isOttawa',
            action='store_true',
            default=False,
            help='Flag for University of Ottawa course data.')

    graphParser.add_argument(
            '-s', '--subject', type=str, help='The course subject or major code. ie. CIS')
    graphParser.add_argument('-n', '--number', type=int, help='The course number. ie. 3760')
    graphParser.add_argument('dropped', type=str, nargs='*', default=None, help='Dropped Coureses for path highlighting')
    graphParser.add_argument('-o', '--out', help='specify output file')
    graphParser.set_defaults(func=graphCourses)


    args = parser.parse_args()
    if args == argparse.Namespace():
        parser.error("Must select one of: course, search, graph")
    else:
        try:
            args.func(parser, args)
        except FileNotFoundError:
            print('Missing Files. Please Generate. Usage: courseUtility.py rebuild -a')
        except RuntimeError as e:
            print(str(e))


    # try:
    #     rebuildGuelphMajorFiles(deleteFiles=False)
    # except RuntimeError:
    #     pass