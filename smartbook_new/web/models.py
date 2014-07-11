from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

USER_TYPE = (
    ('supplier', 'Supplier'),
    ('customer', 'Customer'),
)

class Supplier(models.Model):

    name = models.CharField('Name', max_length=75, null=True, blank=True)
    user_type = models.CharField('User Type', max_length=10, choices=USER_TYPE, null=True, blank=True)
    house_name = models.CharField('House name', null=True, blank=True, max_length=50)
    street = models.CharField('Street', null=True, blank=True, max_length=50)
    city = models.CharField('City', null=True, blank=True, max_length=50)
    district = models.CharField('District', null=True, blank=True, max_length=50)
    pin = models.CharField('Pin', max_length=10, null=True, blank=True,)
    mobile = models.CharField('Mobile', max_length=15, null=True, blank=True)
    land_line = models.CharField('Land Line',max_length=15, null=True, blank=True)
    email_id = models.CharField('Email Id', max_length=30, null=True, blank=True, unique=True)
    contact_person = models.CharField('Contact Person', max_length=50,null=True, blank=True)  

    def __unicode__(self):
        return "supplier - "+str(self.name)
    

    class Meta:

        verbose_name = 'Supplier'
        verbose_name_plural = 'Supplier'

    
class Customer(models.Model):
    
    user_type = models.CharField('User Type', max_length=10, choices=USER_TYPE, null=True, blank=True)
    customer_name = models.CharField('Name of the customer', null=True, blank=True, max_length=75)
    house_name = models.CharField('House name', null=True, blank=True, max_length=50)
    street = models.CharField('Street', null=True, blank=True, max_length=50)
    city = models.CharField('City', null=True, blank=True, max_length=50)
    district = models.CharField('District', null=True, blank=True, max_length=50)
    pin = models.CharField('Pin', max_length=10, null=True, blank=True,)
    mobile_number = models.CharField('Mobile Number', max_length=15, null=True, blank=True)
    land_line = models.CharField('Land Line', max_length=25, null=True, blank=True)
    customer_id = models.CharField('Customer Id(Email id)', max_length=75, unique=False)

    def __unicode__(self):
        return "customer - "+ str(self.customer_name)

    class Meta:

        verbose_name = 'Customer'
        verbose_name_plural = 'Customer'

class TransportationCompany(models.Model):

    company_name = models.CharField('Company Name', null=True, blank=True, max_length=50)

    def __unicode__(self):

        return self.company_name

    class Meta:

        verbose_name = 'Transportation Company'
        verbose_name_plural = 'Transportation Company'

class OwnerCompany(models.Model):

    company_name = models.CharField('Company Name', max_length=100)
    logo = models.FileField('Logo', upload_to = "uploads/logo/", null=True, blank=True)

    def __unicode__(self):

        return self.company_name

    class Meta:

        verbose_name_plural = 'Owner Company'