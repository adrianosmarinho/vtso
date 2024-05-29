from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken import views as auth_token_views

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("companies/", views.CompanyList.as_view(), name="companies"),
    path("persons/", views.PersonList.as_view(), name="persons"),
    # list or create a ship
    path("ships/", views.ShipList.as_view(), name="ships"),
    # retrieve or update a ship
    path("ships/<int:pk>/", views.ShipDetail.as_view(), name="ship_detail"),
    # retrieve the harbours a ship has visited
    path("ships/<int:pk>/visits/", views.ShipVisits.as_view(), name="ship_visits"),
    path("harbours/", views.HarbourList.as_view(), name="harbours"),
    # retrieve a harbour with docked ships
    path(
        "harbours/<int:pk>/details/",
        views.HarbourDetails.as_view(),
        name="harbour_details",
    ),
    path("visits/", views.VisitList.as_view(), name="visits"),
    # generates and downloads an OpenAPI yaml schema
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # OpenAPI Swagger UI
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/tokens/obtain", auth_token_views.obtain_auth_token),
]
