from django.contrib import admin

from .models import Thing, ThingTaker


@admin.register(Thing)
class ThingAdmin(admin.ModelAdmin):
    pass


@admin.register(ThingTaker)
class ThingTaker(admin.ModelAdmin):
    pass
