import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import validateGraph
import graph
import course_util

#Nodestyle isnt very important for test
nodeStyle = graph.NodeStyle(None, 'ellipse', 'blue')
solidEdgeStyle = graph.EdgeStyle()

graph1 = graph.CourseGraph()
node1 = graph.Node('CIS*1300', nodeStyle)
node2 = graph.Node('CIS*1500', nodeStyle)
graph1.add(graph.GraphEdge(node1, node2, solidEdgeStyle))
node3 = graph.Node('CIS*2100', nodeStyle)
node4 = graph.Node('CIS*2200', nodeStyle)
graph1.add(graph.GraphEdge(node2, node3, solidEdgeStyle))
graph1.add(graph.GraphEdge(node2, node4, solidEdgeStyle))
node5 = graph.Node('CIS*2750', nodeStyle)
graph1.add(graph.GraphEdge(node4, node5, solidEdgeStyle))
node6 = graph.Node('CIS*3750', nodeStyle)
graph1.add(graph.GraphEdge(node5, node6, solidEdgeStyle))
#This is an example of a valid graph!

#Test 1
if graph.validate(graph1):
    print('Test 1 Success: Detected a valid graph')
else:
    print('Test 1 Failed: Did not detect a valid graph')

graph2 = graph.CourseGraph()
node7 = graph.Node('MATH*1100', nodeStyle)
node8 = graph.Node('MATH*1200', nodeStyle)
node9 = graph.Node('MATH*2000', nodeStyle)
node10 = graph.Node('MATH*2310', nodeStyle)
node11 = graph.Node('MATH*2420', nodeStyle)
node12 = graph.Node('MATH*2500', nodeStyle)
node13 = graph.Node('MATH*2550', nodeStyle)
node14 = graph.Node('MATH*3010', nodeStyle)
node15 = graph.Node('MATH*3200', nodeStyle)
node16 = graph.Node('MATH*3500', nodeStyle)
graph2.add(graph.GraphEdge(node7, node8, solidEdgeStyle))
graph2.add(graph.GraphEdge(node7, node9, solidEdgeStyle))
graph2.add(graph.GraphEdge(node8, node10, solidEdgeStyle))
graph2.add(graph.GraphEdge(node9, node10, solidEdgeStyle))
graph2.add(graph.GraphEdge(node10, node11, solidEdgeStyle))
graph2.add(graph.GraphEdge(node10, node12, solidEdgeStyle))
graph2.add(graph.GraphEdge(node10, node13, solidEdgeStyle))
graph2.add(graph.GraphEdge(node12, node14, solidEdgeStyle))
graph2.add(graph.GraphEdge(node13, node15, solidEdgeStyle))
graph2.add(graph.GraphEdge(node15, node16, solidEdgeStyle))
graph2.add(graph.GraphEdge(node16, node10, solidEdgeStyle))
#This is an invalid graph!

#Test 2
if graph.validate(graph2):
    print('Test 2 Failed: Detected a valid graph')
else:
    print('Test 2 Success: Did not detect a valid graph')

