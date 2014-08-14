# -*- coding: utf-8 -*- 
import ast
import simplejson
import datetime as dt
from datetime import datetime
from decimal import *

from django.db.models import Max
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse

from sales.models import Sales, SalesItem, \
    ReceiptVoucher, CustomerAccount, SalesReturn, SalesReturnItem
from inventory.models import Item, InventoryItem
from web.models import Customer, OwnerCompany

from reportlab.pdfgen import canvas

def header(canvas, y):
    try:
        owner_company = OwnerCompany.objects.latest('id')
    except:
        owner_company = None
    canvas.setFont("Helvetica", 30) 
    canvas.drawString(50, y + 21, (owner_company.company_name if owner_company else ''))
    canvas.setFont("Helvetica", 18)  
    address = (owner_company.address1 + (' , '+owner_company.street if owner_company.street else '') if owner_company else '')
    canvas.drawString(50, y - 15, address)
    city_state_country = (owner_company.city + (' , '+owner_company.state if owner_company.state else '')+(' , '+owner_company.country if owner_company.country else '') if owner_company else '')
    canvas.drawString(50, y - 35, city_state_country)
    return canvas

def invoice_body_layout(canvas, y, sales):

    canvas.setFont("Helvetica-Bold", 40)
    if sales.status == 'estimate':
        canvas.drawString(350, y - 80, 'Estimate')
    else:
        canvas.drawString(350, y - 80, 'Invoice')
    canvas.setFont("Helvetica", 15)

    # Date and Invoice Box start
    canvas.line(700, y - 45, 950, y - 45)
    canvas.line(700, y - 100, 950, y - 100)  
    canvas.line(700, y - 70, 950, y - 70)  

    canvas.line(700, y - 45, 700, y - 100)  
    canvas.line(950, y - 45, 950, y - 100)
    canvas.line(825, y - 45, 825, y - 100)
    # Date and Invoice Box end

    # Bill and Ship Box start

    canvas.line(50, y - 130, 400, y - 130)
    canvas.line(50, y - 160, 400, y - 160)
    canvas.line(50, y - 250, 400, y - 250)

    canvas.line(500, y - 130, 900, y - 130)
    canvas.line(500, y - 160, 900, y - 160)
    canvas.line(500, y - 250, 900, y - 250)
    
    canvas.line(50, y - 130, 50, y - 250)  
    canvas.line(400, y - 130, 400, y - 250)
    canvas.line(500, y - 130, 500, y - 250)  
    canvas.line(900, y - 130, 900, y - 250)

    # Bill and Ship Box end

    canvas.setFont("Helvetica", 14)
    canvas.drawString(745,  y - 60, 'Date')
    canvas.drawString(865,  y - 60, 'Invoice #')

    canvas.drawString(100, y - 150, 'Bill To')
    canvas.drawString(550, y - 150, 'Ship To')

    canvas.line(50, y - 340, 950, y - 340) 

    canvas.line(50, y - 340, 50, y - 980) 
    canvas.line(950, y - 340, 950, y - 980) 

    canvas.line(50, y - 370, 950, y - 370) 
    
    canvas.line(150, y - 340, 150, y - 980) 
    canvas.line(300, y - 340, 300, y - 980)
    canvas.line(675, y - 340, 675, y - 980)  
    canvas.line(815, y - 340, 815, y - 980) 

    canvas.line(50, y - 980, 950, y - 980)
    

    canvas.drawString(60, y - 360, 'Quantity')
    canvas.drawString(190, y - 360, 'Item Code')
    canvas.drawString(450, y - 360, 'Item Name')
    canvas.drawString(710, y - 360, 'Price Each')
    canvas.drawString(850, y - 360, 'Amount')

    canvas.drawString(725,  y - 85, sales.sales_invoice_date.strftime('%d-%b-%Y'))
    canvas.drawString(865,  y - 85, sales.sales_invoice_number)

    canvas.drawString(70, y - 180, sales.customer.customer_name)
    canvas.drawString(70, y - 200, sales.customer.house_name)
    canvas.drawString(70, y - 220, sales.customer.street)
    canvas.drawString(165, y - 220, ',' if sales.customer.city and sales.customer.street else '')
    canvas.drawString(172, y - 220, sales.customer.city)

    canvas.drawString(510, y - 180, sales.customer.customer_name)
    canvas.drawString(510, y - 200, sales.customer.house_name)
    canvas.drawString(510, y - 220, sales.customer.street)
    canvas.drawString(605, y - 220, ',' if sales.customer.city and sales.customer.street else '')
    canvas.drawString(612, y - 220, sales.customer.city)

    canvas.setFont('Times-Roman', 14)
    return canvas 

