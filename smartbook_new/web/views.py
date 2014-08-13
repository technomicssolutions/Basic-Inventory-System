import simplejson
import re
from datetime import datetime

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from web.models import (Supplier, Customer, TransportationCompany)

class Home(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'home.html',context)

class Login(View):

    def post(self, request, *args, **kwargs):

        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user and user.is_active:
            login(request, user)
        else:
            context = {
                'message' : 'Username or password is incorrect'
            }
            return render(request, 'home.html',context)
        return HttpResponseRedirect(reverse('home'))

class Logout(View):

    def get(self, request, *args, **kwargs):

        logout(request)
        return HttpResponseRedirect(reverse('home'))

class CustomerList(View):
    def get(self, request, *args, **kwargs):
        
        ctx_suppliers = []
        ctx_customers = []
        
       
   
        customers = Customer.objects.all()
        
        if request.is_ajax():
            if len(customers) > 0:
                for customer in customers:
                    ctx_customers.append({
                        'customer_name': customer.customer_name,
                    })
            res = {
                'customers': ctx_customers,                    
            } 
            response = simplejson.dumps(res)
            status_code = 200
            return HttpResponse(response, status = status_code, mimetype="application/json")

        return render(request, 'customers.html',{
            'customers': customers,
        })

class SupplierList(View):
    def get(self, request, *args, **kwargs):
        
        ctx_suppliers = []
  
        suppliers = Supplier.objects.all()
        if request.is_ajax():
            if len(suppliers) > 0:
                for supplier in suppliers:
                    ctx_suppliers.append({
                        'supplier_name': supplier.name,
                        'id': supplier.id,
                    })
            res = {
                'suppliers': ctx_suppliers,
                
            } 
            
            response = simplejson.dumps(res)
            status_code = 200
            return HttpResponse(response, status = status_code, mimetype="application/json")
        return render(request, 'supplier.html',{
            'suppliers': suppliers,
        })


