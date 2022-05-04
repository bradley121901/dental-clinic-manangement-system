from django.urls import URLPattern, path

from . import views

urlpatterns = [
    path("<str:ssn>", views.landing),
    path("upcoming-appointments/<str:ssn>", views.appointment),
    path("patient-records/<str:patientName>",views.patientRecords),
    path("branch-details/<str:ssn>",views.branchDetails)
]