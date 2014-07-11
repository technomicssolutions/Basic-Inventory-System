from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from purchase.views import *

urlpatterns = patterns('',
	url(r'^entry/$', login_required(PurchaseEntry.as_view()), name='purchase'),
	url(r'^vendor_accounts/$', VendorAccounts.as_view(), name='vendor_accounts'),
	url(r'^vendor_account/$', SupplierAccountDetails.as_view(), name='vendor_account_details'),
)