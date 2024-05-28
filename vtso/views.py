# Create your views here.
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny

from vtso.models import Company, Harbour, Person, Ship, Visit
from vtso.serializers import (
    CompanySerializer,
    HarbourDetailsSerializer,
    HarbourSerializer,
    PersonSerializer,
    ShipSerializer,
    ShipVisitSerializer,
    VisitSerializer,
)


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class CompanyList(generics.ListCreateAPIView):
    """
    View for /vtso/companies endpoint
    TODO: add authentication
    TODO: (bonus) change the view to disallow blank Company names

    Args:
        generics (_type_): _description_
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [AllowAny]


class PersonList(generics.ListCreateAPIView):
    """
    View for /vtso/persons endpoint
    TODO: add authentication
    """

    queryset = Person.objects.select_related("company").all()
    serializer_class = PersonSerializer
    permission_classes = [AllowAny]


class ShipList(generics.ListCreateAPIView):
    """
    View for /vtso/ships endpoint
    TODO: add authentication
    """

    queryset = Ship.objects.select_related("company").all()
    serializer_class = ShipSerializer
    permission_classes = [AllowAny]


class ShipDetail(generics.RetrieveUpdateAPIView):
    """
    View for /vtso/ships/<int:pk>/ endpoint
    A GET request will retrieve de details of a given Ship, while
    a PUT or PATCH request will update a given Ship.
    TODO: add authentication
    """

    queryset = Ship.objects.select_related("company").all()
    serializer_class = ShipSerializer
    permission_classes = [AllowAny]


class ShipVisits(generics.ListAPIView):
    """
    View for /vtso/ships/<int:pk>/visits/ endpoint.
    """

    serializer_class = ShipVisitSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        ship_id = self.kwargs["pk"]
        try:
            ship = Ship.objects.get(pk=ship_id)
            return Visit.objects.filter(ship=ship)
        except Ship.DoesNotExist as e:
            raise NotFound("Ship not found") from e


class HarbourList(generics.ListCreateAPIView):
    """
    View for /vtso/harbours endpoint
    TODO: add authentication
    """

    queryset = Harbour.objects.all()
    serializer_class = HarbourSerializer
    permission_classes = [AllowAny]


class HarbourDetails(generics.RetrieveAPIView):
    """
    View for /vtso/harbours/id/details/ endpoint
    A GET request will retrieve de details of a given Harbour, including
    a list of Ships currently docked at it.
    TODO: add authentication
    """

    queryset = Harbour.objects.all()
    serializer_class = HarbourDetailsSerializer
    permission_classes = [AllowAny]


class VisitList(generics.ListCreateAPIView):
    """
    View for /vtso/visits endpoint
    TODO: add authentication
    """

    queryset = Visit.objects.select_related("harbour", "ship").all()
    serializer_class = VisitSerializer
    permission_classes = [AllowAny]
