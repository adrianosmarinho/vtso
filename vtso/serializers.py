from rest_framework import serializers

from vtso.models import Company, Person


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name"]


class PersonSerializer(serializers.ModelSerializer):
    # TODO: check if the queryset can be optimized here
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())

    class Meta:
        model = Person
        fields = ["id", "name", "email", "phone", "company"]
