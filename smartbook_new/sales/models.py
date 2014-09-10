from django.db import models

from inventory.models import  Item
from web.models import Customer, PAYMENT_MODE

STATUS  = (
    ('estimate', 'Estimate'),
    ('invoice', 'Invoice'),
)

class Sales(models.Model): 
    customer = models.ForeignKey(Customer, null=True, blank=True)

    sales_invoice_number = models.CharField('Sales Invoice Number', null=True, blank=True, max_length=10, unique=True)
    sales_invoice_date = models.DateField('Sales Invoice Date', null=True, blank=True)

    status = models.CharField('Status', max_length=100, choices=STATUS, default='estimate')
    
    payment_mode = models.CharField('Payment Mode', null=True, blank=True, max_length=25)
    cheque_no = models.CharField('Cheque Number',null=True, blank=True, max_length=25)
    bank_name = models.CharField('Bank Name',max_length=50,null=True, blank=True)
    bank_branch = models.CharField('Bank Branch', max_length=25, null=True, blank=True)
    cheque_date = models.DateField('Cheque Date', null=True, blank=True)
    
    net_amount = models.DecimalField('Net Amount',max_digits=14, decimal_places=2, default=0)
    kvat = models.DecimalField('KVAT',max_digits=14, decimal_places=2, default=0)
    cess = models.DecimalField('CESS',max_digits=14, decimal_places=2, default=0)
    net_taxable_value = models.DecimalField('Net Taxable Value', max_digits=14, decimal_places=2, default=0)
    grant_total = models.DecimalField('Grand Total',max_digits=14, decimal_places=2, default=0)   
    balance = models.DecimalField('Balance', null=True, blank=True, decimal_places=2, default=0, max_digits=14)
    paid = models.DecimalField('Paid', null=True, blank=True, decimal_places=2, default=0, max_digits=14)
    discount_for_sale = models.DecimalField('Discount for sale',max_digits=14, decimal_places=2, default=0)
    discount_percentage_for_sale = models.DecimalField('Discount percentage for sale',max_digits=14, decimal_places=2, default=0)

    is_processed = models.BooleanField('Processed', default=False)
    is_returned = models.BooleanField('Is Returned Completely', default=False)

    def __unicode__(self):
        return str(self.sales_invoice_number)

    class Meta:
        verbose_name_plural = 'Sales'

class SalesItem(models.Model):
    sales = models.ForeignKey(Sales)
    item = models.ForeignKey(Item, null=True, blank=True)
    rate_of_tax = models.DecimalField('Rate Of Tax',max_digits=14, decimal_places=2, default=0)
    quantity_sold = models.IntegerField('Quantity Sold', default=0)
    selling_price = models.DecimalField('Selling Price', max_digits=14, decimal_places=2, default=0) 
    net_amount = models.DecimalField('Sold Net Amount', max_digits=14, decimal_places=2, default=0)
    
    def __unicode__(self):
        return str(self.sales.sales_invoice_number)

    class Meta:
        verbose_name_plural = 'Sales Items'

class SalesReturn(models.Model):
    sales = models.ForeignKey(Sales)
    return_invoice_number = models.IntegerField('Sales Return invoice number', unique=True)
    date = models.DateField('Date', null=True, blank=True)
    net_amount = models.DecimalField('Total', max_digits=14, decimal_places=2, default=0)
    
    grant_total_before_return = models.DecimalField('Grand Total before return',max_digits=14, decimal_places=2, default=0)
    net_amount_before_return = models.DecimalField('Net Amount before return',max_digits=14, decimal_places=2, default=0)
    discount_before_return = models.DecimalField('Discount before return',max_digits=14, decimal_places=2, default=0)

    def __unicode__(self):
        return str(self.sales.sales_invoice_number)

class SalesReturnItem(models.Model):
    sales_return = models.ForeignKey(SalesReturn, null=True, blank=True)
    item = models.ForeignKey(Item, null=True, blank=True)
    sold_quantity = models.IntegerField('Sold Quantity', default=0)
    return_quantity = models.IntegerField('Return Quantity', null=True, blank=True)
    amount = models.DecimalField('Amount', max_digits=14, decimal_places=2, default=0)

    def __unicode__(self):
        return str(self.sales_return.return_invoice_number)

class ReceiptVoucher(models.Model):
    sales_invoice = models.ForeignKey(Sales, null=True, blank=True)
    receipt_voucher_no = models.CharField('Receipt Voucher No', null=True, blank=True, max_length=30, unique=True)
    date = models.DateField('Date', null=True, blank=True)
    total_amount = models.DecimalField('Total Amount', max_digits=14, decimal_places=2, default=0)
    paid_amount = models.DecimalField('Paid Amount', max_digits=14, decimal_places=2, default=0)
    cheque_no = models.CharField('Check Number', null=True, blank=True, max_length=50)
    bank = models.CharField('Bank', null=True, blank=True, max_length=100)
    dated = models.DateField('Dated', null=True, blank=True)
    payment_mode = models.CharField('Payment Mode', null=True, blank=True, max_length=40, choices=PAYMENT_MODE)
    
    def __unicode__(self):
        return str(self.sales_invoice.sales_invoice_number)

    class Meta:
        verbose_name_plural = 'Receipt Voucher'

class CustomerAccount(models.Model):
    invoice_no = models.ForeignKey(Sales, null=True, blank=True)
    customer = models.ForeignKey(Customer, null=True, blank=True)
    total_amount = models.DecimalField('Total amount', max_digits=14, decimal_places=2, default=0)
    paid = models.DecimalField('Paid', max_digits=14, decimal_places=2, default=0)
    balance = models.DecimalField('Balance', max_digits=14, decimal_places=2, default=0)
    is_complted = models.BooleanField('Is Completed', default=False)

    class Meta:
        verbose_name_plural = 'Customer Account'

    def __unicode__(self):
        return str(self.invoice_no.sales_invoice_number)

class CustomerPayment(models.Model):
    
    customer_account = models.ForeignKey(Sales, null=True, blank=True)
    payment_mode = models.CharField('Payment Mode', null=True, blank=True, max_length=25)
    customer = models.ForeignKey(Customer, null=True, blank=True)
    date = models.DateField('Date', null=True, blank=True)
    total_amount = models.DecimalField('Total amount', max_digits=14, decimal_places=2, default=0)
    paid = models.DecimalField('Paid', max_digits=14, decimal_places=2, default=0)
    balance = models.DecimalField('Balance', max_digits=14, decimal_places=2, default=0)
    amount = models.DecimalField('Amount', max_digits=14, decimal_places=2, default=0)


    class Meta:

        verbose_name = 'Customer Payment'
        verbose_name_plural = 'Customer Payment'

    def __unicode__(self):

        return str(self.customer_account.sales_invoice_number)