graph3 = graph.CourseGraph()
node17 = graph.Node('ENGG*1100', nodeStyle)
node18 = graph.Node('ENGG*1410', nodeStyle)
node19 = graph.Node('ENGG*1210', nodeStyle)
node20 = graph.Node('ENGG*1420', nodeStyle)
node21 = graph.Node('ENGG*1500', nodeStyle)
node22 = graph.Node('ENGG*2400', nodeStyle)
node23 = graph.Node('ENGG*2410', nodeStyle)
node24 = graph.Node('ENGG*2100', nodeStyle)
node25 = graph.Node('ENGG*2450', nodeStyle)
node26 = graph.Node('ENGG*3380', nodeStyle)
node27 = graph.Node('ENGG*3390', nodeStyle)
node28 = graph.Node('ENGG*3450', nodeStyle)
node29 = graph.Node('ENGG*3640', nodeStyle)
node30 = graph.Node('ENGG*4450', nodeStyle)
node31 = graph.Node('ENGG*3100', nodeStyle)
node32 = graph.Node('ENGG*3210', nodeStyle)
node33 = graph.Node('ENGG*3410', nodeStyle)
node34 = graph.Node('ENGG*3050', nodeStyle)
node35 = graph.Node('ENGG*3240', nodeStyle)
node36 = graph.Node('ENGG*4000', nodeStyle)
node37 = graph.Node('ENGG*4420', nodeStyle)
node38 = graph.Node('ENGG*4170', nodeStyle)
node39 = graph.Node('ENGG*4540', nodeStyle)
node40 = graph.Node('ENGG*4550', nodeStyle)
graph3.add(graph.GraphEdge(node19, node22, solidEdgeStyle))
graph3.add(graph.GraphEdge(node21, node22, solidEdgeStyle))
graph3.add(graph.GraphEdge(node21, node22, solidEdgeStyle))
graph3.add(graph.GraphEdge(node17, node24, solidEdgeStyle))
graph3.add(graph.GraphEdge(node21, node24, solidEdgeStyle))
graph3.add(graph.GraphEdge(node22, node25, solidEdgeStyle))
graph3.add(graph.GraphEdge(node23, node26, solidEdgeStyle))
graph3.add(graph.GraphEdge(node21, node22, solidEdgeStyle))
graph3.add(graph.GraphEdge(node22, node27, solidEdgeStyle))
graph3.add(graph.GraphEdge(node25, node28, solidEdgeStyle))
graph3.add(graph.GraphEdge(node23, node29, solidEdgeStyle))
graph3.add(graph.GraphEdge(node25, node29, solidEdgeStyle))
graph3.add(graph.GraphEdge(node24, node30, solidEdgeStyle))
graph3.add(graph.GraphEdge(node21, node22, solidEdgeStyle))
graph3.add(graph.GraphEdge(node24, node31, solidEdgeStyle))
graph3.add(graph.GraphEdge(node22, node33, solidEdgeStyle))
graph3.add(graph.GraphEdge(node23, node34, solidEdgeStyle))
graph3.add(graph.GraphEdge(node26, node34, solidEdgeStyle))
graph3.add(graph.GraphEdge(node21, node22, solidEdgeStyle))
graph3.add(graph.GraphEdge(node31, node36, solidEdgeStyle))
graph3.add(graph.GraphEdge(node22, node37, solidEdgeStyle))
graph3.add(graph.GraphEdge(node29, node37, solidEdgeStyle))
graph3.add(graph.GraphEdge(node36, node38, solidEdgeStyle))
graph3.add(graph.GraphEdge(node26, node39, solidEdgeStyle))
graph3.add(graph.GraphEdge(node23, node40, solidEdgeStyle))
graph3.add(graph.GraphEdge(node25, node40, solidEdgeStyle))
graph3.add(graph.GraphEdge(node28, node40, solidEdgeStyle))
#This is a valid graph!

#Test 3
if graph.validate(graph3):
    print('Test 3 Success: Detected a valid graph')
else:
    print('Test 3 Failed: Did not detect a valid graph')

graph4 = graph.CourseGraph()
graph4.add(graph.GraphEdge(node19, node22, solidEdgeStyle))
graph4.add(graph.GraphEdge(node21, node22, solidEdgeStyle))
graph4.add(graph.GraphEdge(node21, node22, solidEdgeStyle))
graph4.add(graph.GraphEdge(node17, node24, solidEdgeStyle))
graph4.add(graph.GraphEdge(node21, node24, solidEdgeStyle))
graph4.add(graph.GraphEdge(node22, node25, solidEdgeStyle))
graph4.add(graph.GraphEdge(node23, node26, solidEdgeStyle))
graph4.add(graph.GraphEdge(node21, node22, solidEdgeStyle))
graph4.add(graph.GraphEdge(node22, node27, solidEdgeStyle))
graph4.add(graph.GraphEdge(node25, node28, solidEdgeStyle))
graph4.add(graph.GraphEdge(node23, node29, solidEdgeStyle))
graph4.add(graph.GraphEdge(node25, node29, solidEdgeStyle))
graph4.add(graph.GraphEdge(node24, node30, solidEdgeStyle))
graph4.add(graph.GraphEdge(node21, node22, solidEdgeStyle))
graph4.add(graph.GraphEdge(node24, node31, solidEdgeStyle))
graph4.add(graph.GraphEdge(node22, node33, solidEdgeStyle))
graph4.add(graph.GraphEdge(node23, node34, solidEdgeStyle))
graph4.add(graph.GraphEdge(node26, node34, solidEdgeStyle))
graph4.add(graph.GraphEdge(node21, node22, solidEdgeStyle))
graph4.add(graph.GraphEdge(node31, node36, solidEdgeStyle))
graph4.add(graph.GraphEdge(node22, node37, solidEdgeStyle))
graph4.add(graph.GraphEdge(node29, node37, solidEdgeStyle))
graph4.add(graph.GraphEdge(node36, node38, solidEdgeStyle))
graph4.add(graph.GraphEdge(node26, node39, solidEdgeStyle))
graph4.add(graph.GraphEdge(node23, node40, solidEdgeStyle))
graph4.add(graph.GraphEdge(node25, node40, solidEdgeStyle))
graph4.add(graph.GraphEdge(node28, node40, solidEdgeStyle))
graph4.add(graph.GraphEdge(node40, node19, solidEdgeStyle))
#This is not a valid graph

#Test 4
if graph.validate(graph4):
    print('Test 4 Failed: Detected a valid graph')
else:
    print('Test 4 Success: Did not detect a valid graph')

#courseData = course_util.get_courses('./courseData.json')
#Test 5
#if graph.validate(graph.graphMake('ANTH', None)):
#    print('Test 5 Success: Detected a valid graph')
#else:
#    print('Test 5 Failed: Did not detect a valid graph')