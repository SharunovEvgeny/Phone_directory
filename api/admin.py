from django.contrib import admin

from api.models import Contact, Number


@admin.register(Contact, Number)
class PersonAdmin(admin.ModelAdmin):
    pass
