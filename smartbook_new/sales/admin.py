from django.contrib import admin
from sales.models import Sales, SalesItem, CustomerAccount, ReceiptVoucher, SalesReturn, \
SalesReturnItem, CustomerPayment

admin.site.register(Sales)
admin.site.register(SalesItem)
admin.site.register(CustomerAccount)
admin.site.register(ReceiptVoucher)

admin.site.register(CustomerPayment)

admin.site.register(SalesReturn)
admin.site.register(SalesReturnItem)



