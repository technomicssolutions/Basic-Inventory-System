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
	name = models.CharField('Name', max_length=200, unique=False)
	item_type = models.CharField('Type', max_length=50, choices=ITEM_TYPE, default='item')
	
	def __unicode__(self):
		return self.code

	class Meta:
		verbose_name_plural = 'Item'

class InventoryItem(models.Model):

	item = models.ForeignKey(Item, null=True, blank=True)
	selling_price = models.DecimalField('Selling Price', decimal_places=2, max_digits=14, default=0)
	quantity = models.IntegerField('Quantity', default=0)
	unit_price = models.DecimalField('Unit Price',max_digits=14, decimal_places=2, default=0)

	class Meta:
		verbose_name_plural = 'Inventory'

	def __unicode__(self):
		return self.item.code


class Project(models.Model):

	start_date = models.DateField('Start Date', null=True, blank=True)
	expected_end_date = models.DateField('Expected End Date', null=True, blank=True)
	name = models.CharField('Project Name', max_length=20, null=True, blank=True, unique=True)
	budget_amount = models.DecimalField('Budget Amount', max_digits=25, decimal_places=2, default=0)
	expense_amount = models.DecimalField('Expense Amount', max_digits=25, decimal_places=2, default=0)
	sales_amount = models.DecimalField('Sales Amount', max_digits=25, decimal_places=2, default=0)
	purchase_amount = models.DecimalField('Purchase Amount', max_digits=25, decimal_places=2, default=0)
	
	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name_plural = 'Project'

class ProjectItem(models.Model):

	project = models.ForeignKey(Project)
	item = models.ForeignKey(Item, null=True, blank=True)
	quantity = models.IntegerField('Quantity', default=0)
	unit_price = models.DecimalField('Unit Price',max_digits=14, decimal_places=2, default=0)
	selling_price = models.DecimalField('Selling Price',max_digits=14, decimal_places=2, default=0)

	def __unicode__(self):
		return self.project.name + ' - ' + self.item.code

	class Meta:
		verbose_name_plural = 'Project Item'
