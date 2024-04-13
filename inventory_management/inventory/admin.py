from django.contrib import admin
from .models import InventoryItem, Category, Supplier, Location

admin.site.register(InventoryItem)
admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(Location)