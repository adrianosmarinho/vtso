import factory
from django.utils.timezone import get_current_timezone

from vtso.models import Company, Harbour, Person, Ship, Visit


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    name = factory.Faker("company")


class PersonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Person

    company = factory.SubFactory(CompanyFactory)
    name = factory.Faker("first_name")
    email = factory.Faker("email")
    phone = factory.Faker("phone_number", locale="en_AU")


class ShipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ship

    company = factory.SubFactory(CompanyFactory)
    name = factory.Faker("word")
    tonnage = factory.Faker("random_int", min=1000, max=10000)
    max_load_draft = factory.Faker("random_int", min=5, max=15)
    dry_draft = factory.Faker("random_int", min=3, max=8)
    flag = factory.Faker("country_code")
    beam = factory.Faker("random_int", min=10, max=30)
    length = factory.Faker("random_int", min=50, max=150)
    year_built = factory.Faker("year")
    type = factory.Faker(
        "random_element",
        elements=["bulk carrier", "fishing", "submarine", "tanker", "cruise ship"],
    )


class HarbourFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Harbour

    name = factory.Faker("city")
    max_berth_depth = factory.Faker("random_int", min=5, max=20)
    harbour_master = factory.Faker("name")
    city = factory.Faker("city")
    country = factory.Faker("country")


class VisitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Visit

    ship = factory.SubFactory(ShipFactory)
    harbour = factory.SubFactory(HarbourFactory)
    entry_time = factory.Faker("date_time", tzinfo=get_current_timezone())
    exit_time = factory.Faker("date_time", tzinfo=get_current_timezone())
