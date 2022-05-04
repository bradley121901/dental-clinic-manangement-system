from django import forms

class SearchForm(forms.Form):
    Patient_fname = forms.CharField(label = "Patient First name", max_length=30)
    Patient_lname = forms.CharField(label = "Patient Last name", max_length=30)


class AppointmentForm(forms.Form):    
    dentist_FN = forms.CharField(label = "Dentist First Name", max_length=30)
    dentist_LN = forms.CharField(label = "Dentist Last Name", max_length=30)
    appointment_type = forms.CharField(label = "Appointment Type", max_length=30)
    date = forms.CharField(label = "Date of Appointment yyyy-mm-dd", max_length=30)
    startTime = forms.CharField(label = "Appointment Start Time hh:mm", max_length=30)
    endTime = forms.CharField(label = "Appointment End Time hh:mm", max_length=30)

class CancelForm(forms.Form):
    appointment_ID = forms.IntegerField(label = "Appointment Id", min_value = 0)
