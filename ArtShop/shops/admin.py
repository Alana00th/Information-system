from django.contrib import admin
from .models import *


class ShopAdmin (admin.ModelAdmin):
    # list_display = ["name", "email"]
    list_display = [field.name for field in Shop._meta.fields]
    # list_filter = ['name']
    search_fields = ['name']

    class Meta:
        model = Shop


admin.site.register(Shop, ShopAdmin)


class InventAdmin (admin.ModelAdmin):
    list_display = [field.name for field in Invent._meta.fields]
    search_fields = ['stuff']

    class Meta:
        model = Invent


admin.site.register(Invent, InventAdmin)