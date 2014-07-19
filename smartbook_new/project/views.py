import ast
import simplejson
from datetime import datetime
from django.views.generic.base import View
from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from project.models import *




class AddItem(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'project/add_item.html', {})

    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            status = 200
            ctx_item = []
            item_details = ast.literal_eval(request.POST['item_details'])
            try:
                item = Item.objects.get(code=item_details['code'])
                res = {
                    'result': 'error',
                    'message': 'Item with this code is already exists',
                }
            except Exception as ex:
                print str(ex)
                item, created = Item.objects.get_or_create(code=item_details['code'], name=item_details['name'], item_type=item_details['type'])
                ctx_item.append({
                    'id': item.id,
                    'name': item.name,
                    'code': item.code,
                    'type': item.item_type,
                    'current_stock': 0,
                })
                res = {
                    'result': 'ok',
                    'item': ctx_item,
                }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')
        


class ItemList(View):

    def get(self, request, *args, **kwargs):

        ctx_items = []
        inventory_items = []
        project_items = []
        status = 200
        items = Item.objects.all().order_by('id')
        project_id = request.GET.get('project_id', '')
        current_stock = 0
        unit_price = 0
        is_inventory_items = request.GET.get('inventory_item', '')
        if request.is_ajax():
            if is_inventory_items:
                try:
                    item_code = request.GET.get('item_code', '')
                    item_name = request.GET.get('item_name', '')
                    items = []
                    if item_code:
                        items = Item.objects.filter(code__istartswith=item_code)
                    elif item_name:
                        items = Item.objects.filter(name__istartswith=item_name)
                    
                    for item in items:
                        inventory, created = InventoryItem.objects.get_or_create(item=item)
                        inventory_items.append({
                            'id': item.id,
                            'name': item.name,
                            'code': item.code,
                            'current_stock': inventory.quantity if inventory else 0 ,
                            'unit_price': inventory.selling_price if inventory else 0, 
                            'type': item.item_type,
                        })
                except Exception as ex:
                    response = simplejson.dumps({'result': 'error', 'error': str(ex)})
                    return HttpResponse(response, status = status_code, mimetype = 'application/json')
        
        
            res = {
                'result': 'ok',
                'items': ctx_items,
                'inventory_items': inventory_items,
            }
           
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')
       
        return render(request, 'project/items.html', {'items': items})

class ServiceChargeList(View):

    def get(self, request, *args, **kwargs):

        service_charges_items = []
        status = 200
        
        if request.is_ajax():
            try:
                item_code = request.GET.get('item_code', '')
                item_name = request.GET.get('item_name', '')
                items = []
                if item_code:
                    items = Item.objects.filter(code__istartswith=item_code, item_type='service_charge')
                elif item_name:
                    items = Item.objects.filter(name__istartswith=item_name, item_type='service_charge')
                
                for item in items:
                    inventory, created = InventoryItem.objects.get_or_create(item=item)
                    service_charges_items.append({
                        'id': item.id,
                        'name': item.name,
                        'code': item.code,
                        'current_stock': inventory.quantity if inventory else 0 ,
                        'unit_price': inventory.selling_price if inventory else 0, 
                        'type': item.item_type,
                    })
            except Exception as ex:
                response = simplejson.dumps({'result': 'error', 'error': str(ex)})
                return HttpResponse(response, status = status_code, mimetype = 'application/json')
            res = {
                'result': 'ok',
                'service_charges': service_charges_items,
            }
           
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')
       
        return HttpResponseRedirect(reverse('items'))

class AddOpeningStock(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'project/add_stock.html', {})

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            status = 200
            ctx_item = []
            opening_stock_details = ast.literal_eval(request.POST['opening_stock_details'])
          
            item = Item.objects.get(code=opening_stock_details['item_code'])
            inventory_item, created = InventoryItem.objects.get_or_create(item=item)
            
            opening_stock,opening_stock_created = OpeningStock.objects.get_or_create(item=item)
            
            if opening_stock_created:
                opening_stock.quantity = opening_stock_details['quantity']
            else:
                opening_stock.quantity = opening_stock.quantity + int(opening_stock_details['quantity'])
            opening_stock.item = item
            opening_stock.unit_price = opening_stock_details['unit_price']
            opening_stock.selling_price = opening_stock_details['selling_price']
            opening_stock.save()
            if created:
                inventory_item.quantity = int(opening_stock_details['quantity'])
            else:
                inventory_item.quantity = inventory_item.quantity + int(opening_stock_details['quantity'])
            inventory_item.unit_price = opening_stock_details['unit_price']
            inventory_item.selling_price = opening_stock_details['selling_price']
            inventory_item.save()
            res = {
                    'result': 'ok',
                }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')

class OpeningStocklist(View):
    def  get(self, request, *args, **kwargs):
        opening_stocks = OpeningStock.objects.all()
        return render(request, 'project/stock.html', {'opening_stocks': opening_stocks})
    
class DeleteItem(View):
    def get(self,request,*args,**kwargs):
        item_id = kwargs['item_id']
        item = Item.objects.get(id=item_id)
        item.delete()
        return HttpResponseRedirect(reverse('items'))

          