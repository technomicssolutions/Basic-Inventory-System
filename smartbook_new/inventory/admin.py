from django.contrib import admin
from inventory.models import OpeningStock, Item, InventoryItem

admin.site.register(Item)
admin.site.register(InventoryItem)
admin.site.register(OpeningStock)

