from django.contrib import admin
from .models import InventoryItem, Category, Supplier

admin.site.register(InventoryItem)
admin.site.register(Category)
admin.site.register(Supplier)
