from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from purchase.views import PurchaseEntry, PurchaseEdit, \
PurchaseDetail, PurchaseReturnView, SupplierAccountEntry

urlpatterns = patterns('',
	url(r'^entry/$', login_required(PurchaseEntry.as_view()), name='purchase'),
	url(r'^edit/$', PurchaseEdit.as_view(), name='edit_purchase'),
	url(r'^purchase_details/$', PurchaseDetail.as_view(), name='purchase_details'),
	url(r'^return/$', PurchaseReturnView.as_view(), name='purchase_return'),

	url(r'^supplier_accounts/$', SupplierAccountEntry.as_view(), name="supplier_accounts"),
)