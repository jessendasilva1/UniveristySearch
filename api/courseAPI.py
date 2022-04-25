import json
import re

from flask import Flask, Response, request

import sys

sys.path.append('graphing/util')

import search
import graph
import majorGraph

app = Flask(__name__)

valid_params = ['is_ottawa', 'is_guelph', 'subject', 'course_num', 'name', 'is_offered_fall'
    , 'is_offered_winter', 'is_offered_winter', 'is_offered_summer', 'lectures', 'labs', 'credits'
    , 'prereqs', 'blocked']

boolean_params = ['true', 'false']

valid_subject_params = ['is_ottawa', 'is_guelph', 'is_major']
valid_graph_params = ['is_ottawa', 'is_guelph', 'subject', 'blocked']
valid_major_params = ['is_ottawa', 'is_guelph', 'major_code']


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def isValidParams(args, params):
    if args is not None:
        for key in args.keys():
            if key not in params:
                return False

    return True


#api get request for course search
@app.route("/api/courses", methods=['GET'])
def guelphAndOttawaSearch():
    args = json.loads(json.dumps(request.args))
    if not isValidParams(args, valid_params):
        return Response('{"code": 400 ,"message": "Bad Request"}', status=400, mimetype='application/json')

    if "is_ottawa" not in args.keys() or "is_guelph" not in args.keys():
        return Response('{"code": 400 ,"message": "Bad Request"}', status=400, mimetype='application/json')

    if args.get('is_guelph') not in boolean_params or args.get('is_ottawa') not in boolean_params:
        return Response('{"code": 400 ,"message": "Bad Request"}', status=400, mimetype='application/json')

    # if args.get('is_ottawa') == 'true' and args.get('is_guelph') == 'true':
    #     return Response("{'code' : 404, 'message': 'Bad Request'}", status=404,
    #                     mimetype='application/json')

    if args.get('is_ottawa') == 'false' and args.get('is_guelph') == 'false':
        return Response("{'code' : 200, 'message': 'Successful Request'}", status=200,
                        mimetype='application/json')

    if "prereqs" in args.keys():
        return Response('{"code": 400 ,"message": "Bad Request - prereq filtering not supported"}', status=400,
                        mimetype='application/json')

    if "course_num" in args.keys() and not re.match(r'\d+', args.get('course_num')):
        return Response('{"code": 400 ,"message": "Bad Request"}', status=400, mimetype='application/json')

    if "lectures" in args.keys() and not re.match(r'\d+', args.get('lectures')):
        return Response('{"code": 400 ,"message": "Bad Request"}', status=400, mimetype='application/json')

    if "labs" in args.keys() and not re.match(r'\d+', args.get('labs')):
        return Response('{"code": 400 ,"message": "Bad Request"}', status=400, mimetype='application/json')

    if "credits" in args.keys() and not isfloat(args.get('credits')):
        return Response('{"code": 400 ,"message": "Bad Request"}', status=400, mimetype='application/json')

    if "is_offered_fall" in args.keys() and args.get('is_offered_fall') not in boolean_params:
        return Response('{"code": 400 ,"message": "Bad Request"}', status=400, mimetype='application/json')

    if "is_offered_winter" in args.keys() and args.get('is_offered_winter') not in boolean_params:
        return Response('{"code": 400 ,"message": "Bad Request"}', status=400, mimetype='application/json')

    if "is_offered_summer" in args.keys() and args.get('is_offered_summer') not in boolean_params:
        return Response('{"code": 400 ,"message": "Bad Request"}', status=400, mimetype='application/json')

    res = []
    if args.get('is_ottawa') == 'true':
        res += search.searchV2(args, 'graphing/generated/uOttawaCourseData.json')
    if args.get('is_guelph') == 'true':
        res += search.searchV2(args, 'graphing/generated/courseData.json')

    if len(res) == 0:
        return Response('{"code" : 404, "message": "No course found"}', status=404, mimetype='application/json')

    return Response(json.dumps(res), status=200, mimetype='application/json')

#api get request for the subjects that could be searched when a school(s) are chosen
@app.route("/api/subjects", methods=['GET'])
def guelphAndOttawaSubjectSearch():
    args = json.loads(json.dumps(request.args))
    if not isValidParams(args, valid_subject_params):
        return Response('{"code": 400 ,"message": "Bad Request"}', status=400, mimetype='application/json')

    if "is_ottawa" not in args.keys() or "is_guelph" not in args.keys() or "is_major" not in args.keys():
        return Response('{"code": 400 ,"message": "Bad Request"}', status=400, mimetype='application/json')

    if args.get('is_guelph') not in boolean_params or args.get('is_ottawa') not in boolean_params \
            or args.get('is_major') not in boolean_params:
        return Response('{"code": 400 ,"message": "Bad Request"}', status=400, mimetype='application/json')

    if args.get('is_ottawa') == 'false' and args.get('is_guelph') == 'false':
        return Response('{"code" : 200, "message": ""}', status=200,
                        mimetype='application/json')

    res = []
    if args.get('is_major') == 'false':
        res = search.searchAllSubjects(args['is_ottawa'], args['is_guelph'])
    else:
        res = search.searchAllMajorSubjects(args['is_ottawa'], args['is_guelph'])

    if len(res) == 0:
        return Response('{"code" : 404, "message": "No subject found"}', status=404, mimetype='application/json')

    return Response(json.dumps(res), status=200, mimetype='application/json')

