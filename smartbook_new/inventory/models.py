from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from web.models import *

ITEM_TYPE = (
	('item', 'item'),
	('service_charge', 'service_charge'),
)

class Item(models.Model):

	code = models.CharField('Item Code', max_length=200, unique=True)
	name = models.CharField('Name', max_length=200)
	item_type = models.CharField('Type', max_length=50, choices=ITEM_TYPE, default='item')
	
	def __unicode__(self):
		return self.code

	class Meta:
		verbose_name_plural = 'Item'

class InventoryItem(models.Model):

	item = models.ForeignKey(Item)
	selling_price = models.DecimalField('Selling Price', decimal_places=2, max_digits=14, default=0)
	quantity = models.IntegerField('Quantity', default=0)
	unit_price = models.DecimalField('Unit Price',max_digits=14, decimal_places=2, default=0)

	class Meta:
		verbose_name_plural = 'Inventory'

	def __unicode__(self):
		return self.item.code

class OpeningStock(models.Model):

	item = models.ForeignKey(InventoryItem)
	selling_price = models.DecimalField('Selling Price', decimal_places=2, max_digits=14, default=0)
	quantity = models.IntegerField('Quantity', default=0)
	unit_price = models.DecimalField('Unit Price',max_digits=14, decimal_places=2, default=0)

	class Meta:
		verbose_name_plural = 'OpeningStock'

	def __unicode__(self):
		return self.item.item.code