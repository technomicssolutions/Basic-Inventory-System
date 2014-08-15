import ast
import simplejson
import datetime as dt
from datetime import datetime

from django.shortcuts import render
from django.views.generic.base import View
from django.http import  HttpResponse, HttpResponseRedirect

from django.contrib.auth.models import User
from django.db.models import Max

from web.models import Supplier, Customer, TransportationCompany, OwnerCompany
from purchase.models import Purchase, PurchaseItem, SupplierAccount, SupplierAccountPayment, SupplierAccountPaymentDetail, PurchaseReturn, PurchaseReturnItem
from inventory.models import Item, InventoryItem, OpeningStock
from expenses.models import Expense, ExpenseHead

class PurchaseEntry(View):

    def get(self, request, *args, **kwargs):
        
        template_name = 'purchase/inventory_purchase_entry.html'
        if Purchase.objects.exists():
            invoice_number = int(Purchase.objects.aggregate(Max('purchase_invoice_number'))['purchase_invoice_number__max']) + 1
        else:
            invoice_number = 1
        if not invoice_number:
            invoice_number = 1
        return render(request, template_name,{
            'invoice_number': invoice_number,
        })

    def post(self, request, *args, **kwargs):
        
        purchase_dict = ast.literal_eval(request.POST['purchase'])
        purchase, purchase_created = Purchase.objects.get_or_create(purchase_invoice_number=purchase_dict['purchase_invoice_number'])

        purchase.purchase_invoice_number = purchase_dict['purchase_invoice_number']
        purchase.supplier_invoice_number = purchase_dict['supplier_invoice_number']
        purchase.supplier_do_number = purchase_dict['supplier_do_number']
        purchase.supplier_invoice_date = datetime.strptime(purchase_dict['supplier_invoice_date'], '%d/%m/%Y')
        purchase.purchase_invoice_date = datetime.strptime(purchase_dict['purchase_invoice_date'], '%d/%m/%Y')
        purchase.payment_mode = purchase_dict['payment_mode']
        if purchase_dict['payment_mode'] == 'cash' or purchase_dict['payment_mode'] == 'cheque':
            purchase.is_paid_completely = True 
        if purchase_dict['bank_name']:
            purchase.bank_name = purchase_dict['bank_name']
        if purchase_dict['cheque_no']:
            purchase.cheque_no = purchase_dict['cheque_no']
        if purchase_dict['cheque_date']:
            purchase.cheque_date = datetime.strptime(purchase_dict['cheque_date'], '%d/%m/%Y')
        if purchase_dict['supplier_name'] != 'other' or purchase_dict['supplier_name'] != 'select' or purchase_dict['supplier_name'] != '': 
            try:     
                supplier = Supplier.objects.get(name=purchase_dict['supplier_name']) 
                purchase.supplier = supplier
            except:
                pass

        supplier = Supplier.objects.get(name=purchase_dict['supplier_name']) 
        if purchase_created:
            supplier_payment_detail = SupplierAccountPaymentDetail()
        else:
            print purchase.supplieraccountpaymentdetail_set.all().count()
            print (purchase.supplieraccountpaymentdetail_set.all())
            supplier_payment_detail = purchase.supplieraccountpaymentdetail_set.all()[0]
        supplier_payment_detail.supplier = supplier
        supplier_payment_detail.date = purchase.purchase_invoice_date 
        supplier_payment_detail.purchase = purchase

        if purchase_dict['transport'] != 'other' or purchase_dict['transport'] != 'select' or purchase_dict['transport'] != '': 
            try:     
                transport = TransportationCompany.objects.get(company_name=purchase_dict['transport'])
                purchase.transportation_company = transport
            except:
                pass
        
        if purchase_dict['discount']:
            purchase.discount = purchase_dict['discount']
        else:
            purchase.discount = 0
        if purchase_dict['discount_percentage']:
            purchase.discount_percentage = purchase_dict['discount_percentage']
        else:
            purchase.discount_percentage = 0
        purchase.net_total = purchase_dict['net_total']
        purchase.purchase_expense = purchase_dict['purchase_expense']
        purchase.grant_total = purchase_dict['grant_total']
        supplier_payment_detail.total_amount = purchase.grant_total
        if purchase.payment_mode == 'cash':
            supplier_payment_detail.paid = purchase.grant_total
            supplier_payment_detail.payment_mode = 'Cash(purchase)'
        elif purchase.payment_mode == 'cheque':
            supplier_payment_detail.payment_mode = 'Cheque(purchase)'
            supplier_payment_detail.paid = purchase.grant_total
        else:
            supplier_payment_detail.payment_mode = 'Credit(purchase)'
            supplier_payment_detail.balance = purchase_dict['supplier_amount']
        supplier_payment_detail.save()
        purchase.supplier_amount = purchase_dict['supplier_amount']
        purchase.save()
        
        if float(purchase_dict['purchase_expense']) > 0:
            # Save purchase_expense in Expense
            try: 
                expense = Expense.objects.get(purchase=purchase)
            except:
                if Expense.objects.exists():
                    voucher_no = int(Expense.objects.aggregate(Max('voucher_no'))['voucher_no__max']) + 1
                else:
                    voucher_no = 1
                if not voucher_no:
                    voucher_no = 1
                expense = Expense.objects.create(purchase=purchase, created_by=request.user, voucher_no=voucher_no)
            expense.expense_head, created = ExpenseHead.objects.get_or_create(expense_head = 'purchase')
            expense.date = dt.datetime.now().date()
            expense.amount = purchase_dict['purchase_expense']
            expense.payment_mode = 'cash'
            expense.narration = 'By purchase'      
            expense.save()
        purchase_items = purchase_dict['purchase_items']
        deleted_items = purchase_dict['deleted_items']
        purchase.save()
        for deleted_item in deleted_items:
            item = Item.objects.get(code=deleted_item['item_code'])
            p_item, created = PurchaseItem.objects.get_or_create(item=item, purchase=purchase)
            inventory, created = InventoryItem.objects.get_or_create(item=item)
            inventory.quantity = inventory.quantity - p_item.quantity_purchased
            inventory.selling_price = deleted_item['selling_price']
            inventory.unit_price = deleted_item['unit_price']
            inventory.save() 
            p_item.delete()
        
        for purchase_item in purchase_items:

            item = Item.objects.get(code=purchase_item['item_code'])
            p_item, created = PurchaseItem.objects.get_or_create(item=item, purchase=purchase)
            inventory, created = InventoryItem.objects.get_or_create(item=item)
            if created:
                inventory.quantity = int(purchase_item['qty_purchased'])                
            else:
                if purchase_created:
                    inventory.quantity = inventory.quantity + int(purchase_item['qty_purchased'])
                else:
                    inventory.quantity = inventory.quantity - p_item.quantity_purchased + int(purchase_item['qty_purchased'])
            inventory.selling_price = purchase_item['selling_price']
            inventory.unit_price = purchase_item['unit_price']
            inventory.save()    
            p_item.purchase = purchase
            p_item.item = item
            p_item.quantity_purchased = purchase_item['qty_purchased']
            p_item.cost_price = purchase_item['cost_price']
            p_item.net_amount = purchase_item['net_amount']
            p_item.save()
                    
        res = {
            'result': 'Ok',
        } 
        response = simplejson.dumps(res)
        status_code = 200
        return HttpResponse(response, status = status_code, mimetype="application/json")

