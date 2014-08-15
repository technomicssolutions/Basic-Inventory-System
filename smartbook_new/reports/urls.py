from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from django.conf import settings

from reports.views import *

urlpatterns = patterns('',
	

	
	url(r'^whole_sales_report/$', login_required(WholeSalesReport.as_view()), name='whole_sales_report'),
	url(r'^vendor_accounts_report/$', login_required(VendorAccountsReport.as_view()), name='vendor_accounts_report'),
	url(r'^pending_customer/$', PendingCustomerReport.as_view(), name='pending_customer_report'),
	url(r'^customer_payment/$', CustomerPaymentReport.as_view(), name='customer_payment_report'),
	url(r'^expense_report/$', login_required(ExpenseReport.as_view()), name='expense_report'),
	)