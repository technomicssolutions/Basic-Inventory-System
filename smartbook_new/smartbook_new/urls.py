from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from web.urls import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'smartbook_new.views.home', name='home'),
    url(r'', include('web.urls')),
    url(r'^purchase/', include('purchase.urls')),
    url(r'^sales/', include('sales.urls')),
    url(r'^expenses/', include('expenses.urls')),
    url(r'^inventory/', include('inventory.urls')),
    url(r'^reports/', include('reports.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
