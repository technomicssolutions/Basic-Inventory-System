from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from django.conf import settings

from sales.views import *

urlpatterns = patterns('',
	url(r'^entry/$', login_required(SalesEntry.as_view()), name='sales'),
	url(r'^edit_sales_invoice/$', login_required(EditSalesInvoice.as_view()), name='edit_sales_invoice'),
	url(r'^invoice_details/$', login_required(InvoiceDetails.as_view()), name='invoice_details'),
	url(r'^invoice_pdf/(?P<invoice_id>\d+)/$', login_required(SalesInvoicePDF.as_view()), name='invoice_pdf'),
	url(r'^print_invoice/$', login_required(PrintSalesInvoice.as_view()), name='print_invoice'),

	url(r'^receipt_voucher/$', login_required(ReceiptVoucherView.as_view()), name='receipt_voucher'),

	url(r'^dn_details/$', login_required(DeliveryNoteDetails.as_view()), name='dn_details'),
	url(r'^create_delivery_note/$', login_required(DeliveryNoteCreation.as_view()), name='create_delivery_note'),	
	url(r'^edit_delivery_note/$', login_required(EditDeliveryNote.as_view()), name='edit_delivery_note'),	
	url(r'^delivery_note_pdf/(?P<dn_id>\d+)/$', login_required(DeliveryNotePDF.as_view()), name='delivery_note_pdf'),
	url(r'^print_delivery_note/$', login_required(PrintDeliveryNotes.as_view()), name='print_delivery_note'),
	
	url(r'^check_delivery_note_no_existence/$', login_required(CheckDeliverynoteExistence.as_view()), name='dn_exists'),
	url(r'^check_invoice_no_existence/$', login_required(CheckInvoiceExistence.as_view()), name='invoice_exists'),
	url(r'^check_receipt_voucher_existence/$', login_required(CheckReceiptVoucherExistence.as_view()), name='rv_exists'),

)