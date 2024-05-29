# from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import (
    Company,
    CompanyAdmin,
    Harbour,
    HarbourAdmin,
    Person,
    PersonAdmin,
    Ship,
    ShipAdmin,
    User,
    Visit,
    VisitAdmin,
)

# Register your models here.
admin.site.register(Company, CompanyAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Harbour, HarbourAdmin)
admin.site.register(Ship, ShipAdmin)
admin.site.register(Visit, VisitAdmin)
admin.site.register(User)