class SalesEntry(View):
    def get(self, request, *args, **kwargs):
        
        template_name = 'sales/inventory_sales_entry.html'
        current_date = dt.datetime.now().date()
        inv_number = Sales.objects.aggregate(Max('id'))['id__max']

        if not inv_number:
            inv_number = 1
        else:
            inv_number = inv_number + 1
        
        invoice_number = 'INV' + str(inv_number)
        return render(request, template_name,{
            'sales_invoice_number': invoice_number,
            'current_date': current_date.strftime('%d/%m/%Y'),
        })


    def post(self, request, *args, **kwargs):

        sales_dict = ast.literal_eval(request.POST['sales'])
        sales, sales_created = Sales.objects.get_or_create(sales_invoice_number=sales_dict['sales_invoice_number'])
        
        customer = Customer.objects.get(customer_name=sales_dict['customer'])
        sales.customer = customer
        sales.sales_invoice_number = sales_dict['sales_invoice_number']
        sales.payment_mode = sales_dict['payment_mode']
        
        sales.sales_invoice_date = datetime.strptime(sales_dict['sales_invoice_date'], '%d/%m/%Y')
        
        sales.discount_for_sale = sales_dict['discount']
        sales.discount_percentage_for_sale = sales_dict['discount_percentage']
        sales.round_off = sales_dict['roundoff']
        sales.net_amount = sales_dict['net_total']
        sales.grant_total = sales_dict['grant_total']
        sales.paid = sales_dict['paid']
        sales.status = sales_dict['status']

        if sales_dict['payment_mode'] == 'cheque':
            sales.cheque_no = sales_dict['cheque_no'] 
            sales.bank_name = sales_dict['bank_name']
            sales.bank_branch = sales_dict['branch']
            sales.cheque_date = datetime.strptime(sales_dict['cheque_date'], '%d/%m/%Y')

        if sales_dict['payment_mode'] == 'cheque' or sales_dict['payment_mode'] == 'cash':
            sales.is_processed = True
            sales.paid = sales_dict['grant_total']
        sales.balance = float(sales.grant_total) - float(sales.paid)
        sales.save()

        sales_items = sales_dict['sales_items']
        removed_items = sales_dict['removed_items']
        sales.save()

        for r_item in removed_items:
            item = Item.objects.get(code=r_item['item_code'])
            inventory = InventoryItem.objects.get(item=d_item.item)
            inventory.quantity = int(inventory.quantity) + int(r_item['qty_sold'])
            inventory.save()

         
        for sales_item in sales_items:
            item = Item.objects.get(code=sales_item['item_code'])
            s_item, item_created = SalesItem.objects.get_or_create(item=item, sales=sales)
            
            inventory = InventoryItem.objects.get(item=item)
            if item_created:
                inventory.quantity = inventory.quantity - int(sales_item['qty_sold'])
            else:
                inventory.quantity = int(inventory.quantity) + int(s_item.quantity_sold) - int(sales_item['qty_sold'])      
            inventory.save()
            s_item.quantity_sold = sales_item['qty_sold']
            s_item.net_amount = sales_item['net_amount']
            s_item.selling_price = sales_item['unit_price']
            s_item.save()

        res = {
            'result': 'Ok',
            'id': sales.id,
        }
        response = simplejson.dumps(res)
        status_code = 200
        return HttpResponse(response, status = status_code, mimetype="application/json")

