import json
import os
import re
import sys

# The below line is only needed when course_util is in a parent directory
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import course_util


#
# Style Class for Edges
# Attach to each tuple of edges in the graph object
#
class EdgeStyle:
    def __init__(self, style=None, colour=None, shape=None, 
                label=None, isManditory=False, id=-1, isBlocked=False):
        self.style = style
        self.colour = colour
        self.shape = shape
        self.label = label
        self.id = id
        self.isManditory = isManditory
        self.isBlocked = isBlocked

    def __copy__(self):
        return EdgeStyle(style=self.style, colour=self.colour, shape=self.shape, label=self.label, isManditory=self.isManditory, id=self.id)

    def getLabel(self):
        return "{}".format(self.label)

    def getStyle(self):
        return "{}".format(self.style)

    def toD3JSDict(self):
        return {
            'required': self.isManditory,
            'label': self.label,
            'isBlocked': self.isBlocked
        }

    def toString(self):
        edgeStyleStr = '['
        if self.style:
            edgeStyleStr += 'style="{}",'.format(self.style)
        if self.colour:
            edgeStyleStr += 'color="{}",'.format(self.colour)
        if self.shape:
            edgeStyleStr += 'shape="{}",'.format(self.shape)
        if self.label:
            edgeStyleStr += 'label="{}",'.format(self.label)

        if len(edgeStyleStr) > 1:
            return edgeStyleStr[:-1] + ']'
        else:
            return ''


#
# Style class for nodes
# attach to each node object
#
class NodeStyle:

    def __init__(self, style=None, shape=None, colour=None, fillColour=None, label=None, id=-1):
        self.style = style
        self.shape = shape
        self.colour = colour
        self.fillColour = fillColour
        self.label = label
        self.id = id

    def __copy__(self):
        return NodeStyle(style=self.style, shape=self.shape,
                         colour=self.colour, fillColour=self.fillColour, label=self.label, id=self.id)

    def getId(self) -> int:
        return self.id

    def toString(self):
        nodeStyleStr = '['

        if self.style:
            nodeStyleStr += 'style="{}",'.format(self.style)
        if self.shape:
            nodeStyleStr += 'shape="{}",'.format(self.shape)
        if self.colour:
            nodeStyleStr += 'color="{}",'.format(self.colour)
        if self.fillColour:
            nodeStyleStr += 'fillColour="{}",'.format(self.fillColour)
        if self.label:
            nodeStyleStr += 'label="{}",'.format(self.label)

        if len(nodeStyleStr) > 1:
            return nodeStyleStr[:-1] + ']'
        else:
            return ''
    


class Node:

    def __init__(self, name: str, style: NodeStyle, isBlocked=False):
        if name is None:
            raise TypeError('Invalid name. Node Name cannot be None')
        if name.strip() == "":
            raise ValueError('Invalid name. Node Name cannot be empty')
        self.name = name
        self.style = style
        self.isBlocked = isBlocked

    # Override equal comparison
    def __eq__(self, other) -> bool:
        return self.name == other.name

    # override hash function
    def __hash__(self):
        return hash(self.name)

    def getName(self):
        return self.name

    def toD3JSDict(self):
        return {
            'name': self.name,
            'type_id': self.style.getId(),
            'isBlocked': self.isBlocked
        }

    def toString(self, printStyle=False):
        if self.style.toString() == '' or not printStyle:
            return '"{}"'.format(self.name)
        else:
            return '"{}" {}'.format(self.name, self.style.toString())


class GraphEdge:
    def __init__(self, node : Node, connectingNode : Node, edgeStyle: EdgeStyle):
        if node is None or connectingNode is None:
            raise TypeError('nodes cannot be None')

        self.edge = (node, connectingNode, edgeStyle)

    # Override equal comparison
    def __eq__(self, other) -> bool:
        return self.edge[0] == other.edge[0] and self.edge[1] == other.edge[1]

    # override hash function
    def __hash__(self):
        return hash(hash(self.edge[0]) + hash(self.edge[1]))

    def toD3JSDict(self, is_ottawa):
        return {
            'is_guelph': not is_ottawa,
            'is_ottawa': is_ottawa,
            'src': self.edge[0].toD3JSDict(), 
            'dest': self.edge[1].toD3JSDict(),
            'link': self.edge[2].toD3JSDict()
            }

    # TODO: Add style to toString output so it can be called directly when producing the .DOT txt file?

    def getSrcName(self):
        return self.edge[0].getName()
    
    def getDestName(self):
        return self.edge[1].getName()

    
    def toString(self) -> str:
        return '{} -> {} {}'.format(self.edge[0].toString(), self.edge[1].toString(), self.edge[2].toString())


