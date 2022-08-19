from abc import ABC

from rest_framework import serializers
from .models import Patient, Doctor


# where made for use in an api that we handed up not doing


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'email', 'dateOfBirth', 'country', 'floor', 'street', 'apartment', 'city']
    # first_name = serializers.CharField(max_length=100)
    # last_name = serializers.CharField(max_length=100)
    # email = serializers.EmailField(max_length=100)
    # address = serializers.CharField(max_length=300)
    # dateOfBirth = serializers.DateField()
    #
    # def create(self, validated_data):
    #     return Patient.create(validated_data)
    #
    # def update(self, instance, validated_data):
    #     instance.givenName = validated_data.get('givenName', instance.givenName)
    #     instance.lastName = validated_data.get('lastName', instance.lastName)
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.address = validated_data.get('address', instance.address)
    #     instance.dateOfBirth = validated_data.get('dateOfBirth', instance.dateOfBirth)
    #     instance.save()
    #     return instance


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'password', 'email']

