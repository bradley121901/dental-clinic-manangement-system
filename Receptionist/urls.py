from django.urls import URLPattern, path

from . import views

urlpatterns = [
    path("<str:ssn>", views.reception, name = "reception"),
    path("appointment/<str:patientSSN>/<str:ssn>", views.bookAppointment, name = "appointment"),
    path("<str:ssn>/<str:patientSSN>", views.patientInfo, name = "patientInfo"),
   
]