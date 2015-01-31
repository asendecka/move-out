from django.contrib import admin

from .models import Category, Taker, Thing


@admin.register(Thing)
class ThingAdmin(admin.ModelAdmin):
    pass


@admin.register(Taker)
class TakerAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