#api get request for data to graph on page
@app.route("/api/courses/graph", methods=['GET'])
def guelphAndOttawaGraphSearch():
    args = json.loads(json.dumps(request.args))
    print(args)
    if not isValidParams(args, valid_graph_params):
        return Response('{"code": 400 ,"message": "Bad Request"}', status=400, mimetype='application/json')

    if "is_ottawa" not in args.keys() or "is_guelph" not in args.keys():
        return Response('{"code": 400 ,"message": "Bad Request"}', status=400, mimetype='application/json')

    if args.get('is_guelph') not in boolean_params or args.get('is_ottawa') not in boolean_params \
            or args.get('subject') is None or len(args.get('subject')) == 0:
        return Response('{"code": 400 ,"message": "Bad Request"}', status=400, mimetype='application/json')

    if args.get('is_ottawa') == 'true' and args.get('is_guelph') == 'true':
        return Response("{'code' : 400, 'message': 'Bad Request, cannot access both resources together'}", status=200,
                        mimetype='application/json')
    if args.get('is_ottawa') == 'false' and args.get('is_guelph') == 'false':
        return Response("{'code' : 200, 'message': 'Successful Request'}", status=200,
                        mimetype='application/json')

    # temp block requests for ottawa graphing
    if args.get('is_ottawa') == "true":
        return Response('{"code": 501, "message": "Graphing for Ottawa is not currently supported"}', status=501, mimetype='application/json')
    
    subjectAndCode = args.get('subject').split()

    if len(subjectAndCode) > 2:
        return Response('{"code" : 404, "message": "No subject found, graph cannot be created"}', status=404,
                        mimetype='application/json')
    
    if "blocked" in args.keys():
        blockedArgs = args.get("blocked").split(",")
    else:
        blockedArgs = None

    if len(subjectAndCode) == 2:
        res = search.getJSONGraph(args.get('is_ottawa'), args.get('is_guelph'), subjectAndCode[0], subjectAndCode[1], blockedArgs)
    else:
        print(args.get('subject'))
        res = search.getJSONGraph(args.get('is_ottawa'), args.get('is_guelph'), args.get('subject'), blockedArgs)

    if len(res) == 0:
        return Response('{"code" : 404, "message": "No subject found, graph cannot be created"}', status=404,
                        mimetype='application/json')

    return Response(json.dumps(res), status=200, mimetype='application/json')


#api get to graph a major graph when implemented
@app.route("/api/majors/graph", methods=['GET'])
def guelphAndOttawaMajorGraphSearch():
     # temp block requets for graphing major data
    return Response('{"code": 501, "message": "Graphing for Ottawa is not currently supported"}', status=501, mimetype='application/json')


    args = json.loads(json.dumps(request.args))
    if not isValidParams(args, valid_major_params):
        return Response('{"code": 400 ,"message": "Bad Request"}', status=400, mimetype='application/json')

    if "is_ottawa" not in args.keys() or "is_guelph" not in args.keys() or "major_code" not in args.keys():
        return Response('{"code": 400 ,"message": "Bad Request"}', status=400, mimetype='application/json')

    if args.get('is_guelph') not in boolean_params or args.get('is_ottawa') not in boolean_params \
            or args.get('major_code') is None or len(args.get('major_code')) == 0:
        return Response('{"code": 400 ,"message": "Bad Request"}', status=400, mimetype='application/json')

    if args.get('is_ottawa') == 'true' and args.get('is_guelph') == 'true':
        return Response("{'code' : 400, 'message': 'Bad Request, cannot access both resources together'}", status=200,
                        mimetype='application/json')
    if args.get('is_ottawa') == 'false' and args.get('is_guelph') == 'false':
        return Response("{'code' : 200, 'message': 'Successful Request'}", status=200,
                        mimetype='application/json')
    
    res = []
    res = search.getJSONMajorGraph(args.get('is_ottawa'), args.get('is_guelph'), args.get('major_code'))

    if len(res) == 0:
        return Response('{"code" : 404, "message": "No major found, graph cannot be created"}', status=404,
                        mimetype='application/json')

    return Response(json.dumps(res), status=200, mimetype='application/json')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
