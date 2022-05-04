from django.urls import path
from loginregister import views


urlpatterns = [
    path('', views.landing_page),
    path('register', views.register),
    path("register/employee", views.employee_register),
    path("register/patient", views.patient_register),
]