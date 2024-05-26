import factory

from vtso.models import Company


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    name = factory.Faker("company")
