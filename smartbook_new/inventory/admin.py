
from django.contrib import admin
from inventory.models import *


admin.site.register(Item)

admin.site.register(InventoryItem)
admin.site.register(OpeningStock)

