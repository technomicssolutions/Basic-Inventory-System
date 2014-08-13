from django.db import models


from web.models import *
from inventory.models import *

PAYMENT_MODE = (
	('cheque', 'Cheque'),
	('cash', 'Cash'),
    ('credit', 'Credit'),
)

class Purchase(models.Model):
    
    supplier = models.ForeignKey(Supplier, null=True, blank=True)
    transportation_company = models.ForeignKey(TransportationCompany, null=True, blank=True)
    
    purchase_invoice_number = models.IntegerField('Purchase Invoice Number', unique=True)
    supplier_invoice_number = models.CharField('Supplier Invoice Number', default='1', max_length=10)
    supplier_do_number = models.CharField('Supplier DO Number', default='1', max_length = 10)
    supplier_invoice_date = models.DateField('Supplier Invoice Date', null=True, blank=True)
    purchase_invoice_date = models.DateField('Purchase Invoice Date', null=True, blank=True)
    
    payment_mode = models.CharField('Payment Mode', null=True, blank=True, max_length=25, choices=PAYMENT_MODE)
    bank_name = models.CharField('Bank Name',max_length=50,null=True, blank=True)
    cheque_no = models.CharField('Cheque No', max_length=60, null=True, blank=True)
    cheque_date = models.DateField('Cheque Date', null=True, blank=True)
    
    discount = models.DecimalField('Discount',max_digits=14, decimal_places=2, default=0)
    discount_percentage = models.DecimalField('Discount Percentage',max_digits=14, decimal_places=2, default=0)
    net_total = models.DecimalField('Net Total',max_digits=14, decimal_places=2, default=0)
    supplier_amount = models.DecimalField('Supplier Amount',max_digits=14, decimal_places=2, default=0)
    grant_total = models.DecimalField('Grant Total', max_digits=14, decimal_places=2, default=0)
    purchase_expense = models.DecimalField('Purchase Expense', max_digits=14, decimal_places=2, default=0)
    is_paid_completely = models.BooleanField('Paid Completely', default=False)
    
    def __unicode__(self):
        return str(self.purchase_invoice_number)

    class Meta:

        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchase'

class PurchaseItem(models.Model):

    item = models.ForeignKey(Item, null=True, blank=True)
    purchase = models.ForeignKey(Purchase, null=True, blank=True)
    
    quantity_purchased = models.IntegerField('Quantity Purchased', default=0)
    cost_price = models.DecimalField('Cost Price',max_digits=14, decimal_places=3, default=0)
    net_amount = models.DecimalField('Net Amount',max_digits=14, decimal_places=3, default=0)

    def __unicode__(self):

        return str(self.purchase.purchase_invoice_number)

    class Meta:

        verbose_name = 'Purchase Items'
        verbose_name_plural = 'Purchase Items'

class SupplierAccount(models.Model):

    supplier = models.ForeignKey(Supplier, unique=True)
    date = models.DateField('Date', null=True, blank=True)
    payment_mode = models.CharField('Payment Mode', max_length=10, choices=PAYMENT_MODE, default='cash')
    narration = models.TextField('Narration', null=True, blank=True)
    total_amount = models.DecimalField('Total Amount', max_digits=14, decimal_places=2, default=0)
    paid_amount = models.DecimalField('Paid Amount', max_digits=14, decimal_places=2, default=0)
    balance = models.DecimalField('Balance', max_digits=14, decimal_places=2, default=0)
    cheque_no = models.CharField('Cheque No', null=True, blank=True, max_length=30)
    cheque_date = models.DateField('Cheque Date', null=True, blank=True)
    bank_name = models.CharField('Bank Name', max_length=200, null=True, blank=True)
    branch_name = models.CharField('Branch Name', max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.supplier.name

class  SupplierAccountDetail(models.Model):
    
    supplier_account = models.ForeignKey(SupplierAccount)
    date = models.DateField('Date' , null=True, blank=True) 
    opening_balance = models.DecimalField('Opening Balance', max_digits=14, decimal_places=3, default=0) 
    closing_balance = models.DecimalField('Closing Balance', max_digits=14, decimal_places=3, default=0)
    amount = models.DecimalField('Amount', max_digits=14, decimal_places=3, default=0)

    def __unicode__(self):
        return self.supplier_account.supplier.name

class PurchaseReturn(models.Model):
    purchase = models.ForeignKey(Purchase)
    return_invoice_number = models.IntegerField('Purchase Return invoice number', unique=True)
    date = models.DateField('Date', null=True, blank=True)
    net_amount = models.DecimalField('Amount', max_digits=14, decimal_places=3, default=0)

    def __unicode__(self):
        return str(self.purchase.purchase_invoice_number)

class PurchaseReturnItem(models.Model):
    purchase_return = models.ForeignKey(PurchaseReturn)
    item = models.ForeignKey(Item)
    amount = models.DecimalField('Amount', max_digits=14, decimal_places=3, default=0)
    quantity = models.IntegerField('Quantity', default=0)
    
    def __unicode__(self):
        return str(self.purchase_return.return_invoice_number)
