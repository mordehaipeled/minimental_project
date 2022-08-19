# this file handles communications with firebase
# excess to the database is with db and to the storage with storage
# to authenticate users use auth_fb

import os

from pyasn1.compat.octets import null
from pyrebase import pyrebase
from Ex1 import Date
from image_handler import determine_shapes_in_img

config = {
    "apiKey": os.getenv("apiKey"),
    "authDomain": os.getenv("authDomain"),
    "databaseURL": os.getenv("databaseURL"),
    "storageBucket": os.getenv("storageBucket")
}

firebase = pyrebase.initialize_app(config)
auth_fb = firebase.auth()
db = firebase.database()
storage = firebase.storage()  # when we have the pictures,audio files and objects; they will be pulled from here.


# finds a patient in the database by the uid if it can't find one returns null
def get_patient(patient_key):
    patients = db.child('Patients').get()
    for patient in patients.each():
        # print(patient.key())
        if patient_key == patient.key():
            return patient.val()
    return null


# checking by email returns a boolean
def check_if_patient_exists(patient_key):
    patients = db.child('Patients').get()
    for patient in patients.each():
        # print(patient.val()["patient details"]["email"])
        if patient_key == patient.val()["patient details"]["email"]:
            return True
    return False


# checking by email returns a boolean
def check_if_doctor_exists(email):
    doctors = db.child('Doctors').get()
    for doctor in doctors.each():
        if email == doctor.val().get('email'):
            return True
    return False


# param is a list of numbers in a string form, should follow the 100 - 7 logic
# returns a number from 0 to 5, so it's possible to make one mistake and still get 5 points
def score_math_question(param):
    print("score_math")
    score1 = 0
    if param == ['93', '86', '79', '72', '65', '58']:
        return 5
    i = 0
    if param[i] == '93':
        score1 = score1 + 1
    # ['25', '35', '7575', '75', '90', '21']
    print("score math")
    print(param)
    while i < len(param) - 1:
        if int(param[i]) - int(param[i + 1]) == 7:
            score1 = score1 + 1
            print(int(param[i]))
        i = i + 1
    print(param)
    return score1


# if the number of words in the string is 3 or more return 1 otherwise returns 0
def num_of_words_in_string(sentence):
    result = len(sentence.split())
    if result > 2:
        return 1
    else:
        return 0


# returns score for question 2 or 4
# we don't check for spelling here
def test_question_two(param, param1, param2, patient_details):
    ans_list = [param, param1, param2]
    expected_list = [patient_details['next test']['secondQuestion']['object1'],
                     patient_details['next test']['secondQuestion']['object2'],
                     patient_details['next test']['secondQuestion']['object3']]
    # if all correct and in order
    if ans_list == expected_list:
        return 3
    # if all correct but not in order
    if expected_list[0] in ans_list and expected_list[1] in ans_list and expected_list[2] in ans_list:
        return 2
    # if at least 2 are correct in order or not
    if ((expected_list[0] in ans_list and expected_list[1] in ans_list) or
            (expected_list[2] in ans_list and expected_list[1] in ans_list) or
            (expected_list[0] in ans_list and expected_list[2] in ans_list)):
        return 2
    # at least one is correct in order or not
    if expected_list[0] in ans_list or expected_list[1] in ans_list or expected_list[2] in ans_list:
        return 1
    # if none are correct
    return 0


# score is only ment to score the latest test (comparing with next test in patient details)
# some questions have functions called and some don't
def score(test, patient_details):
    print("score beg")
    if test.key() != "token":
        location_score = 0
        time_score = 0
        q2score = 0
        q3score = 0
        q4score = 0
        q5score = 0
        q6score = 0
        q7score = 0
        q8score = 0
        q9score = 0
        q10score = 0

        check = Date()

        for question, val in test.val().items():
            if question == "FirstQuestion":
                try:
                    print("score first question")
                    # print(val['value']['address'], patient_details['patient details']["street"], sep="\n-----\n\n")
                    _date = check.getDate()
                    day = check.getDay()
                    month = check.getMonth()
                    season = check.getSeason()
                    year = check.getYear()
                    if val['value']['date'] in _date:
                        time_score = time_score + 1
                    if val['value']['day'] == day:
                        time_score = time_score + 1
                    if val['value']['month'] == month:
                        time_score = time_score + 1
                    if val['value']['season'] in season:
                        time_score = time_score + 1
                    if val['value']['year'] == year:
                        time_score = time_score + 1
                    if val['value']['address'] == patient_details['patient details']["street"]:
                        location_score = location_score + 1
                    if val['value']['area'] == patient_details['patient details']["area"]:
                        location_score = location_score + 1
                    if val['value']['floor'] == patient_details['patient details']["floor"]:
                        location_score = location_score + 1
                    if val['value']['country'] == patient_details['patient details']["country"]:
                        location_score = location_score + 1
                    if val['value']['city'] == patient_details['patient details']["city"]:
                        location_score = location_score + 1
                except Exception as e:
                    print("no answer given", e)
            elif question == "SecondQuestion":
                print("score second question")
                # print(val["value"]["object1"] == patient_details['next test']['secondQuestion']['object1'])
                try:
                    if val["value"] != "לא ענה על השאלה":
                        q2score = test_question_two(val["value"]["object1"], val["value"]["object2"],
                                                    val["value"]["object3"], patient_details)
                except Exception as e:
                    print("no answer given", e)
            elif question == "MathQuestion":
                print("score third question")
                if val["value"] != "לא ענה על השאלה":
                    q3score = score_math_question(val["value"])
            elif question == "ForthQuestion":
                print("score Forth question")
                if val["value"] != "לא ענה על השאלה":
                    q4score = test_question_two(val["value"]["object1"], val["value"]["object2"],
                                                val["value"]["object3"], patient_details)
            elif question == "FifthQuestion":
                print("score Fifth question")
                if val["value"] != "לא ענה על השאלה":
                    if val["value"]["firstpic"] == patient_details['next test']['fifthQuestion']['pic1']:
                        q5score = q5score + 1
                    if val["value"]["secoundpic"] == patient_details['next test']['fifthQuestion']['pic2']:
                        q5score = q5score + 1
            elif question == "SixthQuestion":
                print("score Sixth question")
                if val["value"] != "לא ענה על השאלה":
                    if val["value"]["sentence"] == patient_details['next test']['sixthQuestion']['sentence']:
                        q6score = q6score + 1
            elif question == "SeventhQuestion":
                print("score Sevent question")
                if val["value"]:
                    q7score = 3
            elif question == "EigthQuestion":
                print("score Eigth question")
                if val["value"]:
                    q8score = 1
            elif question == "NineQuestion":
                print("score Nine question")
                if val["value"] != "לא ענה על השאלה":
                    q9score = num_of_words_in_string(str(val["value"]))
            elif question == "TenthQuestion":
                print("score Tenth question", val["value"])
                # determine_shapes_in_img(val["value"])
                print("determine shapes im img done")
            # print("q2score = " + q2score)
            # print("The score is ", location_score + time_score, " of 10")
        # db.child("Test").child(test).child(test).child("was_tested").update(True)
        return time_score, location_score, q2score, q3score, q4score, q5score, q6score, q7score, q8score, q9score \
            , q10score
    return -1, -1