class GraphStyle:
    def __init__(self, padding=None, rankSep=None, nodeSep=None, splines=None, esep=None, isOttawa=False):
        self.padding = padding
        self.rankSep = rankSep
        self.nodeSep = nodeSep
        self.splines = splines
        self.esep = esep
        self.isOttawa = isOttawa

    def toString(self) -> str:
        styleString = 'graph ['

        if self.padding:
            styleString += 'pad="{}",'.format(self.padding)
        if self.rankSep:
            styleString += 'ranksep="{}",'.format(self.rankSep)
        if self.nodeSep:
            styleString += 'nodesep="{}",'.format(self.nodeSep)
        if self.splines:
            styleString += 'splines="{}",'.format(self.splines)
        if self.esep:
            styleString += 'esep="{}",'.format(self.esep)

        if len(styleString) > 8:
            return styleString[:-1] + ']\n'
        else:
            return ''


class CourseGraph:
    def __init__(self, padding=None, rankSep=None, nodeSep=None, splines=None, esep=None, isOttawa=False):
        self.edges = set()
        self.nodes = set()
        self.style = GraphStyle(padding, rankSep, nodeSep, splines, esep, isOttawa)

    def __iter__(self):
        return iter(self.edges)

    def __len__(self):
        return len(self.edges)
    
    def add(self, newNode: Node, subject: str, courseNum: int, nodeStyle: NodeStyle, edgeStyle: EdgeStyle,
            isOttawa=False) -> None:
        if subject is None:
            raise TypeError('subject cannot be None')
        if courseNum is None:
            raise TypeError('courseNum cannot be None')

        if isOttawa:
            connectingNode = findNode(self.nodes, '{} {}'.format(subject, courseNum))
        else:
            connectingNode = findNode(self.nodes, '{}*{}'.format(subject, courseNum))

        # if connecting node doesn't exist create and add it
        if connectingNode is None:
            if isOttawa:
                connectingNode = Node('{} {}'.format(subject, courseNum), nodeStyle)
            else:
                connectingNode = Node('{}*{}'.format(subject, courseNum), nodeStyle)
            self.nodes.add(connectingNode)

        self.edges.add(GraphEdge(newNode, connectingNode, edgeStyle))

    def remove(self, edge: GraphEdge):
        if edge is None:
            raise TypeError('GraphEdge cannot be None')
        removedEdge = self.edges.remove(edge)
        return removedEdge

    def toD3JSDict(self, is_ottawa):
        d3JSEdgeList = []
        for edge in self.edges:
            d3JSEdgeList.append(edge.toD3JSDict(is_ottawa))
        return d3JSEdgeList

    def toJSON(self, is_ottawa: str, is_guelph: str) -> dict:
        toBeReturned = {}
        for node in self.nodes:
            toBeReturned[node.toJSON()] = []

        for edge in self.edges:
            if edge.getSrc() in toBeReturned.keys():
                toBeReturned[edge.getSrc()].append(edge.toJSON(is_ottawa, is_guelph))

        return toBeReturned

    def toString(self) -> str:
        graphStr = self.style.toString()
        for node in self.nodes:
            graphStr += node.toString(True) + '\n'

        graphStr += '\n'

        for edge in self.edges:
            graphStr += edge.toString() + '\n'
        return graphStr


# Globals
preReqSET_g = set()
nodeStyleIndex = 0
optionalNodeStyleIndex = 0

graph = None
isOneOfMany = False
numOfMany = 0
isCreditNum = False

