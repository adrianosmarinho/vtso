from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("companies/", views.CompanyList.as_view(), name="companies"),
    path("persons/", views.PersonList.as_view(), name="persons"),
    path("ships/", views.ShipList.as_view(), name="ships"),
]
