from collections import defaultdict

def checkTopSort(graphDict):
    #creating a set to count unique vertices in our graph
    vertices = set()
    #Initialize a dictionary to keep track of the inwards degree of vertices
    inDegree = {}
    for key in graphDict:
        #Set all courses inwards degree to 0
        inDegree[key] = 0
        vertices.add(key)
        for key2 in graphDict[key]:
            inDegree[key2] = 0
            vertices.add(key2)
    #Go through each course stored as a value in the dictionary and increment inwards degree
    for i in graphDict:
        for vertex in graphDict[i]:
            inDegree[vertex] += 1
    #Add all vertices with inward degree 0 to queue
    queue = []
    for vertex in graphDict:
        #dont need to check the vertices in the values since they have atleast degree > 0
        if inDegree[vertex] == 0:
            queue.append(vertex)
    #Keep track of how many vertices we visited
    count = 0
    #Vector for the actual topological sorting
    ordering = []

    #Loop as long as the queue isnt empty
    while queue:
        front = queue.pop(0)
        #Append current course in queue to our sorting
        ordering.append(front)
        #For each neighbour decrement the inwards degree
        for connection in graphDict[front]:
            inDegree[connection] -= 1
            if inDegree[connection] == 0:
                queue.append(connection)
        count += 1
    if count != len(vertices):
        return False
    else:
        return True

def recursion(node, visited, stack, graphDict):
    #Mark current node as visited/stack
    visited[node] = True
    stack[node] = True
    #Check each path from current course
    for connection in graphDict[node]:
        if visited[connection] == False:
            if recursion(connection, visited, stack, graphDict) == True:
                return True
        elif stack[connection] == True:
            return True
    #Remove course from the stack
    stack[node] = False
    return False

def checkCycle(graphDict):
    visited = {}
    stack = {}
    #Initialize every value to False
    for key in graphDict:
        visited[key] = False
        stack[key] = False
        #Need to initialize the courses stored in the values as well
        for key2 in graphDict[key]:
            visited[key2] = False
            stack[key2] = False
    #Go through each course and check for paths recursively
    for node in graphDict:
        if visited[node] == False:
            if recursion(node, visited, stack, graphDict) == True:
                return True
            return False

def validate(graph):
    #Initialize dictionary of lists
    graphDict = defaultdict(list)
    for node in graph:
        graphDict[str(node.edge[0].toString())].append(node.edge[1].toString())
    
    if not checkCycle(graphDict) and checkTopSort(graphDict):
        return True
    else:
        return False