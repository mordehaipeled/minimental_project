# TODO: why is this here again? what? the debugger wont run unless its here? whatever
# this is an empty copy of firebaserepo page

import os

from pyasn1.compat.octets import null
from pyrebase import pyrebase

config = {
    "apiKey": os.getenv("apiKey"),
    "authDomain": os.getenv("authDomain"),
    "databaseURL": os.getenv("databaseURL"),
    "storageBucket": os.getenv("storageBucket")
}

firebase = pyrebase.initialize_app(config)
auth_fb = firebase.auth()
db = firebase.database()
storage = firebase.storage()


def get_patient(patient_key):
    patients = db.child('Patients').get()
    for patient in patients.each():
        if patient_key == patient.val().get('user_details').get('patient_key'):
            return patient
    return null


def get_test(test_id):
    tests = db.child('Tests').get()
    for test in tests.each():
        if test_id == test.val().get('test_details').get('test_id'):
            return test
    return null


def check_if_patient_exists(patient_key):
    patients = db.child('Patients').get()
    for patient in patients.each():
        print(patient.val())
        if patient_key == patient.val().get('patient_details'):
            return True
    return False


def check_if_doctor_exists(email):
    doctors = db.child('Doctors').get()
    for doctor in doctors.each():
        if email == doctor.val().get('details').get('email'):
            return True
    return False


def score(test):
    pass


def getNextSecondQuestion(email):
    return {'object1': 'table', 'object2': 'ball', 'object3': 'rug'}


def getNextThirdQuestion(email):
    return {'number': '100', 'deduction': '7', 'word': 'table'}


def getNextFifthQuestion(email):
    return {'pic1': 'pic1', 'pic2': 'pic2'}


def getNextSixthQuestion(email):
    return {'sentence': 'Know thy enemy'}


def getNextSeventhQuestion(email):
    return {'object1': 'table', 'object2': 'ball', 'object3': 'rug', 'audio instructions': 'audio file'}


def getNextEighthQuestion(email):
    return {'button1': 'red', 'button2': 'green', 'shape1': 'triangle', 'shape2': 'circle'}
