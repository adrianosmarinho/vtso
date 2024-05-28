from datetime import datetime

from django.utils.timezone import get_current_timezone
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from vtso.models import Company, Harbour, Person, Ship, Visit


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
    age = serializers.SerializerMethodField()

    class Meta:
        model = Ship
        fields = "__all__"

    def get_age(self, obj: Ship) -> int | None:
        """
        Gets the current age of a Ship.

        Args:
            obj (Ship): a Ship object

        Returns:
            current age of the Ship
        """
        return obj.age


class ShipVisitSerializer(serializers.ModelSerializer):

    harbour_name = serializers.CharField(source="harbour.name", read_only=True)

    class Meta:
        model = Visit
        fields = ["harbour_name", "entry_time", "exit_time"]


class HarbourListSerializer(serializers.ModelSerializer):
    """
    Used on GET /harbours/
    """

    class Meta:
        model = Harbour
        fields = ["id", "name", "max_berth_depth"]


class HarbourCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Harbour
        fields = ["name", "max_berth_depth", "harbour_master", "city", "country"]


class HarbourDetailsSerializer(serializers.ModelSerializer):
    """
    Used on /POST /harbours
    """

    class Meta:
        model = Harbour
        fields = [
            "id",
            "name",
            "max_berth_depth",
            "harbour_master",
            "city",
            "country",
            "current_ships",
        ]

    current_ships = serializers.SerializerMethodField()

    @extend_schema_field(serializers.ListSerializer(child=ShipSerializer()))
    def get_current_ships(self, obj):
        """
        Computes the Ships currently docked at the harbour.
        Args:
            obj (Harbour): Harbour being processed by HarbourDetailView

        Returns:
            list[dict]: list of serialized Ship objects
        """
        current_time = datetime.now(tz=get_current_timezone())
        logs = Visit.objects.filter(
            harbour=obj, entry_time__lte=current_time, exit_time__gte=current_time
        ).select_related("ship")
        ships = [log.ship for log in logs]
        return ShipSerializer(ships, many=True).data


class VisitSerializer(serializers.ModelSerializer):

    harbour = serializers.PrimaryKeyRelatedField(queryset=Harbour.objects.all())
    ship = serializers.PrimaryKeyRelatedField(queryset=Ship.objects.all())

    class Meta:
        model = Visit
        fields = "__all__"

    def validate(self, data):
        """
        Override of validate() to ensure clean() is called
        and prevents entry_times of happening after exit_times

        Args:
            data(Any): new Visit data.

        Returns:
            (Any): cleaned data
        """
        instance = Visit(**data)
        instance.clean()
        return data
