from django.contrib import admin

from .models import Item, Warehouse, WarehouseItemCount


class WarehouseItemCountInline(admin.TabularInline):
    model = WarehouseItemCount


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    inlines = WarehouseItemCountInline,
