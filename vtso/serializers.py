from rest_framework import serializers

from vtso.models import Company, Harbour, Person, Ship


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name"]


class PersonSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())

    class Meta:
        model = Person
        fields = ["id", "name", "email", "phone", "company"]


class ShipSerializer(serializers.ModelSerializer):

    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())

    class Meta:
        model = Ship
        fields = "__all__"


class HarbourSerializer(serializers.ModelSerializer):

    class Meta:
        model = Harbour
        fields = "__all__"
