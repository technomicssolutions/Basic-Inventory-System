# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ProjectItem'
        db.delete_table(u'project_projectitem')

        # Deleting model 'Project'
        db.delete_table(u'project_project')


        # Changing field 'OpeningStock.item'
        db.alter_column(u'project_openingstock', 'item_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['project.InventoryItem'], null=True))
    def backwards(self, orm):
        # Adding model 'ProjectItem'
        db.create_table(u'project_projectitem', (
            ('unit_price', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['project.Project'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['project.Item'], null=True, blank=True)),
            ('selling_price', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'project', ['ProjectItem'])

        # Adding model 'Project'
        db.create_table(u'project_project', (
            ('expected_end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('expense_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=25, decimal_places=2)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20, null=True, blank=True)),
            ('sales_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=25, decimal_places=2)),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('purchase_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=25, decimal_places=2)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('budget_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=25, decimal_places=2)),
        ))
        db.send_create_signal(u'project', ['Project'])


        # Changing field 'OpeningStock.item'
        db.alter_column(u'project_openingstock', 'item_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['project.Item'], null=True))
    models = {
        u'project.inventoryitem': {
            'Meta': {'object_name': 'InventoryItem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['project.Item']", 'null': 'True', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'selling_price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'unit_price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'})
        },
        u'project.item': {
            'Meta': {'object_name': 'Item'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_type': ('django.db.models.fields.CharField', [], {'default': "'item'", 'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'project.openingstock': {
            'Meta': {'object_name': 'OpeningStock'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['project.InventoryItem']", 'null': 'True', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'selling_price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'unit_price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'})
        }
    }

    complete_apps = ['project']