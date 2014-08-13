# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Purchase'
        db.create_table(u'purchase_purchase', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('supplier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.Supplier'], null=True, blank=True)),
            ('transportation_company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.TransportationCompany'], null=True, blank=True)),
            ('purchase_invoice_number', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('supplier_invoice_number', self.gf('django.db.models.fields.CharField')(default='1', max_length=10)),
            ('supplier_do_number', self.gf('django.db.models.fields.CharField')(default='1', max_length=10)),
            ('supplier_invoice_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('purchase_invoice_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('payment_mode', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('bank_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('cheque_no', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('cheque_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('discount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('discount_percentage', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('net_total', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('supplier_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('grant_total', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('purchase_expense', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('is_paid_completely', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'purchase', ['Purchase'])

        # Adding model 'PurchaseItem'
        db.create_table(u'purchase_purchaseitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Item'], null=True, blank=True)),
            ('purchase', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['purchase.Purchase'], null=True, blank=True)),
            ('quantity_purchased', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('cost_price', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=3)),
            ('net_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=3)),
        ))
        db.send_create_signal(u'purchase', ['PurchaseItem'])

        # Adding model 'SupplierAccount'
        db.create_table(u'purchase_supplieraccount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('supplier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.Supplier'], unique=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('payment_mode', self.gf('django.db.models.fields.CharField')(default='cash', max_length=10)),
            ('narration', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('total_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('paid_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('balance', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('cheque_no', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('cheque_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('bank_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('branch_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'purchase', ['SupplierAccount'])

        # Adding model 'SupplierAccountDetail'
        db.create_table(u'purchase_supplieraccountdetail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('supplier_account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['purchase.SupplierAccount'])),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('opening_balance', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=3)),
            ('closing_balance', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=3)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=3)),
        ))
        db.send_create_signal(u'purchase', ['SupplierAccountDetail'])

    def backwards(self, orm):
        # Deleting model 'Purchase'
        db.delete_table(u'purchase_purchase')

        # Deleting model 'PurchaseItem'
        db.delete_table(u'purchase_purchaseitem')

        # Deleting model 'SupplierAccount'
        db.delete_table(u'purchase_supplieraccount')

        # Deleting model 'SupplierAccountDetail'
        db.delete_table(u'purchase_supplieraccountdetail')

    models = {
        u'inventory.item': {
            'Meta': {'object_name': 'Item'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'purchase.purchase': {
            'Meta': {'object_name': 'Purchase'},
            'bank_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'cheque_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'cheque_no': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'discount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'discount_percentage': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'grant_total': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_paid_completely': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'net_total': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'payment_mode': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'purchase_expense': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'purchase_invoice_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'purchase_invoice_number': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Supplier']", 'null': 'True', 'blank': 'True'}),
            'supplier_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'supplier_do_number': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '10'}),
            'supplier_invoice_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'supplier_invoice_number': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '10'}),
            'transportation_company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.TransportationCompany']", 'null': 'True', 'blank': 'True'})
        },
        u'purchase.purchaseitem': {
            'Meta': {'object_name': 'PurchaseItem'},
            'cost_price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Item']", 'null': 'True', 'blank': 'True'}),
            'net_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '3'}),
            'purchase': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['purchase.Purchase']", 'null': 'True', 'blank': 'True'}),
            'quantity_purchased': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'purchase.supplieraccount': {
            'Meta': {'object_name': 'SupplierAccount'},
            'balance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'bank_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'branch_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'cheque_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'cheque_no': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'narration': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'paid_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'payment_mode': ('django.db.models.fields.CharField', [], {'default': "'cash'", 'max_length': '10'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Supplier']", 'unique': 'True'}),
            'total_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'})
        },
        u'purchase.supplieraccountdetail': {
            'Meta': {'object_name': 'SupplierAccountDetail'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '3'}),
            'closing_balance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '3'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opening_balance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '3'}),
            'supplier_account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['purchase.SupplierAccount']"})
        },
        u'web.supplier': {
            'Meta': {'object_name': 'Supplier'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'contact_person': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'district': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'email_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'house_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'land_line': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'pin': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'web.transportationcompany': {
            'Meta': {'object_name': 'TransportationCompany'},
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['purchase']