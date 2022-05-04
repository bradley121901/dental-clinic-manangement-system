from django import forms
from django.core.exceptions import ValidationError
import mysql.connector



class employee_register_form(forms.Form):
    CHOICES = [("dentist", 'Dentist'), ("receptionist", "Receptionist")]

    firstname = forms.CharField(label="firstname", max_length=30)
    lastname  = forms.CharField(label="lastname", max_length=30)
    housenum = forms.IntegerField(label="housenum", min_value=1)
    streetname = forms.CharField(label="streetname", max_length=30)
    city = forms.CharField(label="city", max_length=30)
    province = forms.CharField(label="province", max_length=30)
    role = forms.CharField(label="role", widget=forms.Select(choices=CHOICES))
    salary = forms.IntegerField(label="salary", min_value=0)
    ssn = forms.IntegerField(label="SSN", min_value=0)
    username = forms.CharField(label="username", max_length=30)
    password = forms.CharField(label="password", max_length=30)


#    custom validation
    def clean_username(self):
        db = mysql.connector.connect(
                    host ='us-cdbr-east-05.cleardb.net',
                    user ='be6fd11e32efb5',
                    passwd='2e25d6f3',
                    database = 'heroku_7f02c0751957843')
        mycursor = db.cursor(buffered=True)
        username = self.cleaned_data["username"]
        mycursor.execute("SELECT uname FROM user_table")
        for x in mycursor:
            if username == x[0]:
                raise ValidationError("Username is already taken")

        return username


class patient_register_form(forms.Form):
    firstname = forms.CharField(label="firstname", max_length=30)
    lastname = forms.CharField(label="lastname", max_length=30)
    housenum = forms.IntegerField(label="housenum", min_value=1)
    streetname = forms.CharField(label="streetname", max_length=30)
    city = forms.CharField(label="city", max_length=30)
    province = forms.CharField(label="province", max_length=30)
    gender = forms.CharField(label="gender", max_length=30)
    email = forms.EmailField(label="email", max_length=30)
    DOB = forms.CharField(label="date of birth (yyyy-mm-dd)")
    ssn = forms.IntegerField(label="SSN", min_value=0)
    username = forms.CharField(label="username", max_length=30)
    password = forms.CharField(label="password", max_length=30)


#custom validation
    def clean_username(self):
        db = mysql.connector.connect(
                    host ='us-cdbr-east-05.cleardb.net',
                    user ='be6fd11e32efb5',
                    passwd='2e25d6f3',
                    database = 'heroku_7f02c0751957843')
        mycursor = db.cursor(buffered=True)
        username = self.cleaned_data["username"]
        mycursor.execute("SELECT uname FROM user_table")
        for x in mycursor:
            if username == x[0]:
                raise ValidationError("Username is already taken")
        
        return username


