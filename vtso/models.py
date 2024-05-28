from datetime import datetime

from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import get_current_timezone


class User(AbstractUser):
    pass


# Company
class Company(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        db_table = "COMPANY"
        verbose_name_plural = "Companies"


class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name",)

    # enables seach on the Admin portal
    search_fields = ["name"]


class Person(models.Model):
    id = models.BigAutoField(primary_key=True)
    # a Company may employ many Persons
    company = models.ForeignKey(to=Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, null=True, blank=True)
    email = models.EmailField(max_length=256, null=True, blank=True)
    phone = models.CharField(max_length=64, null=True, blank=True)

    class Meta:
        db_table = "PERSON"


class Harbour(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=256, null=True, blank=True)
    max_berth_depth = models.PositiveIntegerField(null=True, blank=True)
    # the name of the harbour master
    harbour_master = models.CharField(max_length=256, null=True, blank=True)
    city = models.CharField(max_length=256, null=True, blank=True)
    country = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        db_table = "HARBOUR"


def validate_year_in_range(value):
    if value is None or value == "":
        # If the value is None or an empty string, it's valid because null=True and blank=True in the model field
        return

    # Check if all characters in the string are digits
    if not value.isdigit():
        raise ValidationError(f"{value} is not a valid number.")

    # Convert the string to an integer
    num = int(value)

    # Check if the number is within the range 0 to 9999
    if not (0 <= num <= 9999):
        raise ValidationError(f"{value} is not within the range 0 to 9999.")


class Ship(models.Model):
    id = models.BigAutoField(primary_key=True)
    # a Company may operate many Ships
    company = models.ForeignKey(to=Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, null=True, blank=True)
    tonnage = models.PositiveIntegerField(null=True, blank=True)
    max_load_draft = models.PositiveIntegerField(null=True, blank=True)
    dry_draft = models.PositiveIntegerField(null=True, blank=True)

    flag = models.CharField(max_length=256, null=True, blank=True)
    beam = models.PositiveIntegerField(null=True, blank=True)
    length = models.PositiveIntegerField(null=True, blank=True)
    # assumption: year_built varies from 0 to 9999
    year_built = models.CharField(
        max_length=4, null=True, blank=True, validators=[validate_year_in_range]
    )

    class ShipType(models.TextChoices):
        BULK_CARRIER = "bulk carrier", "Bulk Carrier"
        FISHING = "fishing", "Fishing"
        SUBMARINE = "submarine", "Submarine"
        TANKER = "tanker", "Tanker"
        CRUISE_SHIP = "cruise ship", "Cruise Ship"

    type = models.CharField(
        max_length=256, choices=ShipType.choices, null=True, blank=True
    )

    class Meta:
        db_table = "SHIP"

    @property
    def age(self) -> int | None:
        """
        We use this property to display the age of a Ship
        on /vtso/ships/ without storing it on the database.

        Returns:
            int: age of the Ship in years
        """
        if not self.year_built:
            return None
        year_built = int(self.year_built)
        current_year = datetime.now(tz=get_current_timezone()).year
        return current_year - year_built


class Visit(models.Model):
    """
    Each Visit entry contains a record of
    when a particular Ship arrived and exited a particular Harbour.
    Assumption: entry_time and exit_time are known when inputting the data.
    """

    id = models.BigAutoField(primary_key=True)
    ship = models.ForeignKey(to=Ship, on_delete=models.CASCADE)
    harbour = models.ForeignKey(to=Harbour, on_delete=models.CASCADE)
    entry_time = models.DateTimeField(null=True, blank=True)
    exit_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "VISIT"

    def clean(self):
        """
        Override of clean() to validate that exit_time happens after entry_time.

        Raises:
            ValidationError
        """
        if self.entry_time and self.exit_time and self.exit_time < self.entry_time:
            raise ValidationError("Exit time cannot be before entry time.")
