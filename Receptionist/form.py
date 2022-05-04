from django import forms
from django.core.exceptions import ValidationError
import mysql.connector

from django.core.exceptions import ValidationError
import mysql.connector


db = mysql.connector.connect(
    host ='us-cdbr-east-05.cleardb.net',
    user ='be6fd11e32efb5',
    passwd='2e25d6f3',
    database = 'heroku_7f02c0751957843')

mycursor = db.cursor(buffered=True)



db = mysql.connector.connect(
    host ='us-cdbr-east-05.cleardb.net',
    user ='be6fd11e32efb5',
    passwd='2e25d6f3',
    database = 'heroku_7f02c0751957843')

mycursor = db.cursor(buffered=True)

class findPatient(forms.Form):
    patientSSN = forms.IntegerField(label = "Patient SSN", min_value = 0)   

class patient_register_form(forms.Form):
    firstname = forms.CharField(label="firstname", max_length=30)
    lastname = forms.CharField(label="lastname", max_length=30)
    housenumber = forms.IntegerField(label="housenum", min_value=30)
    streetname = forms.CharField(label="streetname", max_length=30)
    city = forms.CharField(label="city", max_length=30)
    province = forms.CharField(label="province", max_length=30)
    gender = forms.CharField(label="gender", max_length=30)
    email = forms.EmailField(label="email", max_length=30)
    dob = forms.CharField(label="date of birth (yyyy-mm-dd)")
    SSN = forms.IntegerField(label="SSN", min_value=0)

    def check_ssn(self):
        ssn = self.cleaned_data["SSN"]
        mycursor.execute("SELECT SSN FROM patient")
        for x in mycursor:
            print(ssn)
            if ssn == x[9]:
                raise ValidationError("SSN is already taken")

        return ssn


class appointment_form(forms.Form):
    patientSSN = forms.IntegerField(label="patientSSN", min_value=0)
    dentistSSN = forms.IntegerField(label="dentistSSN", min_value=0)

class AppointmentForm(forms.Form):    
    dentist_FN = forms.CharField(label = "Dentist First Name", max_length=30)
    dentist_LN = forms.CharField(label = "Dentist Last Name", max_length=30)
    appointment_type = forms.CharField(label = "Appointment Type", max_length=30)
    date = forms.CharField(label = "Date of Appointment yyyy-mm-dd", max_length=30)
    startTime = forms.CharField(label = "Appointment Start Time hh:mm", max_length=30)
    endTime = forms.CharField(label = "Appointment End Time hh:mm", max_length=30)