class ReceiptVoucherView(View):

    def get(self, request, *args, **kwargs):
        current_date = dt.datetime.now().date()
        voucher_no = ReceiptVoucher.objects.aggregate(Max('id'))['id__max']
        prefix = 'RV'
        if not voucher_no:
            voucher_no = 1
        else:
            voucher_no = voucher_no + 1
        voucher_no = prefix + str(voucher_no)

        return render(request, 'sales/receipt_voucher.html',{
            'current_date': current_date.strftime('%d/%m/%Y'),
            'voucher_no': voucher_no,
        })
    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            receiptvoucher = ast.literal_eval(request.POST['receiptvoucher'])
            customer = Customer.objects.get(customer_name=receiptvoucher['customer'])
            sales_invoice_obj = Sales.objects.get(sales_invoice_number=receiptvoucher['invoice_no'])
            receipt_voucher = ReceiptVoucher.objects.create(sales_invoice=sales_invoice_obj)

            receipt_voucher.date = datetime.strptime(receiptvoucher['date'], '%d/%m/%Y')
            
            receipt_voucher.total_amount = receiptvoucher['amount']
            receipt_voucher.paid_amount = receiptvoucher['paid_amount']
            receipt_voucher.receipt_voucher_no = receiptvoucher['voucher_no']
            receipt_voucher.payment_mode = receiptvoucher['payment_mode']
            receipt_voucher.bank = receiptvoucher['bank_name']
            receipt_voucher.cheque_no = receiptvoucher['cheque_no']
            if receiptvoucher['cheque_date']:   
                receipt_voucher.dated = datetime.strptime(receiptvoucher['cheque_date'], '%d/%m/%Y')
            receipt_voucher.save()
            customer_account, created = CustomerAccount.objects.get_or_create(customer=customer, invoice_no=sales_invoice_obj )
 
            if created:
                customer_account.total_amount = receiptvoucher['amount']
                customer_account.paid = receiptvoucher['paid_amount']
            else:
                customer_account.total_amount = receiptvoucher['amount']
                customer_account.paid = float(customer_account.paid) + float(receiptvoucher['paid_amount'])
            customer_account.save()
            customer_account.balance = float(customer_account.total_amount) - float(customer_account.paid)
            customer_account.save()
            sales_invoice_obj.balance = customer_account.balance
            sales_invoice_obj.save()
            if customer_account.balance == 0:
                customer_account.is_complted = True
                customer_account.save()
                sales_invoice_obj.is_processed = True
                sales_invoice_obj.save()
           
            res = {
                'result': 'OK',
                'receiptvoucher_id': receipt_voucher.id,
            }

            response = simplejson.dumps(res)

            return HttpResponse(response, status=200, mimetype='application/json')  


