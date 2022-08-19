from django.db import models


# Create your models here.

# the models are mainly for the forms

class Patient(models.Model):
    id = models.CharField(max_length=10, primary_key="true")
    first_name = models.CharField(max_length=100, default='mor')
    last_name = models.CharField(max_length=100, default='mor')
    dateOfBirth = models.DateField(default='01.01.2022')
    country = models.CharField(max_length=50, default='Test Land')
    floor = models.CharField(max_length=20, default='4')
    street = models.CharField(max_length=50, default='Test Street')
    apartment = models.CharField(max_length=10, default='12')
    city = models.CharField(max_length=50, default='Test City')
    area = models.CharField(max_length=20, default="מרכז")

    def __str__(self):
        return self.first_name + " " + self.last_name


class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, default="mor")
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    # what else do we need here?????

    def __str__(self):
        return self.first_name + " " + self.last_name


class Test(models.Model):
    patient_id = models.CharField(max_length=10)
    test_id = models.IntegerField()
    next_test_date = models.DateField()
    next_test_info = models.CharField(max_length=200)
    test_results = models.CharField(max_length=200)
    has_permission = models.BooleanField()
    test_scores = models.CharField(max_length=100)
    was_scored = models.BooleanField()
    isInHospital = models.BooleanField()

    def __str__(self):
        return "patient id: " + self.patient_id + "test number: " + self.test_id
