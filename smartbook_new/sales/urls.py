from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from sales.views import SalesEntry, EditSalesInvoice,InvoiceDetails, SalesInvoicePDF, PrintSalesInvoice, ReceiptVoucherView, CheckInvoiceExistence, CheckReceiptVoucherExistence

urlpatterns = patterns('',
	url(r'^entry/$', login_required(SalesEntry.as_view()), name='sales'),
	url(r'^edit_sales_invoice/$', login_required(EditSalesInvoice.as_view()), name='edit_sales_invoice'),
	url(r'^invoice_details/$', login_required(InvoiceDetails.as_view()), name='invoice_details'),
	url(r'^invoice_pdf/(?P<invoice_id>\d+)/$', login_required(SalesInvoicePDF.as_view()), name='invoice_pdf'),
	url(r'^print_invoice/$', login_required(PrintSalesInvoice.as_view()), name='print_invoice'),

	url(r'^receipt_voucher/$', login_required(ReceiptVoucherView.as_view()), name='receipt_voucher'),

	url(r'^check_invoice_no_existence/$', login_required(CheckInvoiceExistence.as_view()), name='invoice_exists'),
	url(r'^check_receipt_voucher_existence/$', login_required(CheckReceiptVoucherExistence.as_view()), name='rv_exists'),

)