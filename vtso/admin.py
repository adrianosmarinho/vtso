# from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Company, CompanyAdmin

# Register your models here.
admin.site.register(Company, CompanyAdmin)