class VendorAccounts(View):
    def get(self, request, *args, **kwargs):
        vendor_accounts =  SupplierAccount.objects.all()
        vendors = Supplier.objects.all()
        return render(request, 'purchase/vendor_accounts.html', {
            'vendor_accounts' : vendor_accounts,
            'vendors': vendors
        })
        

class SupplierAccountDetails(View):
    def get(self, request, *args, **kwargs):
        try:
            supplier_id = request.GET['vendor']
            supplier = Supplier.objects.get(id=supplier_id)
            vendor_account =  SupplierAccount.objects.get(supplier=supplier)
            res = {
                'result': 'Ok',
                'vendor_account': {
                    'payment_mode': 'cash',
                    'total_amount': vendor_account.total_amount,
                    'amount_paid': vendor_account.paid_amount,
                    'balance_amount': vendor_account.balance,
                    'vendor': vendor_account.supplier.name
                }
            } 

            response = simplejson.dumps(res)
            status_code = 200
        except:
            res = {
                'result': 'error',
                'message': 'Vendor does not have any purchase details',
            }
            response = simplejson.dumps(res)
            status_code = 200
        return HttpResponse(response, status = status_code, mimetype="application/json")

    def post(self, request, *args, **kwargs):

        vendor_account_dict = ast.literal_eval(request.POST['vendor_account'])
        vendor = Supplier.objects.get(name=vendor_account_dict['vendor'])
        vendor_detail = SupplierAccountDetail()
        vendor_account, created =  SupplierAccount.objects.get_or_create(supplier=vendor) 
        vendor_account.date = datetime.strptime(vendor_account_dict['vendor_account_date'], '%d/%m/%Y')
        vendor_detail.date = vendor_account.date
        vendor_account.payment_mode = vendor_account_dict['payment_mode']
        vendor_account.narration = vendor_account_dict['narration']
        vendor_account.amount = int(vendor_account_dict['amount'])
        vendor_detail.amount = vendor_account.amount
        vendor_account.paid_amount = vendor_account.paid_amount + vendor_account.amount  #int(vendor_account_dict['amount_paid'])
        vendor_detail.opening_balance = vendor_account.balance
        vendor_account.balance = vendor_account.balance - vendor_account.amount  #int(vendor_account_dict['balance_amount'])
        vendor_detail.closing_balance = vendor_account.balance
        vendor_detail.supplier_account = vendor_account
        if vendor_account_dict['cheque_date']:
            vendor_account.cheque_no = vendor_account_dict['cheque_no']
            vendor_account.cheque_date = datetime.strptime(vendor_account_dict['cheque_date'], '%d/%m/%Y') 
            vendor_account.bank_name = vendor_account_dict['bank_name']
            vendor_account.branch_name = vendor_account_dict['branch_name']
        vendor_account.save()
        vendor_detail.save()
        response = {
                'result': 'Ok',
            }
        status_code = 200
        return HttpResponse(response, status = status_code, mimetype="application/json")

