from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from web.views import Home, Login, Logout, CreateSupplier, CreateCustomer, CustomerList, SupplierList, \
EditCustomer, EditSupplier, DeleteCustomer, DeleteSupplier, TransportationCompanyList, AddTransportationCompany

urlpatterns = patterns('',
	url(r'^$', Home.as_view(), name='home'),

	url(r'login/$', Login.as_view(), name='login'),
	url(r'logout/$', login_required(Logout.as_view()), name='logout'),

	url(r'^create_supplier/$', login_required(CreateSupplier.as_view()), name='create_supplier'),
	url(r'^create_customer/$', login_required(CreateCustomer.as_view()), name='create_customer'),
	url(r'^customers/$', login_required(CustomerList.as_view()), name='customers'),
	url(r'^suppliers/$', login_required(SupplierList.as_view()), name='suppliers'),
	url(r'^edit_customer/(?P<customer_id>\d+)/$', login_required(EditCustomer.as_view()), name='edit_customer'),
	url(r'^edit_supplier/(?P<supplier_id>\d+)/$', login_required(EditSupplier.as_view()), name='edit_supplier'),
	url(r'^delete_customer/(?P<customer_id>\d+)/$', login_required(DeleteCustomer.as_view()), name='delete_customer'),
	url(r'^delete_supplier/(?P<supplier_id>\d+)/$', login_required(DeleteSupplier.as_view()), name='delete_supplier'),

	url(r'^company_list/$', login_required(TransportationCompanyList.as_view()), name="company_list"),
	url(r'^add_company/$', login_required(AddTransportationCompany.as_view()), name="add_company"),
)