from django.contrib import admin
from project.models import *

admin.site.register(Project)
admin.site.register(Item)
admin.site.register(ProjectItem)
admin.site.register(InventoryItem)
admin.site.register(OpeningStock)