class PurchaseEdit(View):
    def get(self, request, *args, **kwargs):
        
        return render(request, 'purchase/edit_purchase.html',{})

class PurchaseDetail(View):

    def get(self, request, *args, **kwargs):
        try:
            invoice_number = request.GET.get('invoice_no', '')
            detail_type = request.GET.get('type', '')
            if detail_type == 'edit':
                purchase  = Purchase.objects.get(purchase_invoice_number=int(invoice_number), is_paid_completely=False)
            else:
                purchase  = Purchase.objects.get(purchase_invoice_number=int(invoice_number), is_paid_completely=True)
            purchase_items = PurchaseItem.objects.filter(purchase=purchase)
            items_list = []
            for item in purchase_items:
                inventory = InventoryItem.objects.get(item=item.item)
                
                items_list.append({
                    'item_code': item.item.code,
                    'item_name': item.item.name,
                    'current_stock': inventory.quantity,
                    'selling_price': inventory.selling_price,
                    'qty_purchased': item.quantity_purchased,
                    'cost_price': item.cost_price,
                    'net_amount': item.net_amount,
                    'unit_price': inventory.unit_price,
                })

            purchase_dict = {
                'purchase_invoice_number': purchase.purchase_invoice_number,
                'supplier_invoice_number': purchase.supplier_invoice_number,
                'supplier_do_number': purchase.supplier_do_number,
                'supplier_name': purchase.supplier.name,
                'transport': purchase.transportation_company.company_name if purchase.transportation_company else 'select',
                'supplier_invoice_date': purchase.supplier_invoice_date.strftime('%d/%m/%Y'),
                'purchase_invoice_date': purchase.purchase_invoice_date.strftime('%d/%m/%Y'), 
                'purchase_items': items_list,
                'supplier_amount': purchase.supplier_amount,
                'net_total': purchase.net_total,
                'purchase_expense': purchase.purchase_expense,
                'discount': purchase.discount,
                'grant_total': purchase.grant_total,
                'payment_mode': purchase.payment_mode,
                'bank_name': purchase.bank_name if purchase.bank_name else '',
                'cheque_no': purchase.cheque_no if purchase.cheque_no else '',
                'cheque_date': purchase.cheque_date.strftime('%d/%m/%Y') if purchase.cheque_date else '',
                'discount_percentage': purchase.discount_percentage,
                'discount': purchase.discount
            }
            res = {
                'result': 'Ok',
                'purchase': purchase_dict,
                'message': '',
            } 
            response = simplejson.dumps(res)
            status_code = 200
        except Exception as ex:
            res = {
                'message': 'No purchase with purchase no',
                'result': 'No item with this purchase no'+ str(ex),
                'purchase': {}
            } 
            response = simplejson.dumps(res)
            status_code = 200
        return HttpResponse(response, status = status_code, mimetype="application/json")

