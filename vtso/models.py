from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


# Company
class Company(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        db_table = "COMPANY"


class Person(models.Model):
    id = models.BigAutoField(primary_key=True)
    # a Company may employ many Persons
    company = models.ForeignKey(to=Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, null=True, blank=True)
    email = models.EmailField(max_length=256, null=True, blank=True)
    phone = models.CharField(max_length=64, null=True, blank=True)
