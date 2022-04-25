import os
import sys
import unittest

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import course_util

"""
Unit testing for UOttawa
"""

"""
Testing scrapper for UOttawa
"""


class MyTestCase(unittest.TestCase):
    courses = course_util.get_courses('./scraper/degreeProgramCoursesOttawa.json')
    coursesByPreReqs = course_util.listToPrereqs(courses)

    def test_subject_CPT(self, subject="CPT"):
        coursesBySubject = course_util.filter_course_arr(self.courses, "subject", subject)
        self.assertNotEqual(len(coursesBySubject), 0, f'TEST : Subject called {subject} Failed.')

    def test_subject_SDS(self, subject="SDS"):
        coursesBySubject = course_util.filter_course_arr(self.courses, "subject", subject)
        self.assertNotEqual(len(coursesBySubject), 0, f'TEST : Subject called {subject} Failed.')

    def test_subject_ECO(self, subject="ECO"):
        coursesBySubject = course_util.filter_course_arr(self.courses, "subject", subject)
        self.assertNotEqual(len(coursesBySubject), 0, f'TEST : Subject called {subject} Failed.')

    def test_subject_EDU(self, subject="EDU"):
        coursesBySubject = course_util.filter_course_arr(self.courses, "subject", subject)
        self.assertNotEqual(len(coursesBySubject), 0, f'TEST : Subject called {subject} Failed.')

    def test_subject_JPN(self, subject="JPN"):
        coursesBySubject = course_util.filter_course_arr(self.courses, "subject", subject)
        self.assertNotEqual(len(coursesBySubject), 0, f'TEST : Subject called {subject} Failed.')

    def test_subject_no_name(self, subject="NO_NAME"):
        coursesBySubject = course_util.filter_course_arr(self.courses, "subject", subject)
        self.assertEqual(len(coursesBySubject), 0, f'TEST : Subject called {subject} Failed.')

    def test_course_name_integration(self, courseName="Intégration des compétences avancées en comptabilité"):
        coursesBySubject = course_util.filter_course_arr(self.courses, "course_name", courseName)
        self.assertNotEqual(len(coursesBySubject), 0, f'TEST : Course name called {courseName} Failed.')

    def test_course_name_social_business(self, courseName="Social Context of Business"):
        coursesBySubject = course_util.filter_course_arr(self.courses, "course_name", courseName)
        self.assertNotEqual(len(coursesBySubject), 0, f'TEST : Course name called {courseName} Failed.')

    def test_course_name_intermediate_accounting(self, courseName="Intermediate Accounting I"):
        coursesBySubject = course_util.filter_course_arr(self.courses, "course_name", courseName)
        self.assertNotEqual(len(coursesBySubject), 0, f'TEST : Course name called {courseName} Failed.')

    def test_course_name_statistiques(self, courseName="Les statistiques en gestion"):
        coursesBySubject = course_util.filter_course_arr(self.courses, "course_name", courseName)
        self.assertNotEqual(len(coursesBySubject), 0, f'TEST : Course name called {courseName} Failed.')

    def test_course_name_comportement_organisationnel(self, courseName="Comportement organisationnel"):
        coursesBySubject = course_util.filter_course_arr(self.courses, "course_name", courseName)
        self.assertNotEqual(len(coursesBySubject), 0, f'TEST : Course name called {courseName} Failed.')

    def test_course_name_no_name(self, courseName="I have no name"):
        coursesBySubject = course_util.filter_course_arr(self.courses, "course_name", courseName)
        self.assertEqual(len(coursesBySubject), 0, f'TEST : Course name called {courseName} Failed.')

    def test_offering_unspecified(self, offering="unspecified"):
        coursesBySubject = course_util.filter_course_arr(self.courses, "offering", offering)
        self.assertEqual(len(coursesBySubject), 0, f'TEST : Offering with {offering} Failed.')

    def test_offering_fall_only(self, subject="MAT", courseNum="4343"):
        coursesBySubject = course_util.filter_course_arr(self.courses, "subject", subject)
        coursesByNumber = course_util.filter_course_arr(coursesBySubject, "course_num", courseNum)
        self.assertEqual(coursesByNumber[0]['is_offered_fall'], False, f'TEST : Offered fall only Failed.')
        self.assertEqual(coursesByNumber[0]['is_offered_winter'], False, f'TEST : Offered fall only Failed.')
        self.assertEqual(coursesByNumber[0]['is_offered_summer'], False, f'TEST : Offered fall only Failed.')

    def test_credits_for_MAT_4343(self, subject="MAT", courseNum="4343"):
        coursesBySubject = course_util.filter_course_arr(self.courses, "subject", subject)
        coursesByNumber = course_util.filter_course_arr(coursesBySubject, "course_num", courseNum)
        self.assertEqual(coursesByNumber[0]['credits'], 3, f'TEST : credit for {courseNum}*{subject} Failed.')

    def test_credits_for_MAT_4399(self, subject="MAT", courseNum="4399"):
        coursesBySubject = course_util.filter_course_arr(self.courses, "subject", subject)
        coursesByNumber = course_util.filter_course_arr(coursesBySubject, "course_num", courseNum)
        self.assertEqual(coursesByNumber[0]['credits'], 3, f'TEST : credit for {courseNum}*{subject} Failed.')

    def test_credits_for_SEG_2106(self, subject="SEG", courseNum="2106"):
        coursesBySubject = course_util.filter_course_arr(self.courses, "subject", subject)
        coursesByNumber = course_util.filter_course_arr(coursesBySubject, "course_num", courseNum)
        self.assertEqual(coursesByNumber[0]['credits'], 3, f'TEST : credit for {courseNum}*{subject} Failed.')

    def test_credits_for_ESP_2911(self, subject="ESP", courseNum="2911"):
        coursesBySubject = course_util.filter_course_arr(self.courses, "subject", subject)
        coursesByNumber = course_util.filter_course_arr(coursesBySubject, "course_num", courseNum)
        self.assertEqual(coursesByNumber[0]['credits'], 3, f'TEST : credits for {courseNum}*{subject} Failed.')

    def test_credits_for_YDD_5901(self, subject="YDD", courseNum="5901"):
        coursesBySubject = course_util.filter_course_arr(self.courses, "subject", subject)
        coursesByNumber = course_util.filter_course_arr(coursesBySubject, "course_num", courseNum)
        self.assertEqual(coursesByNumber[0]['credits'], 3, f'TEST : credit for {courseNum}*{subject} Failed.')

    def test_credits_for_LCM_5507(self, subject="LCM", courseNum="5507"):
        coursesBySubject = course_util.filter_course_arr(self.courses, "subject", subject)
        coursesByNumber = course_util.filter_course_arr(coursesBySubject, "course_num", courseNum)
        self.assertEqual(coursesByNumber[0]['credits'], 3, f'TEST : credit for {courseNum}*{subject} Failed.')

    def test_lec_and_lab_for_MAT_4343(self, subject="MAT", courseNum="4343"):
        coursesBySubject = course_util.filter_course_arr(self.courses, "subject", subject)
        coursesByNumber = course_util.filter_course_arr(coursesBySubject, "course_num", courseNum)
        self.assertEqual(coursesByNumber[0]['lectures'], 0, f'TEST : lecture for {courseNum}*{subject} Failed.')
        self.assertEqual(coursesByNumber[0]['labs'], 0, f'TEST : labs for {courseNum}*{subject} Failed.')

    def test_lec_and_lab_for_MAT_4399(self, subject="MAT", courseNum="4399"):
        coursesBySubject = course_util.filter_course_arr(self.courses, "subject", subject)
        coursesByNumber = course_util.filter_course_arr(coursesBySubject, "course_num", courseNum)
        self.assertEqual(coursesByNumber[0]['lectures'], 0, f'TEST : lecture for {courseNum}*{subject} Failed.')
        self.assertEqual(coursesByNumber[0]['labs'], 0, f'TEST : labs for {courseNum}*{subject} Failed.')

    def test_lec_and_lab_for_SEG_2106(self, subject="SEG", courseNum="2106"):
        coursesBySubject = course_util.filter_course_arr(self.courses, "subject", subject)
        coursesByNumber = course_util.filter_course_arr(coursesBySubject, "course_num", courseNum)
        self.assertEqual(coursesByNumber[0]['lectures'], 0, f'TEST : lecture for {courseNum}*{subject} Failed.')
        self.assertEqual(coursesByNumber[0]['labs'], 0, f'TEST : labs for {courseNum}*{subject} Failed.')

    def test_lec_and_lab_for_ESP_2911(self, subject="ESP", courseNum="2911"):
        coursesBySubject = course_util.filter_course_arr(self.courses, "subject", subject)
        coursesByNumber = course_util.filter_course_arr(coursesBySubject, "course_num", courseNum)
        self.assertEqual(coursesByNumber[0]['lectures'], 0, f'TEST : lecture for {courseNum}*{subject} Failed.')
        self.assertEqual(coursesByNumber[0]['labs'], 0, f'TEST : labs for {courseNum}*{subject} Failed.')

    def test_lec_and_lab_for_YDD_5901(self, subject="YDD", courseNum="5901"):
        coursesBySubject = course_util.filter_course_arr(self.courses, "subject", subject)
        coursesByNumber = course_util.filter_course_arr(coursesBySubject, "course_num", courseNum)
        self.assertEqual(coursesByNumber[0]['lectures'], 0, f'TEST : lecture for {courseNum}*{subject} Failed.')
        self.assertEqual(coursesByNumber[0]['labs'], 0, f'TEST : labs for {courseNum}*{subject} Failed.')

    def test_lec_and_lab_for_LCM_5507(self, subject="LCM", courseNum="5507"):
        coursesBySubject = course_util.filter_course_arr(self.courses, "subject", subject)
        coursesByNumber = course_util.filter_course_arr(coursesBySubject, "course_num", courseNum)
        self.assertEqual(coursesByNumber[0]['lectures'], 0, f'TEST : lecture for {courseNum}*{subject} Failed.')
        self.assertEqual(coursesByNumber[0]['labs'], 0, f'TEST : labs for {courseNum}*{subject} Failed.')

    def test_pre_req_for_DCC_2119(self, subject="DCC", courseNum="2119"):
        coursesBySubject = course_util.filter_course_arr(self.coursesByPreReqs, "subject", subject)
        coursesByNumber = course_util.filter_course_arr(coursesBySubject, "course_num", courseNum)
        self.assertEqual(coursesByNumber[0]['prereqs'], [['Prerequisite: DCC\xa02118']],
                         f'TEST : pre-requisites for {courseNum}*{subject} Failed.')

    def test_pre_req_for_DRC_4513(self, subject="DRC", courseNum="4513"):
        coursesBySubject = course_util.filter_course_arr(self.coursesByPreReqs, "subject", subject)
        coursesByNumber = course_util.filter_course_arr(coursesBySubject, "course_num", courseNum)
        self.assertEqual(coursesByNumber[0]['prereqs'], [['Préalable : DRC\xa01708']],
                         f'TEST : pre-requisites for {courseNum}*{subject} Failed.')

    def test_pre_req_for_DCC_2121(self, subject="DCC", courseNum="2121"):
        coursesBySubject = course_util.filter_course_arr(self.coursesByPreReqs, "subject", subject)
        coursesByNumber = course_util.filter_course_arr(coursesBySubject, "course_num", courseNum)
        self.assertEqual(coursesByNumber[0]['prereqs'], [['Prerequisite: DCC\xa02118']],
                         f'TEST : pre-requisites for {courseNum}*{subject} Failed.')

    def test_pre_req_for_GEG_3101(self, subject="GEG", courseNum="3101"):
        coursesBySubject = course_util.filter_course_arr(self.coursesByPreReqs, "subject", subject)
        coursesByNumber = course_util.filter_course_arr(coursesBySubject, "course_num", courseNum)
        self.assertEqual(coursesByNumber[0]['prereqs'], [['Prerequisite: GEG\xa02301. Course includes laboratory', 'field work']],
                         f'TEST : pre-requisites for {courseNum}*{subject} Failed.')

    def test_pre_req_for_GEG_3102(self, subject="GEG", courseNum="3102"):
        coursesBySubject = course_util.filter_course_arr(self.coursesByPreReqs, "subject", subject)
        coursesByNumber = course_util.filter_course_arr(coursesBySubject, "course_num", courseNum)
        self.assertEqual(coursesByNumber[0]['prereqs'], [['Prerequisite: GEG\xa01301', 'EVS\xa01101. Course with laboratory', 'field work']],
                         f'TEST : pre-requisites for {courseNum}*{subject} Failed.')


if __name__ == '__main__':
    unittest.main()