class PurchaseReturnView(View):

    def get(self, request, *args, **kwargs):
        if PurchaseReturn.objects.exists():
            invoice_number = int(PurchaseReturn.objects.aggregate(Max('return_invoice_number'))['return_invoice_number__max']) + 1
        else:
            invoice_number = 1
        if not invoice_number:
            invoice_number = 1
        return render(request, 'purchase/purchase_return.html', {
            'invoice_number' : invoice_number,
        })

    def post(self, request, *args, **kwargs):
        post_dict = ast.literal_eval(request.POST['purchase_return'])
        purchase = Purchase.objects.get(purchase_invoice_number=post_dict['purchase_invoice_number'])
        return_items = PurchaseReturn.objects.filter(purchase=purchase)
        return_amount = 0
        for return_item in return_items:
            return_amount = float(return_amount) + float(return_item.net_amount)
        purchase_return, created = PurchaseReturn.objects.get_or_create(purchase=purchase, return_invoice_number = post_dict['invoice_number'])
        purchase_return.date = datetime.strptime(post_dict['purchase_return_date'], '%d/%m/%Y')
        purchase_return.net_amount = post_dict['net_return_total']
        purchase_return.save()
        
        supplier_account = SupplierAccount.objects.get(supplier=purchase.supplier)
        supplier_account.total_amount = float(supplier_account.total_amount) - float(post_dict['net_return_total'])
        supplier_account.save()
        purchase.net_total_after_return = float(purchase.net_total) - (float(return_amount) + float(post_dict['net_return_total']))
        if purchase.net_total_after_return > 0 and purchase.net_total_after_return >= purchase.discount:
            purchase.grant_total_after_return = float(purchase.net_total_after_return) - float(purchase.discount)
        else:
            purchase.grant_total_after_return = purchase.net_total_after_return
        purchase.supplier_amount = purchase.grant_total_after_return
        purchase.save()
        return_items = post_dict['purchase_items']

        for item in return_items:
            return_item = Item.objects.get(code=item['item_code'])
            purchase_item = PurchaseItem.objects.get(item=return_item, purchase=purchase)
            p_return_item, created = PurchaseReturnItem.objects.get_or_create(item=return_item, purchase_return=purchase_return)
            p_return_item.amount = item['returned_amount']
            p_return_item.quantity = item['returned_quantity']
            p_return_item.purchased_quantity = purchase_item.quantity_purchased
            p_return_item.save()
            purchase_item.quantity_purchased = int(purchase_item.quantity_purchased) - int(item['returned_quantity'])
            purchase_item.net_amount = float(purchase_item.net_amount) - float(item['returned_amount'])
            purchase_item.save() 

            inventory = InventoryItem.objects.get(item=return_item)
            inventory.quantity = int(inventory.quantity) - int(item['returned_quantity'])
            inventory.save()
        response = {
                'result': 'Ok',
            }
        status_code = 200
        return HttpResponse(response, status = status_code, mimetype="application/json")