class InvoiceDetails(View):

    def get(self, request, *args, **kwargs):
        invoice_no = request.GET.get('invoice_no', '')
        ctx_rv_invoice_details = []
        ctx_invoice_details = []
        ctx_whole_invoices = []
        invoice_details = Sales.objects.filter(sales_invoice_number__istartswith=invoice_no, is_processed=False, payment_mode='credit')
        try:
            invoices = Sales.objects.filter(sales_invoice_number=invoice_no, is_processed=False)
        except Exception as ex:
            invoices = []
        whole_invoices = Sales.objects.filter(sales_invoice_number=invoice_no)
        status = 200
        for invoice in invoice_details:
            customer_account, created = CustomerAccount.objects.get_or_create(customer=invoice.customer, invoice_no=invoice)
            ctx_rv_invoice_details.append({
                'invoice_no': invoice.sales_invoice_number if invoice else '',
                'invoice_date': invoice.sales_invoice_date.strftime('%d/%m/%Y') if invoice else '',
                'amount': float(invoice.grant_total) - float(invoice.paid) if invoice else '',
                'customer': invoice.customer.customer_name if invoice.customer else '',
                'paid_amount': customer_account.paid if customer_account.paid else 0,
            })
        for invoice in invoices:
            ctx_item_list = []
            for s_item in invoice.salesitem_set.all():
                inventory = InventoryItem.objects.get(item=s_item.item)
                current_stock = inventory.quantity
                ctx_item_list.append({
                    'item_name': s_item.item.name,
                    'item_code': s_item.item.code,
                    'current_stock': current_stock,
                    'unit_price': s_item.selling_price,
                    'qty_sold': s_item.quantity_sold,
                    'net_amount': s_item.net_amount,
                })
            ctx_invoice_details.append({
                'invoice_no': invoice.sales_invoice_number,
                'date': invoice.sales_invoice_date.strftime('%d/%m/%Y') if invoice.sales_invoice_date else '',
                'customer': invoice.customer.customer_name,
                'payment_mode': invoice.payment_mode,
                'net_total': invoice.net_amount,
                'grant_total': invoice.grant_total,
                'discount_sale': invoice.discount_for_sale,
                'discount_percentage': invoice.discount_percentage_for_sale,
                'roundoff': invoice.round_off,
                'paid': invoice.paid,
                'balance': invoice.balance,
                'sales_items': ctx_item_list,
                'status': invoice.status if invoice.status else '',
            })
        for invoice in whole_invoices:
            ctx_item_list = []
            current_stock = 0
            for s_item in invoice.salesitem_set.all():
                inventory = InventoryItem.objects.get(item=s_item.item)
                current_stock = inventory.quantity
                ctx_item_list.append({
                    'item_name': s_item.item.name,
                    'item_code': s_item.item.code,
                    'current_stock': current_stock,
                    'unit_price': s_item.selling_price,
                    'qty_sold': s_item.quantity_sold,
                    'net_amount': s_item.net_amount,
                })
                current_stock = 0
            ctx_whole_invoices.append({
                'id': invoice.id,
                'invoice_no': invoice.sales_invoice_number,
                'date': invoice.sales_invoice_date.strftime('%d/%m/%Y') if invoice.sales_invoice_date else '',
                'customer': invoice.customer.customer_name,
                'payment_mode': invoice.payment_mode,
                'net_total': invoice.net_amount,
                'grant_total': invoice.grant_total,
                'discount_sale': invoice.discount_for_sale,
                'discount_percentage': invoice.discount_percentage_for_sale,
                'roundoff': invoice.round_off,
                'paid': invoice.paid,
                'balance': invoice.balance,
                'status': invoice.status if invoice.status else '',
                'sales_items': ctx_item_list,
            })

        res = {
            'result': 'ok',
            'rv_invoice_details': ctx_rv_invoice_details,
            'sales_invoices': ctx_invoice_details,
            'whole_invoices': ctx_whole_invoices,
        }
        response = simplejson.dumps(res)

        return HttpResponse(response, status=status, mimetype='application/json')