# for OR condition
optionalNodeStyle = NodeStyle(None, 'ellipse', 'grey', id=1)
optionalNodeStyle2 = NodeStyle(None, 'ellipse', 'purple', id=2)
optionalNodeStyle3 = NodeStyle(None, 'ellipse', 'green', id=3)
optionalNodeStyle4 = NodeStyle(None, 'ellipse', 'yellow', id=4)
optionalNodeStyle5 = NodeStyle(None, 'ellipse', 'crimson', id=5)
optionalNodeStyle6 = NodeStyle(None, 'ellipse', 'cyan', id=6)
optionalNodeStyle7 = NodeStyle(None, 'ellipse', 'hotpink', id=7)
optionalNodeStyle8 = NodeStyle(None, 'ellipse', 'red', id=8)
optionalNodeStyle9 = NodeStyle(None, 'ellipse', 'moccasin', id=9)
optionalNodeStyle10 = NodeStyle(None, 'ellipse', 'black', id=10)
optionalNodeStyle11 = NodeStyle(None, 'ellipse', 'khaki', id=11)
optionalNodeStyle12 = NodeStyle(None, 'ellipse', 'Sienna', id=12)
optionalNodeStyle13 = NodeStyle(None, 'ellipse', 'orange', id=13)

optionalNodeStyleList = [
    optionalNodeStyle, optionalNodeStyle2, optionalNodeStyle3, optionalNodeStyle4,
    optionalNodeStyle5, optionalNodeStyle6, optionalNodeStyle7, optionalNodeStyle8,
    optionalNodeStyle9, optionalNodeStyle10, optionalNodeStyle11, optionalNodeStyle12,
    optionalNodeStyle13
]

optionalNodeDiamondStyleList = []


def setOptionalNodeDiamondStyleList(shape: str):
    global optionalNodeStyleList
    global optionalNodeDiamondStyleList

    for item in optionalNodeStyleList:
        newStyle = item.__copy__()
        newStyle.shape = shape
        optionalNodeDiamondStyleList.append(newStyle)


def findNode(nodeSet: set, nodeName: str) -> Node:
    """
    function finds node in graph
    """
    node = next((x for x in nodeSet if x.name == nodeName), None)
    return node

def getPrereqOptions(prereq: dict, prereqSet, isOttawa, pattern):
    if isinstance(prereq, list):
        for item in prereq:
            getPrereqOptions(item, prereqSet, isOttawa, pattern)
    elif isinstance(prereq, str):
        if re.match(pattern, prereq):
            if isOttawa:
                subject, courseNum = re.match(pattern, prereq).group().split(' ')
            else:
                subject, courseNum = re.match(pattern, prereq).group().split('*')
            return ((subject, int(courseNum)))
        else:
            return None
    else:
        for option in prereq['options']:
            if isinstance(option, str):
                    if re.match(pattern, option):
                        if isOttawa:
                            subject, courseNum = re.match(pattern, option).group().split(' ')
                        else:
                            subject, courseNum = re.match(pattern, option).group().split('*')
                        return ((subject, int(courseNum)))
                    else:
                        return None
            else:
                return getPrereqOptions(option, prereqSet, isOttawa, pattern)
                

def getNewCoursePreq(course: dict, isOttawa=False) -> set:
    if isOttawa:
        pattern = re.compile('^\w{3} \d{4}$')
    else:
        pattern = re.compile('^[A-Z]{3}[A-Z]?\*[0-9]{4}$')

    prereqSet = set()
    prereqs = course['prereqs']

    for prereq in prereqs:
        temp = getPrereqOptions(prereq, prereqSet, isOttawa, pattern)
        if temp is not None:
            prereqSet.add(temp)

    return prereqSet

def getCoursePrereq(course: dict, isOttawa=False) -> set:
    """
    search for a particular subject
    """

    if isOttawa:
        pattern = re.compile('^\w{3} \d{4}$')
    else:
        pattern = re.compile('^[A-Z]{3}[A-Z]?\*[0-9]{4}$')
    prereqSet = set()
    prereqs = course['prereqs']
    for prereq in prereqs:
        # single course code
        if isinstance(prereq, str):
            if re.match(pattern, prereq):
                if isOttawa:
                    subject, courseNum = re.match(pattern, prereq).group().split(' ')
                else:
                    subject, courseNum = re.match(pattern, prereq).group().split('*')
                prereqSet.add((subject, int(courseNum)))
        # nested list
        else:
            for item in prereq:
                if isinstance(item, str):
                    if re.match(pattern, item):
                        if isOttawa:
                            subject, courseNum = re.match(pattern, item).group().split(' ')
                        else:
                            subject, courseNum = re.match(pattern, item).group().split('*')
                        prereqSet.add((subject, int(courseNum)))
                # nested and/or list
                elif isinstance(item, list):
                    for elem in item:
                        if isinstance(elem, str):
                            if re.match(pattern, elem):
                                if isOttawa:
                                    subject, courseNum = re.match(pattern, elem).group().split(' ')
                                else:
                                    subject, courseNum = re.match(pattern, elem).group().split('*')
                                prereqSet.add((subject, int(courseNum)))
    return prereqSet