class CreateSupplier(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'add_supplier.html',{})

    def post(self, request, *args, **kwargs):
       
        context={}
        message = ''
        template = 'add_supplier.html'
        if request.POST['email'] != '':
            email_validation = (re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", request.POST['email']) )
        if not request.is_ajax():
            if request.POST['name'] == '':
                message = "Please enter Name"
            elif request.POST['email'] != '':
                if email_validation == None:
                    message = "Please enter a valid email id"
            elif request.POST['contact_person'] == '':
                message = "Please enter Contact Person"
            elif request.POST['mobile'] == '':
                message = "Please enter Mobile Number"
            if request.POST['mobile'] != '':
                if len(request.POST['mobile']) > 15:
                    message = 'Please enter a valid mobile no.'
            if request.POST['phone'] != '':
                if len(request.POST['phone']) > 15:
                    message = 'Please enter a valid phone no.'
        if message:
            context = {
                'error_message': message,
            }
            context.update(request.POST)            
            return render(request, template, context)
        else:
            try:
                supplier = Supplier.objects.get(name=request.POST['name'])
                context = {
                    'error_message': 'Supplier with this name is already exists',
                    
                }
                if request.is_ajax():
                    res = {
                        'result': 'error',
                        'message': 'Supplier with this name is already exists'
                    }
                    response = simplejson.dumps(res)
                    return HttpResponse(response, status = 200, mimetype="application/json")
                context.update(request.POST)           
                return render(request, template, context)
            except Exception as Ex:
                print str(Ex)
                supplier, supplier_created = Supplier.objects.get_or_create(name=request.POST['name'])
                supplier.name = request.POST['name']
                supplier.house_name = request.POST['house']
                supplier.street = request.POST['street']
                supplier.city = request.POST['city']
                supplier.district = request.POST['district']
                supplier.pin = request.POST['pin']
                supplier.mobile = request.POST['mobile']
                supplier.land_line = request.POST['phone']
                supplier.email_id = request.POST['email']
                supplier.contact_person = request.POST['contact_person']
                supplier.save()
                if request.is_ajax():
                    res = {
                        'result': 'ok',
                        'supplier_name': supplier.name
                    }
                    response = simplejson.dumps(res)
                    return HttpResponse(response, status = 200, mimetype="application/json")
                
            if  supplier_created:

                suppliers = Supplier.objects.all()
                return render(request, 'supplier.html',{
                    'suppliers': suppliers,
                })

            return render(request, 'add_supplier.html',context)

class EditCustomer(View):

    def get(self, request, *args, **kwargs):

        customer_id = kwargs['customer_id']
        print customer_id
        customer = Customer.objects.get(id=customer_id)
        return render(request, 'edit_customer.html',{'customer_id': customer_id, 'customer': customer, })

    def post(self, request, *args, **kwargs):

        customer_id = kwargs['customer_id']
        post_dict = request.POST
        email_validation = (re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", request.POST['email']) )
        
        customer = Customer.objects.get(id = customer_id)
        
        if request.POST['name'] == '':
            context = {
                'message': 'Name cannot be null',
                'customer': customer,
                'customer_id': customer_id,
            }
            context.update(request.POST)
            return render(request, 'edit_customer.html',context)
        elif request.POST['email'] == '':
            context = {
                'message': 'Email cannot be null',
                'customer': customer,
                'customer_id': customer_id,
            }
            context.update(request.POST)
            return render(request, 'edit_user.html',context)
        if email_validation == None:
            message = "Please enter a valid email id"
            context = {
                'message': message,
                'customer': customer,
                'customer_id': customer_id,
            }
            context.update(request.POST)
            return render(request, 'edit_customer.html',context)  

        
        customer.customer_name = request.POST['name']
        customer.house_name =request.POST['house']
        customer.street = request.POST['street']
        customer.city = request.POST['city']
        customer.district = request.POST['district']
        customer.pin = request.POST['pin']
        customer.mobile_number = request.POST['mobile']
        customer.land_line = request.POST['phone']
        customer.email_id = request.POST['email']
        customer.save()
        context = {
            'message' : 'Customer edited correctly',
            'customer': customer,
            'customer_id': customer_id,
        }
        return render(request, 'edit_customer.html',context)
        
class EditSupplier(View):

    def get(self, request, *args, **kwargs):

        supplier_id = kwargs['supplier_id']
        supplier = Supplier.objects.get(id=supplier_id)
        return render(request, 'edit_supplier.html',{'supplier_id':supplier_id, 'supplier': supplier})

    def post(self, request, *args, **kwargs):

        
        post_dict = request.POST
        email_validation = (re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", request.POST['email']) )
        supplier_id = kwargs['supplier_id']
        supplier = Supplier.objects.get(id = supplier_id)
        if request.POST['name'] == '':
            context = {
                'message': 'Name cannot be null',
                
                'supplier': supplier,
                'supplier_id':supplier_id,
            }
            context.update(request.POST)
            return render(request, 'edit_supplier.html',context)
        if request.POST['email'] != '':
            if email_validation == None:
                message = "Please enter a valid email id"
                context = {
                    'message': message,
                    'supplier': supplier,
                    'supplier_id':supplier_id,
                }
                context.update(request.POST)
                return render(request, 'edit_supplier.html',context)  
             
        try:
            supplier.name = request.POST['name']
            supplier.house_name =request.POST['house']
            supplier.street = request.POST['street']
            supplier.city = request.POST['city']
            supplier.district = request.POST['district']
            supplier.pin = request.POST['pin']
            supplier.mobile = request.POST['mobile']
            supplier.land_line = request.POST['phone']
            supplier.email_id = request.POST['email']
            supplier.contact_person= request.POST['contact_person']
            supplier.save()
            return HttpResponseRedirect(reverse('suppliers'))
        except Exception as ex:
            print str(ex)

            context = {
                'message' : 'Supplier with this name already exists',
                'supplier': supplier,
                'supplier_id':supplier_id,
            }
            return render(request, 'edit_supplier.html',context)

class DeleteCustomer(View):

    def get(self, request, *args, **kwargs):

        
        if request.user.is_superuser:
            customer_id = kwargs['customer_id']
            customer = Customer.objects.get(id=customer_id)
            customer.delete()
        else:
            context = {
                'message': "You don't have permission to perform this action"
            }
        return HttpResponseRedirect(reverse('customers'))

class DeleteSupplier(View):

    def get(self, request, *args, **kwargs):

        
        if request.user.is_superuser:
            supplier_id = kwargs['supplier_id']
            supplier = Supplier.objects.get(id=supplier_id)            
            supplier.delete()
        else:
            context = {
                'message': "You don't have permission to perform this action"
            }
        return HttpResponseRedirect(reverse('suppliers'))

class CreateCustomer(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'add_customer.html',{})

    def post(self, request, *args, **kwargs):

        if not request.is_ajax():
            email_validation = (re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", request.POST['email']) )
            if request.POST['name'] == '':
                context = {
                    'error_message': 'Please enter the name',
                    
                }
                context.update(request.POST)
                return render(request, 'add_customer.html',context)
            elif request.POST['email'] == '':
                context = {
                    'error_message': 'Please enter the email id',
                    
                }
                context.update(request.POST)
                return render(request, 'add_customer.html',context)

            elif email_validation == None:
                message = "Please enter a valid email id"
                context = {
                    'error_message': 'Please enter a valid email id',
                    
                }
                context.update(request.POST)
                return render(request, 'add_customer.html',context)

            elif request.POST['mobile'] != '':
                if len(request.POST['mobile']) > 15:
                    context = {
                        'error_message': 'Please enter a valid mobile no',
                        
                    }
                    context.update(request.POST)
                    return render(request, 'add_customer.html',context)
            elif request.POST['phone'] != '':
                if len(request.POST['phone']) > 15:
                    context = {
                        'error_message': 'Please enter a valid phone no.',
                        
                    }
                    context.update(request.POST)
                    return render(request, 'add_customer.html',context)
        try:
            customer = Customer.objects.get(customer_name = request.POST['name'])
            if request.is_ajax():
                res = {
                    'result': 'error',
                    'message': 'Customer with this name already exists',
                }
                response = simplejson.dumps(res)
                return HttpResponse(response, status = 200, mimetype="application/json")
            else:
                context = {
                    'error_message': 'Customer with this name already exists',
                    
                }
                context.update(request.POST)
                return render(request, 'add_customer.html',context)
        except Exception as ex:
            customer = Customer.objects.create(customer_name=request.POST['name'])
            customer.customer_name = request.POST['name']
            customer.house_name = request.POST['house'] 
            customer.street = request.POST['street']
            customer.city = request.POST['city']
            customer.district = request.POST['district'] 
            customer.pin = request.POST['pin']
            customer.mobile_number = request.POST['mobile']
            customer.land_line = request.POST['phone']
            customer.email_id = request.POST['email']
            customer.save()
            if request.is_ajax():
                res = {
                    'result': 'ok',
                    'customer_name': customer.customer_name
                }
                response = simplejson.dumps(res)
                return HttpResponse(response, status = 200, mimetype="application/json")
            customers = Customer.objects.all()
            return render(request, 'customers.html',{
                'customers': customers,
                
            })

class TransportationCompanyList(View):

    def get(self, request, *args, **kwargs):

        ctx = []
        transportationcompanies = TransportationCompany.objects.all()
        if len(transportationcompanies) > 0:
            for transportationcompany in transportationcompanies:
                ctx.append({
                    'company_name': transportationcompany.company_name,    
                })
        res = {
            'company_names': ctx,    
        }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype="application/json")

class AddTransportationCompany(View):

    def post(self, request, *args, **kwargs):

        if len(request.POST['new_company']) > 0 and not request.POST['new_company'].isspace():
            new_company, created = TransportationCompany.objects.get_or_create(company_name=request.POST['new_company']) 
            if not created:
                res = {
                    'result': 'error',
                    'message': 'Company name already exists'
                }
            else:
                res = {
                    'result': 'ok',
                    'company_name': new_company.company_name
                }
        else:
            res = {
                 'result': 'error',
                 'message': 'Company name cannot be null'
            }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')
