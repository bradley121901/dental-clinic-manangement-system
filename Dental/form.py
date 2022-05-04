from django import forms

from dentist.views import appointment

class AppointmentForm(forms.Form):    
    dentist_FN = forms.CharField(label = "Dentist First Name", max_length=30)
    dentist_LN = forms.CharField(label = "Dentist Last Name", max_length=30)
    appointment_type = forms.CharField(label = "Appointment Type", max_length=30)
    date = forms.CharField(label = "Date of Appointment yyyy-mm-dd", max_length=30)
    startTime = forms.CharField(label = "Appointment Start Time hh:mm", max_length=30)
    endTime = forms.CharField(label = "Appointment End Time hh:mm", max_length=30)


class ReviewForm(forms.Form):
    patientSSN = forms.IntegerField(label = "Patient SSN",min_value = 0)
    professionalism = forms.IntegerField(label = "Professionalism of Employees",min_value = 0, max_value = 10)
    communication = forms.IntegerField(label = "Communication of Employees",min_value = 0, max_value = 10)
    cleanliness = forms.IntegerField(label = "Cleanliness",min_value = 0, max_value = 10)
    value = forms.IntegerField(label = "Value",min_value = 0, max_value = 10)

class CancelForm(forms.Form):
    appointment_ID = forms.IntegerField(label = "Appointment Id", min_value = 0)