def getAllCoursePrereqs(allCoursesList: list, courseList: list, numNew: int, isOttawa=False):
    """
    function to get all course pre-requisites
    """
    coursesToAdd = set()

    for course in courseList:
        coursesToAdd.update(getNewCoursePreq(course, isOttawa))
    if numNew < len(coursesToAdd):
        preReqSET_g.update(coursesToAdd)
        newList = []
        for item in coursesToAdd:
            try:
                course = course_util.findCourse(allCoursesList, item[0], item[1])
                newList.append(course)
            except ValueError as e:
                continue
        getAllCoursePrereqs(allCoursesList, newList, len(coursesToAdd), isOttawa)
    else:
        return


def buildGraphEdge(element, connectingCourse, nodeStyle, edgeStyle, isOttawa=False, isManditory=False):
    global graph

    for option in element['options']:
        if isinstance(option, str):
            newNode = Node(option, nodeStyle)
            try:
                graph.nodes.remove(newNode)
            except KeyError:
                pass

            graph.nodes.add(newNode)
            graph.add(newNode, connectingCourse['subject'], connectingCourse['course_num'], nodeStyle, edgeStyle, isOttawa)
            


def getNextNodeStyle(increment=True, optionalShape=False) -> NodeStyle:
    global optionalNodeStyleList
    global optionalNodeDiamondStyleList
    global nodeStyleIndex
    global optionalNodeStyleIndex

    if optionalShape:
        if increment:
            optionalNodeStyleIndex += 1
        return optionalNodeDiamondStyleList[optionalNodeStyleIndex % len(optionalNodeStyleList)]
    else:
        if increment:
            nodeStyleIndex += 1
        return optionalNodeStyleList[nodeStyleIndex % len(optionalNodeStyleList)]


def newBuildGraphEdge(prereq, idx :int, connectingCourse, nodeStyle, edgeStyle : EdgeStyle, isOttawa, isManditory=False, droppedCourses=None):
    global graph  

    newEdgeStyle = edgeStyle.__copy__()
    if isinstance(prereq, str):
        option = prereq
    else:
        if prereq['num_credits'] > 0.0:
            if prereq['is_credits']:
                newEdgeStyle.label = '{} credits including'.format(prereq['num_credits'])
            else:
                newEdgeStyle.label = '{}'.format(prereq['num_options'])
        option = prereq['options'][idx]

    newEdgeStyle.isManditory = isManditory

    

    if isManditory:
        newNode = Node(option, nodeStyle)
    else:
        newNode = Node(option, getNextNodeStyle(increment=False))
        
    try:
        graph.nodes.remove(newNode)
    except KeyError:
        pass

    if droppedCourses != None:
        if newNode.getName() in droppedCourses:
            newNode.isBlocked = True
            newEdgeStyle.isBlocked = True

    graph.nodes.add(newNode)
    graph.add(newNode, connectingCourse['subject'], connectingCourse['course_num'], nodeStyle, newEdgeStyle, isOttawa)

def traverseElement(element, course, nodeStyle, edgeStyle, isOttawa=False, droppedCourses=None):
    global nodeStyleIndex
    global isCreditNum
    global isOneOfMany
    global numOfMany

    if not element:
        isOneOfMany = False
        numOfMany = 0
        isCreditNum = False

    if isinstance(element, list):
        for elem in element:
            if isinstance(elem, list):
               traverseElement(elem, course, nodeStyle, edgeStyle, isOttawa)
            elif isinstance(elem, str):
                newBuildGraphEdge(elem, i, course, nodeStyle, edgeStyle, isOttawa, isManditory)
            else:
                if len(elem['options']) == 1:
                    isManditory = True
                else:
                    isManditory = False
                for i, option in enumerate(elem['options']):                   
                    if isinstance(option, str):
                        newBuildGraphEdge(elem, i, course, nodeStyle, edgeStyle, isOttawa, isManditory)
                    else:
                        traverseElement(option, course, nodeStyle, edgeStyle, isOttawa)
    else:
        if len(element['options']) == 1:
            isManditory = True
        else:
            isManditory = False
            
        for i, option in enumerate(element['options']):
            if isinstance(option, str):
                newBuildGraphEdge(element, i, course, nodeStyle, edgeStyle, isOttawa, isManditory)
            else:
                traverseElement(option, course, nodeStyle, edgeStyle, isOttawa)