class EditSalesInvoice(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'sales/edit_sales_invoice.html', {})

    def post(self, request, *args, **kwargs):

        sales_dict = ast.literal_eval(request.POST['sales'])
        sales = Sales.objects.get(sales_invoice_number=sales_dict['invoice_no'])

        sales.payment_mode = sales_dict['payment_mode']
        
        sales.sales_invoice_date = datetime.strptime(sales_dict['date'], '%d/%m/%Y')
    
        sales.status = sales_dict['status']

        sales.discount_for_sale = sales_dict['discount_sale']
        sales.discount_percentage_for_sale = sales_dict['discount_percentage']
        sales.round_off = sales_dict['roundoff']
        sales.net_amount = sales_dict['net_total']
        sales.grant_total = sales_dict['grant_total']
        sales.paid = float(sales.paid) + float(sales_dict['paid'])
        customer = Customer.objects.get(customer_name=sales_dict['customer'])
        sales.customer = customer
        if sales_dict['payment_mode'] == 'cheque':
            sales.cheque_no = sales_dict['cheque_no'] 
            sales.bank_name = sales_dict['bank_name']
            sales.bank_branch = sales_dict['branch']
            sales.cheque_date = datetime.strptime(sales_dict['cheque_date'], '%d/%m/%Y')
        if sales_dict['payment_mode'] == 'cheque' or sales_dict['payment_mode'] == 'cash':
            sales.is_processed = True
            sales.paid = sales_dict['grant_total']
        sales.balance = float(sales.grant_total) - float(sales.paid)
        sales.save()

        sales_items = sales_dict['sales_items']
        removed_items = sales_dict['removed_items']
        for r_item in removed_items:
            item = Item.objects.get(code=r_item['item_code'])
            inventory = InventoryItem.objects.get(item=item)
            inventory.quantity = int(inventory.quantity) + int(r_item['qty_sold'])
            inventory.save()
            s_item = SalesItem.objects.get(item=item, sales=sales)
            s_item.delete()

        for item in sales_items:
            item_obj = Item.objects.get(code=item['item_code'])
            s_item = SalesItem.objects.get(item=item_obj, sales=sales)
            if int(s_item.quantity_sold) != int(item['qty_sold']):
                inventory = InventoryItem.objects.get(item=item_obj)
                inventory.quantity = int(inventory.quantity) + int(s_item.quantity_sold) - int(item['qty_sold'])
                inventory.save()
                s_item.quantity_sold = item['qty_sold']
            s_item.net_amount = item['net_amount']
            s_item.selling_price = item['unit_price']
            s_item.save()
        res = {
            'result': 'Ok',
            'id': sales.id,
        }
        response = simplejson.dumps(res)
        status_code = 200
        return HttpResponse(response, status = status_code, mimetype="application/json")

class SalesInvoicePDF(View):

    def get(self, request, *args, **kwargs):

        invoice_id = kwargs['invoice_id']
        sales = Sales.objects.get(id=invoice_id)

        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1000, 1250))
        y = 1150
        
        p = invoice_body_layout(p, y, sales)
        p = header(p, y)

        total_amount = 0
        y1 = y - 400
        p.setFont('Helvetica', 14)
        for s_item in sales.salesitem_set.all():
                        
            if y1 <= 170:
                y1 = y - 400
                p.showPage()
                
                p = invoice_body_layout(p, y, sales)
                p = header(p, y)

            p.drawString(60, y1, str(s_item.quantity_sold))
            p.drawString(190, y1, str(s_item.item.code))
            p.drawString(350, y1, str(s_item.item.name))
            p.drawString(710, y1, str(s_item.selling_price))
            p.drawString(850, y1, str(s_item.net_amount))

            total_amount = total_amount + s_item.net_amount

            y1 = y1 - 30

        #  total box start 
        p.line(50, y - 1040, 950, y - 1040)
        p.line(650, y - 980, 650, y - 1040)
        p.line(50, y - 980, 50, y - 1040)
        p.line(950, y - 980, 950, y - 1040)

        # total box end
        p.drawString(820, y - 995, 'Rs')
        p.drawString(850, y - 995, str(total_amount))

        # p.setFont("Helvetica-Bold", 30)  
        p.drawString(660, y - 995, 'Total')
        
        p.drawString(820, y - 1015, 'Rs')
        p.drawString(850, y - 1015, str(sales.discount_for_sale))
        p.drawString(660, y - 1015, 'Discount')

        p.drawString(820, y - 1035, 'Rs')
        p.drawString(850, y - 1035, str(sales.grant_total))
        p.drawString(660, y - 1035, 'Grant Total')
        # Item Box end

        p.showPage()
        p.save()
         
        return response

class PrintSalesInvoice(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'sales/print_invoice.html', {})


class CheckInvoiceExistence(View):

    def get(self, request, *args, **kwargs):

        invoice_no = request.GET.get('invoice_no', '')
        try:
            invoice = Sales.objects.get(sales_invoice_number=invoice_no)
            res = {
                'result': 'error',
            }
        except Exception as ex:

            res = {
                'result': 'ok',
            }

        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')

