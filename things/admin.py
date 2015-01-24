from django.contrib import admin

from .models import Thing, Taker


@admin.register(Thing)
class ThingAdmin(admin.ModelAdmin):
    pass


@admin.register(Taker)
class TakerAdmin(admin.ModelAdmin):
    pass
