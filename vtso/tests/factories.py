import factory

from vtso.models import Company, Person


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
