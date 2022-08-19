from datetime import datetime, date
from json import dumps
import requests
from PIL import Image
from django.views.decorators.cache import cache_control
from django.contrib import auth
from django.shortcuts import render, redirect
import firebase_admin
from django.shortcuts import HttpResponse
import pyrebase
from firebase_repo import db, auth_fb, check_if_patient_exists, check_if_doctor_exists \
    , getNextSecondQuestion, getNextThirdQuestion, getNextFifthQuestion, getNextSixthQuestion, getNextSeventhQuestion \
    , getNextEighthQuestion, storage, score
from django.views.decorators.cache import cache_control
from django.shortcuts import render, redirect
from .forms import Login, RegisterForm, DoctorRegisterForm, PatientRegisterForm, TestRegisterForm


# Create your views here.
# TODO: 1) questions 7 and 8 only have true or false in the db and we want to save what they were asked to do
#  you can add it at the function validate test, or ask the android team to add it with the test.
#

# Handles login users
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def postsign(request):
    print("postsign-webapp")
    print(request)
    email, password = None, None
    form = Login()
    if request.method == "GET":
        if request.session.get('uid') is not None:
            return redirect("/home", )
        if request.GET != {}:
            print(request.GET["len"] == "en")
        return render(request, "login.html", {"form": form})

    if request.method == "POST":
        form = Login(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            print(email)
            password = form.cleaned_data['password']
            print(password)
        try:
            user = auth_fb.sign_in_with_email_and_password(email, password)
            print(user['localId'])
            current_doctor_id = db.child("Doctors").child(user['localId']).get()
            print(current_doctor_id.val())
            name = current_doctor_id.val()['first_name'] + " " + current_doctor_id.val()['last_name']
            request.session['uid'] = str(user['idToken'])
            request.session['name'] = name
            request.session['email'] = user['email']
            return redirect("/home")
        except:
            form.add_error('password', "אימייל או סיסמא אינם מתאימים!")
            return render(request, "login.html", {'form': form})


# Rendering home page
@cache_control(no_cache=False, must_revalidate=True, no_store=True)
def home(request):
    # print("home-webapp")
    # return render(request, "dashboard.html")
    if request.method == "GET":
        if request.session.get('uid'):
            return render(request, "dashboard.html")
        else:
            return redirect("/")


# Handles user logout
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_logout(request):
    if request.session.get('uid') is not None:
        try:
            del request.session['uid']
            auth.current_user = None
            request.session.clear()
            return redirect("/")
        except KeyError:
            pass
    else:
        return redirect("/")


# organising the tests
def sortMyDict(mydict):
    print("sort begin")
    d = {'FirstQuestion': {"value": "", "score": "0"}, 'SecondQuestion': {"value": "", "score": "0"},
         'MathQuestion': {"value": "", "score": "0"},
         'ForthQuestion': {"value": "", "score": "0"}, 'FifthQuestion': {"value": "", "score": "0"},
         'SixthQuestion': {"value": "", "score": "0"},
         'SeventhQuestion': {"value": "", "score": "0"}, 'EigthQuestion': {"value": "", "score": "0"},
         'NineQuestion': {"value": "", "score": "0"}, 'TenthQuestion': {"value": "", "score": "0"},
         'final_score': {"value": "0"}}
    for i in d.keys():
        try:
            d[i] = mydict[i]
        except Exception as e:
            print("Error: ", e)
    return d


# not all tests were made equal, firebase will not save an empty question, all the lines in the table must be the same,
# so I add the missing data.
def validate_test(test, uid):
    print("validate test")
    testv = db.child("Test").child(uid).child(test).get()
    # print(testv.val())
    q1 = False
    q2 = False
    q3 = False
    q4 = False
    q5 = False
    q6 = False
    q7 = False
    q8 = False
    q9 = False
    q10 = False
    was_tested = False
    for q in testv.val():
        # print(q)
        if q == "FirstQuestion":
            q1 = True
        elif q == "SecondQuestion":
            q2 = True
        elif q == "MathQuestion":
            q3 = True
        elif q == "ForthQuestion":
            q4 = True
        elif q == "FifthQuestion":
            q5 = True
        elif q == "SixthQuestion":
            q6 = True
        elif q == "SeventhQuestion":
            q7 = True
        elif q == "EigthQuestion":
            q8 = True
        elif q == "NineQuestion":
            q9 = True
        elif q == "TenthQuestion":
            q10 = True
        elif q == "WordQuestion":
            q3 = True
        elif q == "was_tested":
            was_tested = True
    if not q1:
        db.child("Test").child(uid).child(test).child("FirstQuestion").child("value").set("לא ענה על השאלה")
        db.child("Test").child(uid).child(test).child("FirstQuestion").child("score").set(["0", "0"])
    if not q2:
        db.child("Test").child(uid).child(test).child("SecondQuestion").child("value").set("לא ענה על השאלה")
        db.child("Test").child(uid).child(test).child("SecondQuestion").child("score").set(["0"])
    if not q3:
        db.child("Test").child(uid).child(test).child("MathQuestion").child("value").set("לא ענה על השאלה")
        db.child("Test").child(uid).child(test).child("MathQuestion").child("score").set(["0"])
    if not q4:
        db.child("Test").child(uid).child(test).child("ForthQuestion").child("value").set("לא ענה על השאלה")
        db.child("Test").child(uid).child(test).child("ForthQuestion").child("score").set(["0"])
    if not q5:
        db.child("Test").child(uid).child(test).child("FifthQuestion").child("value").set("לא ענה על השאלה")
        db.child("Test").child(uid).child(test).child("FifthQuestion").child("score").set(["0"])
    if not q6:
        db.child("Test").child(uid).child(test).child("SixthQuestion").child("value").set("לא ענה על השאלה")
        db.child("Test").child(uid).child(test).child("SixthQuestion").child("score").set(["0"])
    if not q7:
        db.child("Test").child(uid).child(test).child("SeventhQuestion").child("value").set("לא ענה על השאלה")
        db.child("Test").child(uid).child(test).child("SeventhQuestion").child("score").set(["0"])
    if not q8:
        db.child("Test").child(uid).child(test).child("EigthQuestion").child("value").set("לא ענה על השאלה")
        db.child("Test").child(uid).child(test).child("EigthQuestion").child("score").set(["0"])
    if not q9:
        db.child("Test").child(uid).child(test).child("NineQuestion").child("value").set("לא ענה על השאלה")
        db.child("Test").child(uid).child(test).child("NineQuestion").child("score").set(["0"])
    if not was_tested:
        db.child("Test").child(uid).child(test).child("was_tested").set(False)
    pass


# returns all urls (if any exist) for pics uploaded by the patient
# TODO: the open img function costs alot of time, so you may want to find a different solution once you have a big db
def getPatientImeges(url_string, test_num):
    print("get patient img")
    i = 1
    all_tests_img = {}
    while i < test_num:
        img_url_dic = {}
        try:
            url = storage.child(url_string + "test" + str(i) + "/file1.JPEG").get_url('url')
            img = Image.open(requests.get(url, stream=True).raw)
            print(img.format)
            has_more_pics = False
            j = 1
            if img.format == "JPEG":
                has_more_pics = True
            while has_more_pics:
                url = storage.child(url_string + "test" + str(i) + "/file" + str(j) + ".JPEG").get_url('url')
                j = j + 1
                img = Image.open(requests.get(url, stream=True).raw)
                if img.format != "JPEG":
                    has_more_pics = False
                else:
                    img_url_dic["pic_" + str(j)] = url
        except Exception as e:
            print(e)
        all_tests_img["test"+str(i)] = img_url_dic
        i = i + 1
    print(test_num)
    return all_tests_img


# collects and organise all the patients details, tests, scores (calculate the score for latest test), pics ect.
# pass the info to the html page
@cache_control(no_cache=False, must_revalidate=True, no_store=True)
def patient_detail(request):
    print("patient_details")
    # print(request.GET)
    if request.session.get('uid') is not None:
        patient_id = request.GET.get("patient_id", 0)
        for patient in db.child("Patients").get().each():
            if patient.val()["id"] == patient_id:
                uid = patient.key()
                request.session['patient_key'] = patient.key()
                patient_details = patient.val()
                patient_tests = {}
                for test in db.child('Test').get().each():
                    if test.key() == patient.key():
                        patient_tests = test.val()
                for test in patient_tests:
                    # print(test)
                    if test != "value":
                        validate_test(test, uid)
                        picurl = storage.child("/TenthQuestion Pic/" + patient_tests['value'] +
                                               "/" + test + "/drawImage.jpg").get_url('url')
                        patient_tests[test] = sortMyDict(patient_tests[test])
                        patient_tests[test]["TenthQuestion"] = {'value': picurl}
                        db.child("Test").child(patient.key()).child(test).child("TenthQuestion").child("value").set(
                            picurl)
                        # print(patient_details["patient details"]["test_number"])
                        if test == "test" + str(patient_details["patient details"]["test_number"]):
                            try:
                                if not db.child("Test").child(uid).child(test).child("was_tested").get().val():
                                    timescore, locationscore, q2score, q3score, q4score, q5score, q6score, q7score, \
                                    q8score, q9score, q10score = score(db.child("Test").child(patient_tests['value'])
                                                                       .child(test).get(), patient_details)
                                    db.child("Test").child(uid).child(test).child("was_tested").set(True)
                                    final = timescore + locationscore + q2score + q3score + q4score + q5score + q6score + q7score + q8score + q9score + q10score
                                    db.child("Test").child(patient.key()).child(test).child("FirstQuestion"). \
                                        child("score").set([timescore, locationscore])
                                    db.child("Test").child(patient.key()).child(test).child("SecondQuestion"). \
                                        child("score").set([q2score])
                                    db.child("Test").child(patient.key()).child(test).child("MathQuestion"). \
                                        child("score").set([q3score])
                                    db.child("Test").child(patient.key()).child(test).child("ForthQuestion"). \
                                        child("score").set([q4score])
                                    db.child("Test").child(patient.key()).child(test).child("FifthQuestion"). \
                                        child("score").set([q5score])
                                    db.child("Test").child(patient.key()).child(test).child("SixthQuestion"). \
                                        child("score").set([q6score])
                                    db.child("Test").child(patient.key()).child(test).child("SeventhQuestion"). \
                                        child("score").set([q7score])
                                    db.child("Test").child(patient.key()).child(test).child("EigthQuestion"). \
                                        child("score").set([q8score])
                                    db.child("Test").child(patient.key()).child(test).child("NineQuestion"). \
                                        child("score").set([q9score])
                                    db.child("Test").child(patient.key()).child(test).child("TenthQuestion"). \
                                        child("score").set([q10score])
                                    db.child("Test").child(patient.key()).child(test).child("final_score").\
                                        child("value").set(final)
                            except Exception as e:
                                print("error: ", e)
                # patient_tests = db.child('Test').order_by_child('token/patient_id').equal_to(patient_id).get()
                # print(patient_details)
                # print(patient_tests)
                if patient_tests != {}:
                    patient_tests2 = db.child("Test").child(uid).get().val()
                    for test in patient_tests2:
                        if test != "value":
                            patient_tests2[test] = sortMyDict(patient_tests2[test])
                    print("------------------------", patient_tests['value'])
                    patient_imeges = getPatientImeges("/TenthQuestion Pic/" + str(patient_tests['value']) + "/",
                                                      len(patient_tests2))
                    return render(request, "patient_page.html",
                                  {'patient_details': patient_details.get('patient details'),
                                   'patient_tests': patient_tests2,
                                   'next_test_date': patient_details.get('next test').get('test date'),
                                   'has_permission': patient_details.get('patient details').get('has permission'),
                                   'patient_imeges': patient_imeges})
                else:
                    return render(request, "patient_page.html",
                                  {'patient_details': patient_details.get('patient details'),
                                   'patient_tests': None,
                                   'next_test_date': patient_details.get('next test').get('test date'),
                                   'has_permission': patient_details.get('patient details').get('has permission')
                                   })
        return redirect("/home")


# Checking if patient is exists
def patient_detail_check(request):
    print("patient_detail_check")
    patient_id = request.GET.get('data')
    for patient in db.child("Patients").get().each():
        # print(patient.val()["id"])
        if patient.val()["id"] == patient_id:
            return HttpResponse("True")
    return HttpResponse("False")


# Handling registering new doctor
@cache_control(no_cache=False, must_revalidate=True, no_store=True)
def register_new_doctor(response):
    print("register")
    if response.method == "POST":
        print("post")
        django_form = RegisterForm(response.POST)  # django User
        doctor_form = DoctorRegisterForm(response.POST)  # our user
        if django_form.is_valid() and doctor_form.is_valid():
            print("valid")
            first_name = django_form.cleaned_data["first_name"]
            last_name = django_form.cleaned_data["last_name"]
            email = django_form.cleaned_data["email"]
            password = django_form.cleaned_data["password1"]
            doctor = auth_fb.create_user_with_email_and_password(email=email, password=password)
            if doctor:
                data = {
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                }
                db.child("Doctors").child(doctor['localId']).set(data)
        else:
            print("not valid")
            return render(response, "register.html", {'form': django_form, 'ourform': doctor_form})
        return redirect("/")
    else:
        print("not post")
        form = RegisterForm()
        doctor_form = DoctorRegisterForm()
        return render(response, "register.html", {'form': form, 'ourform': doctor_form})


# Handling registering new patient
@cache_control(no_cache=False, must_revalidate=True, no_store=True)
def register_new_patient(response):
    print("register_new_patient")
    if response.method == "POST":
        django_form = RegisterForm(response.POST)  # django User
        patient_form = PatientRegisterForm(response.POST)  # our user
        print(patient_form.is_valid())
        if django_form.is_valid() and patient_form.is_valid():
            first_name = django_form.cleaned_data["first_name"]
            last_name = django_form.cleaned_data["last_name"]
            patientid = patient_form.cleaned_data["id"]
            email = django_form.cleaned_data["email"]
            password = django_form.cleaned_data["password1"]
            country = patient_form.cleaned_data["country"]
            date_of_birth = str(patient_form.cleaned_data['date_of_birth'])
            floor = str(patient_form.cleaned_data['floor'])
            street = str(patient_form.cleaned_data['street'])
            apartment = str(patient_form.cleaned_data['apartment'])
            city = str(patient_form.cleaned_data['city'])
            area = str(patient_form.cleaned_data['area'])
            patient = auth_fb.create_user_with_email_and_password(email=email, password=password)
            # TODO: revers the date string.
            data = {
                'doctor': response.session.get('email'),
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'country': country,
                'date_of_birth': date_of_birth,
                'floor': floor,
                'apartment': apartment,
                'city': city,
                'street': street,
                'area': area,
                'has permission': False,
                'is_in_hospital': True,
                'test_number': 0,
            }
            nextTest = {
                'test date': dumps(datetime.now(), default=json_serial),
                'secondQuestion': getNextSecondQuestion(email),
                'thirdQuestion': getNextThirdQuestion(email),
                'fifthQuestion': getNextFifthQuestion(email),
                'sixthQuestion': getNextSixthQuestion(email),
                'seventhQuestion': getNextSeventhQuestion(email),
                'eighthQuestion': getNextEighthQuestion(email),
            }
            db.child("Patients").child(patient['localId']).set({'id': patientid})
            db.child("Patients").child(patient['localId']).child("patient details").set(data)
            db.child("Patients").child(patient['localId']).child("next test").set(nextTest)
        else:
            return render(response, "add_new_patient.html", {'form': django_form, 'ourform': patient_form})
        return redirect("/home")
    else:  # Get
        if response.session.get('uid') is not None:
            form = RegisterForm()
            patient_form = PatientRegisterForm()
            return render(response, "add_new_patient.html", {'form': form, 'ourform': patient_form})
        else:
            return redirect("/")


# Checking if user(doctor or patient) already exist
def validate_email(request):
    print("validate_email")
    email = request.POST.get('email')
    if email == '':
        return HttpResponse("FillEmail")
    if check_if_patient_exists(email) or check_if_doctor_exists(email):
        return HttpResponse("EmailExists")
    return HttpResponse("Valid")


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


# preparing for a new test, includes changing arguments in the patient details and next test.
@cache_control(no_cache=False, must_revalidate=True, no_store=True)
def make_new_test(request):
    print("make_new_test")
    # print(request.POST)
    email = request.POST.get('email')
    for patient in db.child("Patients").get().each():
        if patient.val()["patient details"]["email"] == email:
            # print(db.child("Test").child(patient.key()).get().val())
            num_of_tests = 0
            if db.child("Test").child(patient.key()).get().val() is not None:
                # print("in if test number")
                for test in db.child("Test").child(patient.key()).get().each():
                    num_of_tests = num_of_tests + 1
                # print(num_of_tests)
            if num_of_tests != 0:
                num_of_tests = num_of_tests - 1
            data = {"has permission": True, "is_in_hospital": request.POST.get('is_in_hospital') == "true",
                    "test_number": num_of_tests + 1,
                    }
            db.child("Patients").child(patient.key()).child("patient details").update(data)
            next_test = {
                'test date': request.POST.get('date'),
                'secondQuestion': getNextSecondQuestion(email),
                'thirdQuestion': getNextThirdQuestion(email),
                'fifthQuestion': getNextFifthQuestion(email),
                'sixthQuestion': getNextSixthQuestion(email),
                'seventhQuestion': getNextSeventhQuestion(email),
                'eighthQuestion': getNextEighthQuestion(email),
            }
            db.child("Patients").child(patient.key()).child("next test").set(next_test)

            return HttpResponse("True")
    return HttpResponse("False")
    # form = TestRegisterForm()
    # return render(request, "make_new_test.html",
    #               {'patient_details': request, 'form': form})


# returns the patient uid by finding the right email
def get_uid_by_email(email):
    patients = db.child("Patients").get()
    for patient in patients.each():
        if patient.val()['patient details']['email'] == email:
            return patient.key()
    return "not found"


# if the doctor want to overrule the score given automatically this function handles all relevant buttons.
# returns True on successes and False if fails.
def edit_score(response):
    print("edit score")
    print(response.POST)
    uid = get_uid_by_email(response.POST.get("email"))
    grade = db.child("Test").child(uid).child(response.POST.get('test')).child(response.POST.get('question')). \
        child("score").get().val()
    if grade is None:
        grade = [0, 0]
    change = 0
    print(grade)
    if response.POST.get('question') == "FirstQuestion":
        if response.POST.get('place') == '1':
            change = int(response.POST.get('score')) - int(grade[1])
            grade[1] = response.POST.get('score')
        else:
            change = int(response.POST.get('score')) - int(grade[0])
            grade[0] = response.POST.get('score')
    else:
        change = int(response.POST.get('score')) - int(grade[0])
        grade = [response.POST.get('score')]
    if db.child("Test").child(uid).child(response.POST.get('test')).child("final_score").child("value").get().val() is not None:
        final = int(db.child("Test").child(uid).child(response.POST.get('test')).child("final_score").child("value").get().val()) + int(change)
        print(final, change)
    try:
        db.child("Test").child(uid).child(response.POST.get('test')).child(response.POST.get('question')). \
            child("score").set(grade)
        db.child("Test").child(uid).child(response.POST.get('test')).child("final_score").update({"value": str(final)})
        return HttpResponse("True")
    except Exception as e:
        print("error: ", e)
        return HttpResponse("False")
