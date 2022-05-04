from django.urls import URLPattern, path

from . import views

urlpatterns = [
    path("<str:ssn>", views.patient, name = "patient"),
    path("appointment/<str:ssn>", views.appointment, name = "appointment"),
    path("appointment/view/<str:ssn>", views.viewAppointment, name = "viewAppointment"),
    path("records/<str:ssn>",views.viewRecords, name = "viewRecords"),
    path("reviews/<str:ssn>",views.leaveReview, name = "leaveReview"),
    path("invoices/<str:ssn>",views.invoices, name = "invoices"),
    path("invoices/payement/<str:ssn>",views.payement, name = "payement"),
    path("appointments/view/late/<str:ssn>/<str:appointmentID>",views.cancellation, name = "cancellation")
]