from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from django.conf import settings


from project.views import *

urlpatterns = patterns('',
	
	url(r'add_item/$', AddItem.as_view(), name='add_item'),
	
	url(r'items/$', ItemList.as_view(), name='items'),
	url(r'add_stock/$',AddOpeningStock.as_view(),name='add_stock'),
	url(r'service_charges/$', ServiceChargeList.as_view(), name='service_charges'),
)
