from rest_framework import serializers

from vtso.models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name"]
