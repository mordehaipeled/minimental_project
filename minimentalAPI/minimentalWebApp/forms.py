from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.forms import DateInput

from .models import Doctor, Patient, Test
# with the forms you can build a html form page


class Login(forms.Form):
    email = forms.EmailField(required=True, validators=[validate_email], max_length=256, label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label="Password", min_length=8)


class RegisterFormHeb(UserCreationForm):  # django registration form
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'סיסמא'
        self.fields['password2'].label = 'אישור סיסמא'
        self.fields['password1'].help_text = "<li>הסיסמה שלך לא יכולה להיות דומה מדי למידע האישי האחר שלך.</li>" \
                                             "<li>הסיסמה שלך חייבת להכיל לפחות 8 תווים.</li>" \
                                             "<li>הסיסמה שלך לא יכולה להיות סיסמה נפוצה.</li>" \
                                             "<li>הסיסמה שלך חייבת להכיל אותיות ומספרים לחלוטין.</li>"
        self.fields['password2'].help_text = '<li>אנא הזן סיסמא בשנית.</li>'
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = User
        fields = ("email", "password1", "password2", "first_name", "last_name")
        labels = {
            "email": "אימייל",
            "first_name": "שם פרטי",
            "last_name": "שם משפחה",
        }
        attrs = {
            'dir': 'rtl',
        }


class RegisterForm(UserCreationForm):  # django registration form
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirm Password'
        self.fields['password1'].help_text = "<li>Your password cannot be similar to other privet information.</li>" \
                                             "<li>Password must contain at least 8 characters</li>" \
                                             "<li>Password cannot be a commonly used password.</li>" \
                                             "<li>Password must contain letters and numbers only.</li>"
        self.fields['password2'].help_text = '<li>Please fill your password again.</li>'
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = User
        fields = ("email", "password1", "password2", "first_name", "last_name")
        labels = {
            "email": "Email",
            "first_name": "Given name",
            "last_name": "Last name",
        }
        attrs = {
            'dir': 'rtl',
        }


class DoctorRegisterForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ()
        exclude = ('user',)  # this should be removed


class DateInput(forms.DateInput):
    input_type = 'date'


class PatientRegisterFormHeb(forms.ModelForm):
    id = forms.CharField(label="תעודת זהות", )
    date_of_birth = forms.DateField(widget=DateInput, label="תאריך לידה", required=False)
    country = forms.CharField(label="מדינה", required=False)
    floor = forms.CharField(label="קומה", required=False)
    street = forms.CharField(label="שם רחוב", required=False)
    apartment = forms.CharField(label="דירה", required=False)
    city = forms.CharField(label="עיר", required=False)
    area = forms.CharField(label="אזור", required=False)

    class Meta:
        model = Patient
        fields = ("id", "date_of_birth", "country", "floor", "street", "apartment", "city", "area")
        exclude = ()  # this should be removed
        # fields = "__all__"


class PatientRegisterForm(forms.ModelForm):
    id = forms.CharField(label="ID", )
    date_of_birth = forms.DateField(widget=DateInput, label="Birthdate", required=False)
    country = forms.CharField(label="Country", required=False)
    floor = forms.CharField(label="Floor", required=False)
    street = forms.CharField(label="Street name", required=False)
    apartment = forms.CharField(label="Apartment number", required=False)
    city = forms.CharField(label="City", required=False)
    area = forms.CharField(label="Area", required=False)

    class Meta:
        model = Patient
        fields = ("id", "date_of_birth", "country", "floor", "street", "apartment", "city", "area")
        exclude = ()  # this should be removed
        # fields = "__all__"


class TestRegisterFormHeb(forms.ModelForm):
    next_test_date = forms.DateField(widget=DateInput, label="תאריך מבחן")
    isInHospital = forms.BooleanField(label="נבחן בבית החולים")

    class Meta:
        model = Test
        fields = ("next_test_date", "isInHospital")
        exclude = ()


class TestRegisterForm(forms.ModelForm):
    next_test_date = forms.DateField(widget=DateInput, label="Test date")
    isInHospital = forms.BooleanField(label="Test in Hospital")

    class Meta:
        model = Test
        fields = ("next_test_date", "isInHospital")
        exclude = ()
