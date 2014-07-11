from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from django.conf import settings

from reports.views import *

urlpatterns = patterns('',
	url(r'^purchase_report/$', login_required(PurchaseReport.as_view()), name='purchase_report'),
	url(r'^purchase_reports/$', login_required(PurchaseReports.as_view()), name='purchase_reports'),

	url(r'^sales_report/$', login_required(SalesReport.as_view()), name='sales_report'),
	url(r'^whole_sales_report/$', login_required(WholeSalesReport.as_view()), name='whole_sales_report'),

	url(r'^cash_report/$', login_required(CashReport.as_view()), name='cash_report'),
	url(r'^bank_income_report/$', login_required(BankIncomeReport.as_view()), name='bank_income_report'),

	url(r'^project_report/$', login_required(ProjectReport.as_view()), name='project_report'),
	url(r'^cash_flow_report/$', login_required(CashFlows.as_view()), name='cash_flow_report'),

	url(r'^expense_report/$', login_required(ExpenseReport.as_view()), name='expense_report'),
	url(r'^outstanding_customer_report/$', login_required(OutstandingCustomerReport.as_view()), name='outstanding_customer_report'),
)