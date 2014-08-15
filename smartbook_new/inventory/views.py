import ast
import simplejson
from django.views.generic.base import View
from django.shortcuts import render
from django.http import  HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from inventory.models import Item, InventoryItem, OpeningStock
from sales.models import SalesItem
from purchase.models import PurchaseItem

class AddItem(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'inventory/add_item.html', {})

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
                item, created = Item.objects.get_or_create(code=item_details['code'], name=item_details['name'])
                ctx_item.append({
                    'id': item.id,
                    'name': item.name,
                    'code': item.code,
                    'current_stock': 0,
                })
                res = {
                    'result': 'ok',
                    'item': ctx_item,
                }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')
class DeleteItem(View):
    def get(self,request,*args,**kwargs):
        item_id = kwargs['item_id']
        item = Item.objects.get(id=item_id)
        sales = SalesItem.objects.filter(item=item)
        purchases = PurchaseItem.objects.filter(item=item)
        if purchases.count() == 0 and sales.count() == 0:
            item.delete()
        else:
            items = Item.objects.all()
            return render(request, 'inventory/items.html', {'items': items, 'message': 'Not able to delete this item'})
        return HttpResponseRedirect(reverse('items'))

class EditItem(View):

    def get(self, request, *args, **kwargs):
        status = 200
        item = Item.objects.get(id=kwargs['item_id'])
        ctx_item = []
        if request.is_ajax():
            ctx_item.append({
                'name': item.name,
                'code': item.code,
                'id': item.id,
            })
            res = {
                'result': 'ok',
                'item': ctx_item,
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')
        return render(request, 'inventory/edit_item.html', {'item_id': item.id})

    def post(self, request, *args, **kwargs):
        status = 200
        item = Item.objects.get(id=kwargs['item_id'])
        item_details = ast.literal_eval(request.POST['item'])
        item.name = item_details['name']
        item.save()
        res = {
            'result': 'ok',
        }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=status, mimetype='application/json')


class ItemList(View):

    def get(self, request, *args, **kwargs):
        inventory_items = []
        status = 200
        items = Item.objects.all().order_by('name')
        current_stock = 0
        unit_price = 0
        if request.is_ajax():
            try:
                item_code = request.GET.get('item_code', '')
                item_name = request.GET.get('item_name', '')
                items = []
                if item_code:
                    items = Item.objects.filter(code__istartswith=item_code)
                elif item_name:
                    items = Item.objects.filter(name__istartswith=item_name)
                
                for item in items:
                    try:
                        inventory = InventoryItem.objects.get(item=item)
                    except:
                        inventory = None
                    inventory_items.append({
                        'id': item.id,
                        'name': item.name,
                        'code': item.code,
                        'current_stock': inventory.quantity if inventory else 0 ,
                        'unit_price': inventory.unit_price if inventory else 0, 
                        'selling_price': inventory.selling_price if inventory else 0, 
                    })
            except Exception as ex:
                response = simplejson.dumps({'result': 'error', 'error': str(ex)})
                return HttpResponse(response, status = status_code, mimetype = 'application/json')
            res = {
                'result': 'ok',
                'inventory_items': inventory_items,
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')
       
        return render(request, 'inventory/items.html', {'items': items})

class AddOpeningStock(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'inventory/add_opening_stock.html', {})

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            status = 200
            ctx_item = []
            opening_stock_details = ast.literal_eval(request.POST['opening_stock_details'])
            item = Item.objects.get(code=opening_stock_details['item_code'])
            inventory_item, created = InventoryItem.objects.get_or_create(item=item)
            opening_stock,opening_stock_created = OpeningStock.objects.get_or_create(item=inventory_item)
            if opening_stock_created:
                opening_stock.quantity = opening_stock_details['quantity']
            else:
                opening_stock.quantity = opening_stock.quantity + int(opening_stock_details['quantity'])
            opening_stock.item = inventory_item
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
        return render(request, 'inventory/opening_stock.html', {'opening_stocks': opening_stocks})

class StockView(View):

    def get(self, request, *args, **kwargs):
        stock_items = InventoryItem.objects.all()
        return render(request, 'inventory/stock.html', {
            'stock_items': stock_items
        })
    
        