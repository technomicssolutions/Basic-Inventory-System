import ast
import simplejson
from datetime import datetime
from django.views.generic.base import View
from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from project.models import *

class CreateProject(View):

    def get(self, request, *args, **kwargs):

        ctx_project_data = []
        status = 200
        project = None
        if request.GET.get('project_id', ''):
            project = Project.objects.get(id=request.GET.get('project_id', ''))
            ctx_project_data.append({
                'id': project.id,
                'name': project.name,
                'start_date': project.start_date.strftime('%d/%m/%Y'),
                'end_date': project.expected_end_date.strftime('%d/%m/%Y'),
                'budget_amount': project.budget_amount,
            })
            res = {
                'project': ctx_project_data,
                'result': 'ok',
            }
        if request.is_ajax():
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')

        return render(request, 'project/create_project.html', {'project': project if project else ''})

    def post(self, request, *args, **kwargs):

        if request.is_ajax:
            status = 200
            project_details = ast.literal_eval(request.POST['project_details'])
            if project_details['id']:
                project = Project.objects.get(id=project_details['id'])
                try:
                    project.name = project_details['name']
                    project.save()
                    
                except Exception as Ex:
                    res = {
                        'result': 'error',
                        'message': 'Project with this Name is already exists',
                    }
                    response = simplejson.dumps(res)
                    return HttpResponse(response, status=status, mimetype='application/json')
            else:
                try:
                    project = Project.objects.get(name=project_details['name'])
                    res = {
                        'result': 'error',
                        'message': 'Project with this Name is already exists',
                    }
                except Exception as Ex:
                    print str(Ex)
                    project = Project.objects.create(name=project_details['name'])
            project.start_date = datetime.strptime(project_details['start_date'], '%d/%m/%Y')
            project.expected_end_date = datetime.strptime(project_details['end_date'], '%d/%m/%Y')               
            project.budget_amount = project_details['budget_amount']
            project.save()
            res = {
                'result': 'ok',
                'id': project.id,
                'name': project.name,
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')

class Projects(View):
    def get(self, request, *args, **kwargs):

        projects = Project.objects.all()
        current_date = datetime.now().date()
        valid_projects = Project.objects.filter(expected_end_date__gte=current_date)
        ctx_whole_projects = []
        for project in valid_projects:
            ctx_whole_projects.append({
                'id': project.id,
                'name': project.name,
                'start_date': project.start_date.strftime('%d/%m/%Y'),
                'end_date': project.expected_end_date.strftime('%d/%m/%Y'),
                'budget_amount': project.budget_amount if project.budget_amount else '',
            })
        if request.is_ajax():
            status = 200
            res = {
                'result': 'ok',
                'projects': ctx_whole_projects,
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')

        context = {
            'projects': projects,
        }
        return render(request, 'project/project_list.html', context)

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
            else:
                for item in items:
                    current_stock = 0
                    unit_price = 0
                    if project_id:
                        project = Project.objects.get(id=project_id)
                        for p_item in project.projectitem_set.all():
                            if p_item.item.id == item.id:
                                current_stock = p_item.quantity
                                unit_price = p_item.selling_price
                                project_items.append({
                                    'id': item.id,
                                    'name': item.name,
                                    'code': item.code,
                                    'type': item.item_type,
                                    'current_stock': current_stock,
                                    'unit_price': unit_price, 
                                })
                            
                    ctx_items.append({
                        'id': item.id,
                        'name': item.name,
                        'code': item.code,
                        'type': item.item_type,
                        'current_stock': current_stock,
                        'unit_price': unit_price, 
                    })
                
        
            res = {
                'result': 'ok',
                'items': ctx_items,
                'project_items': project_items,
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

class ProjectItemList(View):

    def get(self, request, *args, **kwargs):

        project_items = []
        status = 200
        project_id = request.GET.get('project_id', '')
        if request.is_ajax():
            try:
                item_code = request.GET.get('item_code', '')
                item_name = request.GET.get('item_name', '')
                items = []
                if project_id:
                    project = Project.objects.get(id=project_id)
                    if item_code:
                        items = project.projectitem_set.all().filter(item__code__istartswith=item_code, item__item_type='item').order_by('id')
                    elif item_name:
                        items = project.projectitem_set.all().filter(item__name__istartswith=item_name, item__item_type='item').order_by('id')
                    
                    for p_item in items:

                        project_items.append({
                            'id': p_item.item.id,
                            'name': p_item.item.name,
                            'code': p_item.item.code,
                            'current_stock': p_item.quantity if p_item else 0 ,
                            'unit_price': p_item.selling_price if p_item else 0, 
                            'type': p_item.item.item_type,
                        })
            except Exception as ex:
                response = simplejson.dumps({'result': 'error', 'error': str(ex)})
                return HttpResponse(response, status = status_code, mimetype = 'application/json')
            res = {
                'result': 'ok',
                'project_items': project_items,
            }
           
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')
       
        return HttpResponseRedirect(reverse('items'))

