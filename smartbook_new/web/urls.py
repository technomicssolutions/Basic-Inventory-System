from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from django.conf import settings

from web.views import *

urlpatterns = patterns('',
	url(r'^$', Home.as_view(), name='home'),

	url(r'login/$', Login.as_view(), name='login'),
	url(r'logout/$', login_required(Logout.as_view()), name='logout'),

	url(r'^register/(?P<user_type>\w+)/$', login_required(RegisterUser.as_view()), name='register_user'),
	url(r'^create_customer/$', login_required(CreateCustomer.as_view()), name='create_customer'),
	url(r'^(?P<user_type>\w+)/list/$', login_required(UserList.as_view()), name='users'),
	url(r'^(?P<user_type>\w+)/(?P<user_id>\d+)/edit/$', login_required(EditUser.as_view()), name='edit_user'),
	url(r'^(?P<user_type>\w+)/(?P<user_id>\d+)/delete/$', login_required(DeleteUser.as_view()), name='delete_user'),

	url(r'^company_list/$', login_required(TransportationCompanyList.as_view()), name="company_list"),
	url(r'^add_company/$', login_required(AddTransportationCompany.as_view()), name="add_company"),
)