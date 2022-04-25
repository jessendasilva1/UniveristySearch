import json
import os
import sys
from typing import Dict, Union
import course_util

sys.path.append('graphing/generated')


class Subject:
    def __init__(self, code: str, name: str, is_ottawa: bool, is_guelph: bool):
        if name is None:
            raise TypeError('Invalid name. Node Name cannot be None')
        if name.strip() == "":
            raise ValueError('Invalid name. Node Name cannot be empty')

        if code is None:
            raise TypeError('Invalid code. Node Name cannot be None')

        self.code = code
        self.name = name
        self.is_ottawa = is_ottawa
        self.is_guelph = is_guelph

    # Override equal comparison
    def __eq__(self, other) -> bool:
        return \
            self.name == other.name and self.code == self.code \
            and self.is_ottawa == other.is_ottawa and self.is_guelph == self.is_guelph

    # override hash function
    def __hash__(self):
        return hash(hash(self.name) + hash(self.code) + hash(self.is_ottawa) + hash(self.is_guelph))

    def toString(self) -> Dict[str, Union[str, bool]]:
        return {'code': str(self.code), 'name': self.name, 'is_ottawa': self.is_ottawa, 'is_guelph': self.is_guelph}


def getAllSubjects(is_ottawa, is_guelph) -> set:
    subjects = set()
    is_guelph_value = True if is_guelph == 'true' else False
    is_ottawa_value = True if is_ottawa == 'true' else False

    if is_guelph_value:
        f = open('graphing/generated/courseData.json', mode='r', encoding='utf-8')
        jsonSubjects = json.loads(f.read())
        for sub in jsonSubjects:
            subjects.add(Subject(sub['subject'], sub['subject_name'], False, True))
        f.close()

    if is_ottawa_value:
        f = open('graphing/generated/uOttawaCourseData.json', mode='r', encoding='utf-8')
        jsonSubjects = json.loads(f.read())
        for sub in jsonSubjects:
            if 'subject_name' in sub.keys():
                subjects.add(Subject(sub['subject'], sub['subject_name'], True, False))
            else:
                subjects.add(Subject(sub['subject'], "Unknown", True, False))
        f.close()

    return subjects


def getAllMajorSubjects(is_ottawa, is_guelph) -> set:
    subjects = set()
    is_guelph_value = True if is_guelph == 'true' else False
    is_ottawa_value = True if is_ottawa == 'true' else False

    if is_guelph_value:
        f = open('graphing/generated/degreeProgramCourses.json', mode='r', encoding='utf-8')
        jsonSubjects = json.loads(f.read())
        for sub in jsonSubjects:
            subjects.add(Subject(sub['majorCode'], sub['majorName'], is_ottawa_value, is_guelph_value))
        f.close()

    if is_ottawa_value:
        f = open('graphing/generated/degreeProgramCoursesOttawa.json', mode='r', encoding='utf-8')
        jsonSubjects = json.loads(f.read())
        for sub in jsonSubjects:
            subjects.add(Subject(str(sub['course_num']), sub['subject'], is_ottawa_value, is_guelph_value))
        f.close()

    return subjects
