# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Sales'
        db.create_table(u'sales_sales', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.Customer'], null=True, blank=True)),
            ('sales_invoice_number', self.gf('django.db.models.fields.CharField')(max_length=10, unique=True, null=True, blank=True)),
            ('sales_invoice_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='estimate', max_length=100)),
            ('payment_mode', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('cheque_no', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('bank_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('bank_branch', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('cheque_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('net_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('net_amount_after_return', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('grant_total', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('grant_total_after_return', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('balance', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=14, decimal_places=2, blank=True)),
            ('paid', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=14, decimal_places=2, blank=True)),
            ('discount_for_sale', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('discount_percentage_for_sale', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('is_processed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'sales', ['Sales'])

        # Adding model 'SalesItem'
        db.create_table(u'sales_salesitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sales', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sales.Sales'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Item'], null=True, blank=True)),
            ('quantity_sold', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('selling_price', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('net_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
        ))
        db.send_create_signal(u'sales', ['SalesItem'])

        # Adding model 'SalesReturn'
        db.create_table(u'sales_salesreturn', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sales', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sales.Sales'])),
            ('return_invoice_number', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('net_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
        ))
        db.send_create_signal(u'sales', ['SalesReturn'])

        # Adding model 'SalesReturnItem'
        db.create_table(u'sales_salesreturnitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sales_return', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sales.SalesReturn'], null=True, blank=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Item'], null=True, blank=True)),
            ('sold_quantity', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('return_quantity', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
        ))
        db.send_create_signal(u'sales', ['SalesReturnItem'])

        # Adding model 'ReceiptVoucher'
        db.create_table(u'sales_receiptvoucher', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sales_invoice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sales.Sales'], null=True, blank=True)),
            ('receipt_voucher_no', self.gf('django.db.models.fields.CharField')(max_length=30, unique=True, null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('total_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('paid_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('cheque_no', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('bank', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('dated', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('payment_mode', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
        ))
        db.send_create_signal(u'sales', ['ReceiptVoucher'])

        # Adding model 'CustomerAccount'
        db.create_table(u'sales_customeraccount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('invoice_no', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sales.Sales'], null=True, blank=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.Customer'], null=True, blank=True)),
            ('total_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('paid', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('balance', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('is_complted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'sales', ['CustomerAccount'])

        # Adding model 'CustomerPayment'
        db.create_table(u'sales_customerpayment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('customer_account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sales.Sales'], null=True, blank=True)),
            ('payment_mode', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.Customer'], null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('total_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('paid', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('balance', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
        ))
        db.send_create_signal(u'sales', ['CustomerPayment'])

    def backwards(self, orm):
        # Deleting model 'Sales'
        db.delete_table(u'sales_sales')

        # Deleting model 'SalesItem'
        db.delete_table(u'sales_salesitem')

        # Deleting model 'SalesReturn'
        db.delete_table(u'sales_salesreturn')

        # Deleting model 'SalesReturnItem'
        db.delete_table(u'sales_salesreturnitem')

        # Deleting model 'ReceiptVoucher'
        db.delete_table(u'sales_receiptvoucher')

        # Deleting model 'CustomerAccount'
        db.delete_table(u'sales_customeraccount')

        # Deleting model 'CustomerPayment'
        db.delete_table(u'sales_customerpayment')

    models = {
        u'inventory.item': {
            'Meta': {'object_name': 'Item'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'sales.customeraccount': {
            'Meta': {'object_name': 'CustomerAccount'},
            'balance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Customer']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_no': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sales.Sales']", 'null': 'True', 'blank': 'True'}),
            'is_complted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'paid': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'total_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'})
        },
        u'sales.customerpayment': {
            'Meta': {'object_name': 'CustomerPayment'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'balance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Customer']", 'null': 'True', 'blank': 'True'}),
            'customer_account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sales.Sales']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'payment_mode': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'total_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'})
        },
        u'sales.receiptvoucher': {
            'Meta': {'object_name': 'ReceiptVoucher'},
            'bank': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'cheque_no': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dated': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'payment_mode': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'receipt_voucher_no': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'sales_invoice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sales.Sales']", 'null': 'True', 'blank': 'True'}),
            'total_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'})
        },
        u'sales.sales': {
            'Meta': {'object_name': 'Sales'},
            'balance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'bank_branch': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'bank_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'cheque_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'cheque_no': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Customer']", 'null': 'True', 'blank': 'True'}),
            'discount_for_sale': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'discount_percentage_for_sale': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'grant_total': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'grant_total_after_return': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'net_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'net_amount_after_return': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'paid': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'payment_mode': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'sales_invoice_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'sales_invoice_number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'estimate'", 'max_length': '100'})
        },
        u'sales.salesitem': {
            'Meta': {'object_name': 'SalesItem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Item']", 'null': 'True', 'blank': 'True'}),
            'net_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'quantity_sold': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sales': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sales.Sales']"}),
            'selling_price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'})
        },
        u'sales.salesreturn': {
            'Meta': {'object_name': 'SalesReturn'},
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'net_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'return_invoice_number': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'sales': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sales.Sales']"})
        },
        u'sales.salesreturnitem': {
            'Meta': {'object_name': 'SalesReturnItem'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Item']", 'null': 'True', 'blank': 'True'}),
            'return_quantity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sales_return': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sales.SalesReturn']", 'null': 'True', 'blank': 'True'}),
            'sold_quantity': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'web.customer': {
            'Meta': {'object_name': 'Customer'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'customer_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'district': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'email_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'house_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'land_line': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'mobile_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'pin': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['sales']