class CheckReceiptVoucherExistence(View):

    def get(self, request, *args, **kwargs):

        rv_no = request.GET.get('rv_no', '')
        try:
            receiptvoucher = ReceiptVoucher.objects.get(receipt_voucher_no=rv_no)
            res = {
                'result': 'error',
            }
        except Exception as ex:

            res = {
                'result': 'ok',
            }

        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')

class SalesReturnView(View):
    def get(self, request, *args, **kwargs):
        if SalesReturn.objects.exists():
            invoice_number = int(SalesReturn.objects.aggregate(Max('return_invoice_number'))['return_invoice_number__max']) + 1
        else:
            invoice_number = 1
        if not invoice_number:
            invoice_number = 1
        return render(request, 'sales/sales_return.html', {
            'invoice_number' : invoice_number,
        })

    def post(self, request, *args, **kwargs):
        post_dict = ast.literal_eval(request.POST['sales_return'])
        sales = Sales.objects.get(sales_invoice_number=post_dict['sales_invoice_number'])
        sales_return, created = SalesReturn.objects.get_or_create(sales=sales, return_invoice_number = post_dict['invoice_number'])
        sales_return.date = datetime.strptime(post_dict['sales_return_date'], '%d/%m/%Y')
        sales_return.net_amount = post_dict['net_return_total']
        sales_return.save() 
        sales.net_amount = float(sales.net_amount) - float(post_dict['net_return_total'])
        sales.grant_total = float(sales.grant_total) - float(post_dict['net_return_total'])
        sales.paid = float(sales.paid) - float(post_dict['net_return_total'])
        sales.save()

        return_items = post_dict['sales_items']

        for item in return_items:
            return_item = Item.objects.get(code=item['item_code'])
            sales_return_item = SalesItem.objects.get(sales=sales, item=return_item)
            s_return_item, created = SalesReturnItem.objects.get_or_create(item=return_item, sales_return=sales_return)
            s_return_item.amount = item['returned_amount']
            s_return_item.return_quantity = item['returned_quantity']
            s_return_item.sold_quantity = sales_return_item.quantity_sold
            s_return_item.save()
            sales_return_item.quantity_sold = int(sales_return_item.quantity_sold) - int(item['returned_quantity'])
            sales_return_item.net_amount = float(sales_return_item.net_amount) - float(item['returned_amount'])
            sales_return_item.save()
            inventory = InventoryItem.objects.get(item=return_item)
            inventory.quantity = inventory.quantity + int(item['returned_quantity'])
            inventory.save()
        response = {
                'result': 'Ok',
            }
        status_code = 200
        return HttpResponse(response, status = status_code, mimetype="application/json")

class SalesDetails(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            invoice_number = request.GET['invoice_no']
            try:
                sales = Sales.objects.get(sales_invoice_number=invoice_number)
            except:
                sales = None
            if sales:
                sales_items = SalesItem.objects.filter(sales=sales)

                sl_items = []

                for item in sales_items:
                    sl_items.append({
                        'item_code': item.item.code,
                        'item_name': item.item.name,
                        'stock': item.item.inventoryitem_set.all()[0].quantity,
                        'unit_price': item.item.inventoryitem_set.all()[0].selling_price,
                        'quantity_sold': item.quantity_sold,
                    })

                sales_dict = {
                    'invoice_number': sales.sales_invoice_number,
                    'sales_invoice_date': sales.sales_invoice_date.strftime('%d/%m/%Y'),
                    'customer': sales.customer.customer_name,
                    'net_amount': sales.net_amount,
                    'round_off': sales.round_off,
                    'grant_total': sales.grant_total,
                    'discount': sales.discount_for_sale,
                    'sales_items': sl_items
                }
                res = {
                    'result': 'Ok',
                    'sales': sales_dict
                }
            else:
                res = {
                    'result': 'No Sales entry for this invoice number',
                }
            response = simplejson.dumps(res)
            status_code = 200
            return HttpResponse(response, status = status_code, mimetype="application/json")

        return render(request, 'sales/view_sales.html',{})
