from django.contrib import admin
from purchase.models import Purchase, PurchaseItem, SupplierAccount, SupplierAccountDetail, \
PurchaseReturn, PurchaseReturnItem

admin.site.register(Purchase)
admin.site.register(PurchaseItem)
admin.site.register(SupplierAccount)
admin.site.register(SupplierAccountDetail)
admin.site.register(PurchaseReturn)
admin.site.register(PurchaseReturnItem)

