import factory

from vtso.models import Company, Person, Ship


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