def addIsolatedNode(course: dict, nodeStyle: NodeStyle, isOttawa: bool) -> None:
    global graph

    if isOttawa:
        pattern = re.compile('^\w{3} \d{4}$')
    else:
        pattern = re.compile('^[A-Z]{3}[A-Z]?\*[0-9]{4}$')

    if isOttawa:
        courseString = '{} {}'.format(course['subject'], course['course_num'])
    else:
        courseString = '{}*{}'.format(course['subject'], course['course_num'])
    newNode = Node(courseString, nodeStyle)
    graph.nodes.add(newNode)

def newGraphMake(courseFileIn: str, fileOut: str, subject: str, course_num=None, isOttawa=False, droppedCourses=None):
    global graph
    global isOneOfMany
    global numOfMany
    global isCreditNum
    global nodeStyleIndex

    graph = CourseGraph(padding=0.5, nodeSep=0.5, rankSep=1.25, splines=True, esep=0.5, isOttawa=isOttawa)

    allCourses = course_util.get_courses(courseFileIn)

    coursesList = []
    subjectSet = set()
    if subject:
        coursesList.append(course_util.filter_course_arr(allCourses, 'subject', subject))
        if course_num:
            coursesList[0] = course_util.filter_course_arr(coursesList[0], 'course_num', course_num)
    else:
        for item in allCourses:
            subjectSet.add(item['subject'])

        for item in sorted(subjectSet):
            courseList = []
            for course in allCourses:
                if course['subject'] == item:
                    courseList.append(course)
            coursesList.append(courseList)

    # default for first subject.
    nodeStyle = NodeStyle(shape='ellipse', colour='blue', id=0)
    # default
    solidEdgeStyle = EdgeStyle()
    # for OR condition
    dottedEdgeStyle = EdgeStyle(style='dashed', colour='grey', shape='odot')

    for courses in coursesList:
        # print('({}/{}) Currently graphing: {}'.format(count, totalNum, courses[0]['subject']))
        getAllCoursePrereqs(allCourses, courses, 0, isOttawa)
       
        for item in preReqSET_g:
            try:
                course = course_util.findCourse(allCourses, item[0], item[1])
                courses.append(course)
            except ValueError as e:
                continue

        for course in courses:
            prereqList = course['prereqs']
            if len(prereqList) == 0:
                addIsolatedNode(course, nodeStyle, isOttawa)
                
            for prereq in prereqList:
                if isinstance(prereq, list):
                    for item in prereq:
                        if len(item['options']) == 1:
                            isManditory = True
                        else:
                            isManditory = False
                            
                        for i, option in enumerate(item['options']):
                            if isinstance(option, str):
                                isOneOfMany = False
                                numOfMany = 0
                                isCreditNum = False
                                newBuildGraphEdge(item, i, course, nodeStyle, solidEdgeStyle, isOttawa, isManditory, droppedCourses)
                            else:
                                traverseElement(item, course, nodeStyle, dottedEdgeStyle, isOttawa, droppedCourses)
                elif isinstance(prereq, str):
                    newBuildGraphEdge(prereq, 0, course, nodeStyle, solidEdgeStyle, isOttawa, True, droppedCourses)
                    
                else:
                    if len(prereq['options']) == 1:
                        isManditory = True
                    else:
                        isManditory = False
                    for i, option in enumerate(prereq['options']):
                        if isinstance(option, str):
                            isOneOfMany = False
                            numOfMany = 0
                            isCreditNum = False
                            newBuildGraphEdge(prereq, i, course, nodeStyle, solidEdgeStyle, isOttawa,isManditory, droppedCourses)
                        else:
                            traverseElement(prereq, course, nodeStyle, dottedEdgeStyle, isOttawa, droppedCourses)
                nodeStyleIndex +=1

    return graph.toD3JSDict(is_ottawa=isOttawa)

