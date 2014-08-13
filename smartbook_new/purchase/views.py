import ast
import simplejson
import datetime as dt
from datetime import datetime

from django.shortcuts import get_object_or_404, render
from django.views.generic.base import View
from django.http import  HttpResponse, HttpResponseRedirect

from django.contrib.auth.models import User
from django.db.models import Max

from web.models import Supplier,Customer,TransportationCompany,OwnerCompany
from purchase.models import Purchase,PurchaseItem,SupplierAccount,SupplierAccountDetail
from inventory.models import Item, InventoryItem, OpeningStock

from expenses.models import Expense, ExpenseHead

class PurchaseEntry(View):

    def get(self, request, *args, **kwargs):
        
        purchase_type = request.GET.get('purchase_type', '')
        if purchase_type == 'inventory_based':
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
                
            except:
                pass
        supplier = Supplier.objects.get(name=purchase_dict['supplier_name']) 
        if purchase_dict['transport'] != 'other' or purchase_dict['transport'] != 'select' or purchase_dict['transport'] != '': 
            try:     
                transport = TransportationCompany.objects.get(company_name=purchase_dict['transport'])
                purchase.transportation_company = transport
            except:
                pass
        purchase.supplier = supplier
        
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

        supplier_account, supplier_account_created = SupplierAccount.objects.get_or_create(supplier=supplier)
        if supplier_account_created:
            supplier_account.total_amount = purchase_dict['supplier_amount']
            supplier_account.balance = purchase_dict['supplier_amount']
        else:
            if purchase_created:
                supplier_account.total_amount = supplier_account.total_amount + purchase_dict['supplier_amount']
                supplier_account.balance = supplier_account.balance + purchase_dict['supplier_amount']
            else:
                supplier_account.total_amount = supplier_account.total_amount - purchase.supplier_amount + purchase_dict['supplier_amount']
                supplier_account.balance = supplier_account.balance - purchase.supplier_amount + purchase_dict['supplier_amount']
        supplier_account.save()       
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
            expense.created_by = request.user
            expense.expense_head, created = ExpenseHead.objects.get_or_create(expense_head = 'purchase')
            expense.date = dt.datetime.now().date().strftime('%Y-%m-%d')
            expense.amount = purchase_dict['purchase_expense']
            expense.payment_mode = 'cash'
            expense.narration = 'By purchase'      

        purchase_items = purchase_dict['purchase_items']
        deleted_items = purchase_dict['deleted_items']
        purchase.save()
        
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
                    # 'vendor_account_date' : vendor_account.date.strftime('%d/%m/%Y') if vendor_account.date else '',
                    'payment_mode': 'cash',
                    # 'narration': vendor_account.narration,
                    'total_amount': vendor_account.total_amount,
                    'amount_paid': vendor_account.paid_amount,
                    'balance_amount': vendor_account.balance,
                    # 'cheque_date': vendor_account.cheque_date.strftime('%d/%m/%Y') if vendor_account.cheque_date else '',
                    # 'cheque_no': vendor_account.cheque_no,
                    # 'bank_name': vendor_account.bank_name,
                    # 'branch_name': vendor_account.branch_name,
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
        # vendor_account.total_amount = int(vendor_account_dict['total_amount'])
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

