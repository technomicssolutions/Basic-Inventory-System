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
    ReceiptVoucher, CustomerAccount
from inventory.models import Item, InventoryItem
from web.models import Customer

from reportlab.pdfgen import canvas
from reportlab.lib.colors import black

def header(canvas, y):

    canvas.setFont("Helvetica", 30)  
    canvas.setFillColor(black)
    canvas.drawString(50, y + 21, 'Mubeena Furniture and Home Appliances')
    canvas.setFont("Helvetica", 18)  
    canvas.drawString(50, y - 15, 'Karimpulli')
    canvas.drawString(50, y - 35, 'Shop: 8086 615 615')
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

def dn_body_layout(canvas, y, delivery_note):

    canvas.setFont("Helvetica-Bold", 40)  
    canvas.drawString(350, y - 80, 'Delivery Note')
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
    canvas.drawString(865,  y - 60, 'DN No #')

    canvas.drawString(100, y - 150, 'Bill To')
    canvas.drawString(550, y - 150, 'Ship To')

    canvas.drawString(725,  y - 85, delivery_note.date.strftime('%d-%b-%Y'))
    canvas.drawString(865,  y - 85, delivery_note.delivery_note_number)

    canvas.drawString(70, y - 180, delivery_note.customer.customer_name)
    canvas.drawString(70, y - 200, delivery_note.customer.house_name)
    canvas.drawString(70, y - 220, delivery_note.customer.street)
    canvas.drawString(165, y - 220, ',' if delivery_note.customer.street and delivery_note.customer.city else '')
    canvas.drawString(172, y - 220, delivery_note.customer.city)

    canvas.drawString(510, y - 180, delivery_note.customer.customer_name)
    canvas.drawString(510, y - 200, delivery_note.customer.house_name)
    canvas.drawString(510, y - 220, delivery_note.customer.street)
    canvas.drawString(605, y - 220, ',' if delivery_note.customer.street and delivery_note.customer.city else '')
    canvas.drawString(612, y - 220, delivery_note.customer.city)

    canvas.line(50, y - 270, 950, y - 270)  

    canvas.line(50, y - 270, 50, y - 980) 
    canvas.line(950, y - 270, 950, y - 980) 

    canvas.line(50, y - 300, 950, y - 300) 
    
    canvas.line(150, y - 270, 150, y - 980) 
    canvas.line(300, y - 270, 300, y - 980)
    canvas.line(675, y - 270, 675, y - 980)  
    canvas.line(815, y - 270, 815, y - 980) 

    canvas.line(50, y - 980, 950, y - 980)

    canvas.drawString(60, y - 290, 'Quantity')
    canvas.drawString(190, y - 290, 'Item Code')
    canvas.drawString(450, y - 290, 'Item Name')
    canvas.drawString(710, y - 290, 'Price Each')
    canvas.drawString(850, y - 290, 'Amount')

    return canvas


class SalesEntry(View):
    def get(self, request, *args, **kwargs):
        
        sales_type = request.GET.get('sales_type', '')

        if sales_type == 'project_sales':
            template_name = 'sales/sales_entry.html'
        elif sales_type == 'dn_sales':
            template_name = 'sales/DN_sales_entry.html'
        elif sales_type == 'inventory_sales':
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
            current_stock = 0
            for s_item in invoice.salesitem_set.all():
                if s_item.item.item_type == 'item':
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
                
                'delivery_note_no': invoice.delivery_note.delivery_note_number if invoice.delivery_note else '',
                'lpo_number': invoice.delivery_note.lpo_number if invoice.delivery_note else '',
                'sales_items': ctx_item_list,
                'po_no': invoice.po_no if invoice.po_no else '',
                'terms': invoice.terms if invoice.terms else '',
                'rep': invoice.rep if invoice.rep else '',
                'via': invoice.via if invoice.via else '',
                'fob': invoice.fob if invoice.fob else '',
                'status': invoice.status if invoice.status else '',
            })
        for invoice in whole_invoices:
            ctx_item_list = []
            current_stock = 0
            for s_item in invoice.salesitem_set.all():
                if s_item.item.item_type == 'item':
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
                
                'dn_no': invoice.delivery_note.delivery_note_number if invoice.delivery_note else '',
                'lpo_no': invoice.delivery_note.lpo_number if invoice.delivery_note else '',
                'sales_items': ctx_item_list,
                'po_no': invoice.po_no if invoice.po_no else '',
                'terms': invoice.terms if invoice.terms else '',
                'rep': invoice.rep if invoice.rep else '',
                'via': invoice.via if invoice.via else '',
                'fob': invoice.fob if invoice.fob else '',
                'status': invoice.status if invoice.status else '',
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
            if item.item_type == 'item':
                inventory = InventoryItem.objects.get(item=item)
                inventory.quantity = int(inventory.quantity) + int(r_item['qty_sold'])
                s_item = SalesItem.objects.get(item=item, sales=sales)
                s_item.delete()

        for item in sales_items:
            item_obj = Item.objects.get(code=item['item_code'])
            s_item = SalesItem.objects.get(item=item_obj, sales=sales)
            if int(s_item.quantity_sold) != int(item['qty_sold']):
                if item_obj.item_type == 'item':
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

class PrintDeliveryNotes(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'sales/print_delivery_note.html', {})

class PrintSalesInvoice(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'sales/print_invoice.html', {})

class CheckDeliverynoteExistence(View):

    def get(self, request, *args, **kwargs):

        delivery_no = request.GET.get('delivery_no', '')
        try:
            delivery_note = DeliveryNote.objects.get(delivery_note_number=delivery_no)
            res = {
                'result': 'error',
            }
        except Exception as ex:

            res = {
                'result': 'ok',
            }

        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')

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
