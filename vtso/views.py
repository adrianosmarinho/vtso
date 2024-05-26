# Create your views here.
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.permissions import AllowAny

from vtso.models import Company, Harbour, Person, Ship
from vtso.serializers import (
    CompanySerializer,
    HarbourSerializer,
    PersonSerializer,
    ShipSerializer,
)

# from django.shortcuts import render


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


class HarbourList(generics.ListCreateAPIView):
    """
    View for /vtso/harbours endpoint
    TODO: add authentication
    """

    queryset = Harbour.objects.all()
    serializer_class = HarbourSerializer
    permission_classes = [AllowAny]
