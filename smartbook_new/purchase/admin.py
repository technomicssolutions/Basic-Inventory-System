from django.contrib import admin
from purchase.models import *

admin.site.register(Purchase)
admin.site.register(PurchaseItem)
admin.site.register(SupplierAccount)
admin.site.register(SupplierAccountDetail)

