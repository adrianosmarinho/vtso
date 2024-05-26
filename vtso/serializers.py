from rest_framework import serializers

from vtso.models import Company, Harbour, HarbourLog, Person, Ship


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


class HarbourLogSerializer(serializers.ModelSerializer):

    harbour = serializers.PrimaryKeyRelatedField(queryset=Harbour.objects.all())
    ship = serializers.PrimaryKeyRelatedField(queryset=Ship.objects.all())

    class Meta:
        model = HarbourLog
        fields = "__all__"

    def validate(self, data):
        """
        Override of validate() to ensure clean() is called
        and prevents entry_times of happening after exit_times

        Args:
            data(Any): new HarbourLog data.

        Returns:
            (Any): cleaned data
        """
        instance = HarbourLog(**data)
        instance.clean()
        return data