# 4 versions possible for now
def getNextSecondQuestion(email):
    version = get_next_test_version_by_email(email)
    if version == 1:
        return {'object1': 'כדור', 'object2': 'דגל', 'object3': 'עץ'}
    elif version == 2:
        return {'object1': 'אגס', 'object2': 'שולחן', 'object3': 'חולצה'}
    elif version == 3:
        return {'object1': 'אבטיח', 'object2': 'ארון', 'object3': 'מכנסיים'}
    else:
        return {'object1': 'תפוח', 'object2': 'כיסא', 'object3': 'גרביים'}


def getNextThirdQuestion(email):
    version = get_next_test_version_by_email(email)
    if version == 1:
        return {'number': '100', 'deduction': '7', 'word': 'ארצות'}
    elif version == 2:
        return {'number': '100', 'deduction': '7', 'word': 'ארצות'}
    elif version == 3:
        return {'number': '100', 'deduction': '7', 'word': 'ארצות'}
    else:
        return {'number': '100', 'deduction': '7', 'word': 'ארצות'}


def getNextFifthQuestion(email):
    # עיפרון וסרגל
    version = get_next_test_version_by_email(email)
    if version == 1:
        return {'pic1': 'עיפרון', 'pic2': 'סרגל'}
    elif version == 2:
        return {'pic1': 'שולחן', 'pic2': 'כדור'}
    elif version == 3:
        return {'pic1': 'בלון', 'pic2': 'לימון'}
    else:
        return {'pic1': 'עיפרון', 'pic2': 'לימון'}


def getNextSixthQuestion(email):
    # קניתי אבטיח בשוק
    version = get_next_test_version_by_email(email)
    if version == 1:
        return {'sentence': 'לא כל הנוצץ זהב הוא'}
    elif version == 2:
        return {'sentence': 'התפוח לא נופל רחוק מהעץ'}
    elif version == 3:
        return {'sentence': 'אל תסתכל בקנקן אלה במה שיש בו'}
    else:
        return {'sentence': 'כל הדרכים מובילות לרומא'}


def getNextSeventhQuestion(email):
    version = get_next_test_version_by_email(email)
    if version == 1:
        return {'instructions': 'לחץ על דלת המקרר כדי לפתוח אותה ותגרור את החלב למפית האדומה שעל השולחן'}
    elif version == 2:
        return {'instructions': 'לחץ על דלת המקרר כדי לפתוח אותה ותגרור את הענבים למפית הכחולה שעל השולחן'}
    elif version == 3:
        return {'instructions': 'לחץ על דלת המקרר כדי לפתוח אותה ותגרור את העוף למפית הירוקה שעל השולחן'}
    else:
        return {'instructions': 'לחץ על דלת המקרר כדי לפתוח אותה ותגרור את הפחית למפית הצהובה שעל השולחן'}


def getNextEighthQuestion(email):
    # vertion1 = {'button1': 'red', 'button2': 'green', 'shape1': 'triangle', 'shape2': 'circle'}
    # vertion2 = {'button1': 'red', 'button2': 'green', 'shape1': 'triangle', 'shape2': 'circle'}
    # vertion3 = {'button1': 'red', 'button2': 'green', 'shape1': 'triangle', 'shape2': 'circle'}
    # vertion4 = {'button1': 'red', 'button2': 'green', 'shape1': 'triangle', 'shape2': 'circle'}
    return {'value': "not available"}


# remember to change if you had more versions of the test
def get_next_test_version_by_email(email):
    version = 1
    for patient in db.child("Patients").get().each():
        if patient.val()["patient details"]["email"] == email:
            version = patient.val()["patient details"]["test_number"]
    if version == 0:
        return 1
    # print(version)
    return version % 4
