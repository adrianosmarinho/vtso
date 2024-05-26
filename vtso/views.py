# Create your views here.
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.permissions import AllowAny

from vtso.models import Company
from vtso.serializers import CompanySerializer

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
