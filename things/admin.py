from django.contrib import admin

from .models import Category, Taker, Thing


@admin.register(Thing)
class ThingAdmin(admin.ModelAdmin):
    list_display = ('name', 'taken_by')
    list_filter = ('taken_by',)
    search_fields = ('name', )


@admin.register(Taker)
class TakerAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
