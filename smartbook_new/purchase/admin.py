from django.contrib import admin
from purchase.models import Purchase, PurchaseItem, SupplierAccount, SupplierAccountPayment, \
PurchaseReturn, PurchaseReturnItem, SupplierAccountPaymentDetail

admin.site.register(Purchase)
admin.site.register(PurchaseItem)
admin.site.register(SupplierAccount)
admin.site.register(SupplierAccountPayment)
admin.site.register(SupplierAccountPaymentDetail)
admin.site.register(PurchaseReturn)
admin.site.register(PurchaseReturnItem)

