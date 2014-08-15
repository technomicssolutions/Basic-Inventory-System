from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from inventory.views import AddItem, ItemList, DeleteItem, EditItem, AddOpeningStock,\
	OpeningStocklist, StockView

urlpatterns = patterns('',
	url(r'add_item/$', AddItem.as_view(), name='add_item'),	
	url(r'items/$', ItemList.as_view(), name='items'),
	url(r'delete_item/(?P<item_id>\d+)/$', DeleteItem.as_view(), name='delete_item'),
	url(r'edit_item/(?P<item_id>\d+)/$', EditItem.as_view(), name='edit_item'),
	
	url(r'add_opening_stock/$',AddOpeningStock.as_view(),name='add_opening_stock'),
	url(r'opening_stock/$', OpeningStocklist.as_view(), name='opening_stock'),
	url(r'stock/$', StockView.as_view(), name='stock'),
)
