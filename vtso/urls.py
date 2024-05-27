from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("companies/", views.CompanyList.as_view(), name="companies"),
    path("persons/", views.PersonList.as_view(), name="persons"),
    # list or create a ship
    path("ships/", views.ShipList.as_view(), name="ships"),
    # retrieve or update a ship
    path("ships/<int:pk>/", views.ShipDetail.as_view(), name="ship_detail"),
    path("harbours/", views.HarbourList.as_view(), name="harbours"),
    # retrieve a harbour
    path(
        "harbours/<int:pk>/details/",
        views.HarbourDetails.as_view(),
        name="harbour_details",
    ),
    # TODO: consider renaming HarbourLog to Visit
    path("harbourlogs/", views.HarbourLogList.as_view(), name="harbourlogs"),
]