def generateMajorGraph(courseFileIn: str, fileOut: str, major: dict, isOttawa=False) -> CourseGraph:
    global isOneOfMany
    global numOfMany
    global isCreditNum
    global graph
    global nodeStyleIndex

    graph = CourseGraph(padding=0.5, nodeSep=0.5, rankSep=1.25, splines=True, esep=0.5)

    allCourses = course_util.get_courses(courseFileIn)
    requiredList = major['requiredCourses']

    requiredCourses = set()

    optionalCourses = []

    for element in requiredList:
        if isinstance(element, str):
            requiredCourses.add(element)
        elif isinstance(element, list):
            optionalCourses.append(element)

    requiredCourseList = []
    for item in requiredCourses:
        subject, courseNum = item.split('*')
        try:
            course = course_util.findCourse(allCourses, subject, int(courseNum))
            requiredCourseList.append(course)
        except ValueError:
            pass

    coursesList = requiredCourseList

    getAllCoursePrereqs(allCourses, requiredCourseList, 0)

    for item in preReqSET_g:
        try:
            course = course_util.findCourse(allCourses, item[0], item[1])
            coursesList.append(course)
        except ValueError as e:
            continue

    # default for first subject.
    nodeStyle = NodeStyle(None, 'ellipse', 'blue')
    # default
    solidEdgeStyle = EdgeStyle()
    # for OR condition
    dottedEdgeStyle = EdgeStyle(style='dashed', colour='grey', shape='odot')

    for course in coursesList:
        prereqList = course['prereqs']
        for prereq in prereqList:
            if isinstance(prereq, str):
                buildGraphEdge(prereq, course, nodeStyle, solidEdgeStyle)
            else:
                traverseElement(prereq, course, getNextNodeStyle(False), dottedEdgeStyle)

    ## OPTIONAL Courses
    setOptionalNodeDiamondStyleList('diamond')
    preReqSET_g.clear()
    coursesList.clear()

    tempList = []
    for item in optionalCourses:
        tempList.append(item)

    for item in tempList:
        for elem in item:
            subject, courseNum = elem.split('*')
            try:
                course = course_util.findCourse(allCourses, subject, int(courseNum))
                coursesList.append(course)
            except ValueError:
                pass

    getAllCoursePrereqs(allCourses, coursesList, 0)

    for item in preReqSET_g:
        try:
            course = course_util.findCourse(allCourses, item[0], item[1])
            coursesList.append(course)
        except ValueError as e:
            continue

    for course in coursesList:
            prereqList = course['prereqs']
            if len(prereqList) == 0:
                addIsolatedNode(course, nodeStyle, isOttawa)
                
            for prereq in prereqList:
                if isinstance(prereq, list):
                    for item in prereq:
                        if item['num_options'] is len(item['options']):
                            isManditory = True
                        else:
                            isManditory = False
                            nodeStyleIndex +=1
                        for i, option in enumerate(item['options']):
                            if isinstance(option, str):
                                isOneOfMany = False
                                numOfMany = 0
                                isCreditNum = False
                                newBuildGraphEdge(item, i, course, nodeStyle, solidEdgeStyle, isOttawa, isManditory=isManditory)
                            else:
                                traverseElement(item, course, nodeStyle, dottedEdgeStyle, isOttawa,isManditory=isManditory)
                else:
                    if prereq['num_options'] is len(prereq['options']):
                        isManditory = True
                    else:
                        isManditory = False
                        nodeStyleIndex +=1
                    for i, option in enumerate(prereq['options']):
                        if isinstance(option, str):
                            isOneOfMany = False
                            numOfMany = 0
                            isCreditNum = False
                            newBuildGraphEdge(prereq, i, course, nodeStyle, solidEdgeStyle, isOttawa, isManditory=isManditory)
                        else:
                            traverseElement(prereq, course, nodeStyle, dottedEdgeStyle, isOttawa, isManditory=isManditory)


    return graph
    
def hasCourse(edge: GraphEdge, droppedCourses : list):
    if edge.getSrcName() in droppedCourses or edge.getDestName() in droppedCourses:
        return True
    return False
        
