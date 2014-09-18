from datetime import datetime

from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle


from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.models import User
from django.http import HttpResponse

from sales.models import Sales, SalesReturn, CustomerPayment, CustomerAccount   
from expenses.models import Expense, ExpenseHead
from purchase.models import SupplierAccount, SupplierAccountPayment, SupplierAccountPaymentDetail, Purchase, PurchaseReturn
from web.models import OwnerCompany, Customer, Supplier

style = [
    ('FONTSIZE', (0,0), (-1, -1), 10),
    ('FONTNAME',(0,0),(-1,-1),'Helvetica') 
]
para_style = ParagraphStyle('fancy')
para_style.fontSize = 13
para_style.fontName = 'Helvetica'

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

class WholeSalesReport(View):

    def get(self, request, *args, **kwargs):    

        status_code = 200
        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1000, 1250))
        y = 1150
        p.setFontSize(15)
        p = header(p, y)

        report_type = request.GET.get('report_type', '')

        if not report_type:
            return render(request, 'reports/whole_sales_reports.html', {
                'report_type' : 'date',
                })

        if report_type == 'date': 

            start = request.GET['start_date']
            end = request.GET['end_date']
           
            if not start:            
                ctx = {
                    'msg' : 'Please Select Start Date',
                    'start_date' : start,
                    'end_date' : end,
                    'report_type' : 'date',
                }
                return render(request, 'reports/whole_sales_reports.html', ctx)
            elif not end:
                ctx = {
                    'msg' : 'Please Select End Date',
                    'start_date' : start,
                    'end_date' : end,
                    'report_type' : 'date',
                }
                return render(request, 'reports/whole_sales_reports.html', ctx)                  
            else:
                total = 0
                total_discount = 0
                total_discount_after_return = 0
                grant_total = 0
                p.setFont('Helvetica', 20)
                report_heading = 'Date Wise Sales Report' + ' - '+ start + ' - ' + end
                start_date = datetime.strptime(start, '%d/%m/%Y')
                end_date = datetime.strptime(end, '%d/%m/%Y')
                p.drawString(270, y - 70, report_heading)
                p.setFontSize(13)
                p.drawString(50, y - 100, "Date")
                p.drawString(110, y - 100, "Invoice Number")
                p.drawString(240, y - 100, "Customer")
                p.drawString(400, y - 100, "Net Total")
                p.drawString(580, y - 100, "Discount")
                p.drawString(480, y - 100, "Grant Total")

                sales = Sales.objects.filter(sales_invoice_date__gte=start_date,sales_invoice_date__lte=end_date, is_returned=False).order_by('sales_invoice_date')
                y1 = y - 110
                for sale in sales:
                    y1 = y1 - 30
                    if y1 <= 135:
                        y1 = y - 110
                        p.showPage()
                        p = header(p, y)
                            
                    total = float(total) + float(sale.net_amount)
                    grant_total = float(grant_total) + float(sale.grant_total)  
                    total_discount = float(total_discount) + float(sale.discount_for_sale)
                    p.drawString(50, y1, sale.sales_invoice_date.strftime('%d/%m/%y'))
                    p.drawString(120, y1, str(sale.sales_invoice_number))

                    p.drawString(240, y1, sale.customer.customer_name)
                    p.drawString(400, y1, str(sale.net_amount))
                    p.drawString(580, y1, str(sale.discount_for_sale))
                    p.drawString(480, y1, str(sale.grant_total))
                if y1 <= 135:
                    y1 = y - 110
                    p.showPage()
                    p = header(p, y)
                p.drawString(50, y1 - 60, 'Total Discount:')
                p.drawString(150, y1 - 60, str(total_discount))
                p.drawString(50, y1 - 80, 'Total Amount:')
                p.drawString(150, y1 - 80, str(total))
                p.drawString(50, y1 - 100, 'Grant Total:')
                p.drawString(150, y1 - 100, str(grant_total))
                p.showPage()
                p.save()
                return response


class ExpenseReport(View):

    def get(self, request, *args, **kwargs):

        status_code = 200
        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1000, 1250))
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        total_amount = 0

        if start_date is None:
            return render(request, 'reports/expense_report.html', {})
        if not start_date:            
            ctx = {
                'msg' : 'Please Select Start Date ',
                'start_date' : start_date,
                'end_date' : end_date,
            }
            return render(request, 'reports/expense_report.html', ctx)
        elif not end_date:
            ctx = {
                'msg' : 'Please Select End Date',
                'start_date' : start_date,
                'end_date' : end_date,
            }
            return render(request, 'reports/expense_report.html', ctx)

        else:       
        
            start = request.GET['start_date']
            end = request.GET['end_date']
            start_date = datetime.strptime(start, '%d/%m/%Y')
            end_date = datetime.strptime(end, '%d/%m/%Y')
            heading = 'Expense Report' + ' - ' + start + ' - ' + end
            p.setFontSize(20)
            y = 1150
            p.drawString(270, y - 70, heading)
            p.setFontSize(14)
            p.drawString(50, y - 100, "Date")
            p.drawString(150, y - 100, "Voucher No")
            p.drawString(250, y - 100, "Particulars")

            p.drawString(500, y - 100, "Narration")
            p.drawString(650, y - 100, "Amount") 
            
            p.setFontSize(12)
            p = header(p, y)
            head_name = request.GET.get('expense_head','')
            y1 = y - 130
            expense_head = None
            if head_name != 'select':
                try:
                    expense_head = ExpenseHead.objects.get(expense_head=head_name)
                except Exception as ex:
                    expense_head = None
            
            if expense_head:
                expenses = Expense.objects.filter(date__gte=start_date, date__lte=end_date, expense_head=expense_head).order_by('date')
            else:
                expenses = Expense.objects.filter(date__gte=start_date, date__lte=end_date).order_by('date')
            if len(expenses) > 0: 
                for expense in expenses:
                    p.setFontSize(12)
                    p.drawString(50, y1, expense.date.strftime('%d/%m/%Y'))
                    p.drawString(150, y1, str(expense.voucher_no))
                    data=[[Paragraph(expense.expense_head.expense_head, para_style)]]

                    table = Table(data, colWidths=[150], rowHeights=100, style=style)      
                    table.wrapOn(p, 200, 400)
                    table.drawOn(p, 250, y1)
                    # p.drawString(250, y1, expense.expense_head.expense_head[:38] if len(expense.expense_head.expense_head) > 40 else expense.expense_head.expense_head)
                    data=[[Paragraph(expense.narration, para_style)]]

                    table = Table(data, colWidths=[150], rowHeights=100, style=style)      
                    table.wrapOn(p, 200, 400)
                    table.drawOn(p, 500, y1-10)
                    # p.drawString(500, y1, expense.narration)
                    p.drawString(650, y1, str(expense.amount))
                    y1 = y1 - 30
                    if y1 <= 135:
                        y1 = y - 110
                        p.showPage()
                        p = header(p,y)
                    total_amount = total_amount + expense.amount
            

            p.drawString(50, y1, '')
            p.drawString(150, y1, '')
            p.drawString(550, y1, 'Total: ')
            p.drawString(650, y1, str(total_amount))

            p.showPage()
            p.save()
        return response
class VendorAccountsReport(View):
    def get(self, request, *args, **kwargs):

        status_code = 200
        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1000, 1250))
        y = 1150
        report_type = request.GET.get('report_type', '')
        
        if not report_type:
            return render(request, 'reports/vendor_accounts_report.html', {
                'report_type' : 'date',
                })

        if report_type == 'date':             
                                
            start_date = request.GET['start_date']
            end_date = request.GET['end_date']

            if start_date is None:
                return render(request, 'reports/vendor_accounts_report.html', {})
            if not start_date:            
                ctx = {
                    'msg' : 'Please Select Start Date',
                    'start_date' : start_date,
                    'end_date' : end_date,
                    'report_type' : 'date',
                }
                return render(request, 'reports/vendor_accounts_report.html', ctx)
            elif not end_date:
                ctx = {
                    'msg' : 'Please Select End Date',
                    'start_date' : start_date,
                    'end_date' : end_date,
                    'report_type' : 'date',
                }
                return render(request, 'reports/vendor_accounts_report.html', ctx) 
            else:
                heading = 'Date Wise Vendor Report - ' + start_date + ' - '+ end_date
                start_date = datetime.strptime(start_date, '%d/%m/%Y')
                end_date = datetime.strptime(end_date, '%d/%m/%Y')
                p = header(p,y)
                p.setFontSize(16)
                p.drawString(350, y - 70, heading)

                p.setFontSize(14)

                p.drawString(50, y - 100, "Date")
                p.drawString(150, y - 100, "Vendor Name")
                p.drawString(370, y - 100, "Invoice No")
                p.drawString(450, y - 100, "Payment Mode")
                p.drawString(600, y - 100, "Amount Paid")
                p.drawString(700, y - 100, "Balance")
                
                y1 = y - 120
                p.setFontSize(12)

                purchase_accounts = SupplierAccountPaymentDetail.objects.filter(date__gte=start_date, date__lte=end_date).order_by('date')
                if len(purchase_accounts) > 0:
                    for purchase_account in purchase_accounts:
                        y1 = y1 - 30
                        if y1 <= 270:
                            y1 = y - 120
                            p.showPage()
                            p = header(p, y)

                        p.drawString(50, y1, purchase_account.date.strftime('%d/%m/%Y') if purchase_account.date else '')
                        data=[[Paragraph(purchase_account.supplier.name if purchase_account.supplier else '', para_style)]]

                        table = Table(data, colWidths=[50], rowHeights=100, style=style)      
                        table.wrapOn(p, 200, 400)
                        table.drawOn(p, 150, y1-10)
                        # p.drawString(150, y1, purchase_account.supplier.name if purchase_account.supplier else '')
                        p.drawString(400, y1, str(purchase_account.purchase.purchase_invoice_number) if purchase_account.purchase else '')
                        p.drawString(450, y1, purchase_account.payment_mode)

                        p.drawString(600, y1, str(purchase_account.paid))
                        p.drawString(700, y1, str(purchase_account.balance)) 
                p.showPage()
                p.save()
        elif report_type == 'vendor':
            supplier_name = request.GET.get('vendor', '')
            if not supplier_name or supplier_name == 'undefined':            
                ctx = {
                    'msg' : 'Please Select Vendor',
                    'report_type' : 'vendor',
                }
                return render(request, 'reports/vendor_accounts_report.html', ctx)
            else:      
                heading = 'Vendor Wise Vendor Accounts' + ' - ' + supplier_name
                p.setFontSize(16)
                p.drawString(270, y - 70, heading)
                p.setFontSize(14)
                p.drawString(50, y - 100, 'Date')
                p.drawString(150, y - 100, 'Supplier Name')
                p.drawString(350, y - 100, 'Invoice No')
                p.drawString(490, y - 100, 'Total Amount')
                p.drawString(610, y - 100, 'Payment Mode')
                p.drawString(740, y - 100, 'Amount Paid')
                p.drawString(860, y - 100, 'Balance')        
                p = header(p,y)
                p.setFontSize(12)
                y1 = y - 120
                supplier = Supplier.objects.get(name=supplier_name)
                purchase_accounts = SupplierAccountPaymentDetail.objects.filter(supplier=supplier).order_by('-id')[:10]
                if len(purchase_accounts) > 0:
                    for purchase_account in purchase_accounts:
                        y1 = y1 - 30
                        if y1 <= 270:
                            y1 = 850
                            p.showPage()
                            p = header(p,y)
                        p.drawString(50, y1, purchase_account.date.strftime('%d/%m/%Y') if purchase_account.date else '')
                        p.drawString(150, y1, purchase_account.supplier.name if purchase_account.supplier else '')
                        p.drawString(350, y1, str(purchase_account.purchase.purchase_invoice_number) if purchase_account.purchase else '')
                        p.drawString(490, y1, str(purchase_account.total_amount))
                        p.drawString(610, y1, purchase_account.payment_mode)
                        p.drawString(740, y1, str(purchase_account.paid))
                        p.drawString(860, y1, str(purchase_account.balance)) 
                    y1 = y1 - 50
                    if y1 <= 270:
                        y1 = 850
                        p.showPage()
                        p = header(p,y)
                p.showPage()
                p.save()
            
        return response 

class PendingCustomerReport(View):
    
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1000, 1250))
        y = 1150
        status_code = 200
        customer_name = request.GET.get('customer_name')
        report_type = request.GET.get('report_type', '')
        if not report_type:
            return render(request, 'reports/pending_customer_report.html', {
                    'report_type' : 'pending_customer',
                })
        else:
            if not customer_name:
                context = {
                        'message': 'Please enter a customer',
                        'report_type' : 'pending_customer',
                    }
                return render(request, 'reports/pending_customer_report.html', context)
            else:
                if customer_name == 'all' or customer_name == 'All':
                    customers = Customer.objects.all()   
                else:
                    try:
                        customer = Customer.objects.get(customer_name=customer_name)
                        customer_accounts = CustomerAccount.objects.filter(customer=customer, is_complted=False)
                    except:
                        context = {
                            'report_type' : 'pending_customer',
                            'message': 'No such customers',
                        }
                        return render(request, 'reports/pending_customer_report.html', context)
            p = header(p,y)
            p.setFontSize(16)
            p.drawString(400, y - 70, 'Pending Customer Report - ' + customer_name)
            total_balance = 0
            p.setFontSize(14)
            p.drawString(50,y - 100,'Date')
            p.drawString(140, y - 100, 'Customer Name')
            p.drawString(320, y - 100, 'Invoice No')
            p.drawString(420, y - 100, 'Total Amount')
            p.drawString(550, y - 100, 'Paid') 
            p.drawString(650, y - 100, 'Balance') 
            
            y1 = y - 120 
            if customer_name == 'all' or customer_name == 'All':
                if len(customers) > 0:
                    for customer in customers:
                        customer_accounts = CustomerAccount.objects.filter(customer=customer, is_complted=False)
                        for customer_account in customer_accounts:
                                p.drawString(50, y1, customer_account.invoice_no.sales_invoice_date.strftime('%d/%m/%Y') if customer_account.invoice_no.sales_invoice_date else '')
                                p.drawString(140, y1, customer_account.customer.customer_name)
                                
                                p.drawString(320, y1, customer_account.invoice_no.sales_invoice_number)
                                p.drawString(420, y1, str(customer_account.total_amount))
                                p.drawString(550, y1, str(customer_account.paid))
                                p.drawString(650, y1, str(customer_account.balance))
                                y1 = y1 - 30
                                if y1 <= 270:
                                    y1 = y - 120
                                    p.showPage()
                                    p = header(p,y)
                                total_balance = total_balance + customer_account.balance

                p.drawString(50, y1, '')
                p.drawString(150, y1, '')
                p.drawString(650, y1, 'Total Balance: ')
                p.drawString(750, y1, str(total_balance))
            else:
                
                if len(customer_accounts) > 0:
                    for customer_account in customer_accounts:
                        p.drawString(50, y1, customer_account.invoice_no.sales_invoice_date.strftime('%d/%m/%Y') if customer_account.invoice_no.sales_invoice_date else '')
                        p.drawString(140, y1, customer_account.customer.customer_name)
                        
                        p.drawString(320, y1, customer_account.invoice_no.sales_invoice_number)
                        p.drawString(420, y1, str(customer_account.total_amount))
                        p.drawString(550, y1, str(customer_account.paid))
                        p.drawString(650, y1, str(customer_account.balance))
                        y1 = y1 - 30
                        if y1 <= 270:
                            y1 = y - 120
                            p.showPage()
                            p = header(p,y)
            p.showPage()
            p.save()
            return response

class CustomerPaymentReport(View):
    def get(self, request, *args, **kwargs):

        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1000, 1250))
        y = 1150
        status_code = 200
        customer_name = request.GET.get('customer_name')
        report_type = request.GET.get('report_type', '')
        
        if not report_type:
            return render(request, 'reports/customer_payment_report.html', {
                    'report_type' : 'customer_payment',
                })
        else:
            if not customer_name:
                context = {
                    'message': 'Please enter a customer',
                    'report_type' : 'customer_payment',
                }

                return render(request, 'reports/customer_payment_report.html', context)
            else:
                if customer_name:
                    if customer_name == 'all' or customer_name == 'All':
                        customers = Customer.objects.all()
                    else:
                        try:
                            customer = Customer.objects.get(customer_name=customer_name)
                            customer_payments = CustomerPayment.objects.filter(customer=customer)
                            
                        except Exception as ex:
                            context = {
                                'message': 'No such customers',
                                'report_type' : 'customer_payment',
                            }
                            return render(request, 'reports/customer_payment_report.html', context)
            p = header(p,y)
            p.setFontSize(16)

            p.drawString(400, y - 70, ' Customer Report - ' + customer_name)
            p.setFontSize(14)
            p.drawString(150, y - 100, 'Date')
            p.drawString(250, y - 100, 'Customer Name')
            p.drawString(400, y - 100, 'Invoice No')
            p.drawString(490, y - 100, 'Total Amount')
            p.drawString(610, y - 100, 'Payment Mode')
            p.drawString(740, y - 100, 'Amount Paid')
            p.drawString(860, y - 100, 'Balance') 
            p.setFontSize(12)
            y1 = y - 120 
            if customer_name == 'all' or customer_name == 'All':
                if len(customers) > 0:
                    for customer in customers:
                        customer_payments = CustomerPayment.objects.filter(customer=customer)
                        for customer_payment in customer_payments:
                                p.drawString(150, y1, customer_payment.date.strftime('%d/%m/%Y') if customer_payment.date else '')
                                p.drawString(250, y1, customer_payment.customer.customer_name)
                                p.drawString(400, y1, customer_payment.customer_account.sales_invoice_number)
                                p.drawString(500, y1, str(customer_payment.total_amount))
                                p.drawString(610, y1, str(customer_payment.payment_mode))
                                if customer_payment.payment_mode == 'Cash(sales)' or customer_payment.payment_mode == 'Cheque(sales)':
                                    p.drawString(740, y1, str(customer_payment.paid))
                                else:
                                    p.drawString(740, y1, str(customer_payment.amount))
                                p.drawString(860, y1, str(customer_payment.balance))
                                y1 = y1 - 30
                                if y1 <= 270:
                                    y1 = y - 120
                                    p.showPage()
                                    p = header(p,y)
            else:
                if len(customer_payments) > 0:
                    for customer_payment in customer_payments:
                        customer_payments = CustomerPayment.objects.filter(customer=customer)
                        p.drawString(150, y1, customer_payment.date.strftime('%d/%m/%Y') if customer_payment.date else '')
                        p.drawString(250, y1, customer_payment.customer.customer_name)
                        p.drawString(400, y1, customer_payment.customer_account.sales_invoice_number)
                        p.drawString(500, y1, str(customer_payment.total_amount))
                        p.drawString(610, y1, str(customer_payment.payment_mode))
                        if customer_payment.payment_mode == 'Cash(sales)' or customer_payment.payment_mode == 'Cheque(sales)':
                            p.drawString(740, y1, str(customer_payment.paid))
                        else:
                            p.drawString(740, y1, str(customer_payment.amount))
                        p.drawString(860, y1, str(customer_payment.balance))
                        y1 = y1 - 30
                        if y1 <= 270:
                            y1 = y - 120
                            p.showPage()
                            p = header(p,y)
            p.showPage()
            p.save()
            return response

class PurchaseReport(View):

    def get(self, request, *args, **kwargs):    

        status_code = 200
        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1000, 1250))
        y = 1150
        p.setFontSize(15)
        p = header(p, y)

        report_type = request.GET.get('report_type', '')

        if not report_type:
            return render(request, 'reports/purchase_reports.html', {
                'report_type' : 'date',
                })

        if report_type == 'date': 

            start = request.GET['start_date']
            end = request.GET['end_date']
           
            if not start:            
                ctx = {
                    'msg' : 'Please Select Start Date',
                    'start_date' : start,
                    'end_date' : end,
                    'report_type' : 'date',
                }
                return render(request, 'reports/purchase_reports.html', ctx)
            elif not end:
                ctx = {
                    'msg' : 'Please Select End Date',
                    'start_date' : start,
                    'end_date' : end,
                    'report_type' : 'date',
                }
                return render(request, 'reports/purchase_reports.html', ctx)                  
            else:
                total = 0
                total_discount = 0
                total_discount_after_return = 0
                grant_total = 0
                p.setFont('Helvetica', 20)
                report_heading = 'Date Wise Purchase Report' + ' - '+ start + ' - ' + end
                start_date = datetime.strptime(start, '%d/%m/%Y')
                end_date = datetime.strptime(end, '%d/%m/%Y')
                p.drawString(270, y - 70, report_heading)
                p.setFontSize(15)
                p.drawString(50, y - 100, "Date")
                p.drawString(110, y - 100, "Invoice Number")
                p.drawString(240, y - 100, "Supplier")
                p.drawString(500, y - 100, "Net Total")
                p.drawString(670, y - 100, "Discount")
                p.drawString(580, y - 100, "Grant Total")

                purchases = Purchase.objects.filter(purchase_invoice_date__gte=start_date, purchase_invoice_date__lte=end_date, is_returned=False).order_by('purchase_invoice_date')
                y1 = y - 110
                for purchase in purchases:
                    y1 = y1 - 30
                    if y1 <= 135:
                        y1 = y - 110
                        p.showPage()
                        p = header(p, y)
                    
                    total = float(total) + float(purchase.net_total)
                    grant_total = float(grant_total) + float(purchase.grant_total)
                    total_discount = float(total_discount) + float(purchase.discount)
                    p.drawString(50, y1, purchase.purchase_invoice_date.strftime('%d/%m/%y'))
                    p.drawString(120, y1, str(purchase.purchase_invoice_number))

                    p.drawString(240, y1, purchase.supplier.name if purchase and purchase.supplier else '')
                    p.drawString(500, y1, str(purchase.net_total))
                    p.drawString(670, y1, str(purchase.discount))
                    p.drawString(580, y1, str(purchase.grant_total))
                        
                if y1 <= 135:
                    y1 = y - 110
                    p.showPage()
                    p = header(p, y)
                p.drawString(50, y1 - 60, 'Total Discount:')
                p.drawString(150, y1 - 60, str(total_discount))
                p.drawString(50, y1 - 80, 'Total Amount:')
                p.drawString(150, y1 - 80, str(total))
                p.drawString(50, y1 - 100, 'Grant Total:')
                p.drawString(150, y1 - 100, str(grant_total))
                p.showPage()
                p.save()
                return response

class PurchaseReturnReport(View):

    def get(self, request, *args, **kwargs):    

        status_code = 200
        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1000, 1250))
        y = 1150
        p.setFontSize(15)
        p = header(p, y)

        report_type = request.GET.get('report_type', '')

        if not report_type:
            return render(request, 'reports/purchase_return_report.html', {
                'report_type' : 'date',
                })

        if report_type == 'date': 

            start = request.GET['start_date']
            end = request.GET['end_date']
           
            if not start:            
                ctx = {
                    'msg' : 'Please Select Start Date',
                    'start_date' : start,
                    'end_date' : end,
                    'report_type' : 'date',
                }
                return render(request, 'reports/purchase_return_report.html', ctx)
            elif not end:
                ctx = {
                    'msg' : 'Please Select End Date',
                    'start_date' : start,
                    'end_date' : end,
                    'report_type' : 'date',
                }
                return render(request, 'reports/purchase_return_report.html', ctx)                  
            else:
                total = 0
                p.setFont('Helvetica', 20)
                report_heading = 'Date Wise Purchase Return Report' + ' - '+ start + ' - ' + end
                start_date = datetime.strptime(start, '%d/%m/%Y')
                end_date = datetime.strptime(end, '%d/%m/%Y')
                p.drawString(270, y - 70, report_heading)
                p.setFontSize(13)
                p.drawString(50, y - 100, "Date")
                p.drawString(110, y - 100, "Invoice Number")
                p.drawString(240, y - 100, "Purchase Invoice")
                p.drawString(360, y - 100, "Supplier")
                p.drawString(500, y - 100, "Net Total")
                
                purchase_returns = PurchaseReturn.objects.filter(date__gte=start_date, date__lte=end_date).order_by('date')
                y1 = y - 110
                for purchase in purchase_returns:
                    y1 = y1 - 30
                    if y1 <= 135:
                        y1 = y - 110
                        p.showPage()
                        p = header(p, y)
                    
                    total = float(total) + float(purchase.net_amount)
                    p.drawString(50, y1, purchase.date.strftime('%d/%m/%y'))
                    p.drawString(120, y1, str(purchase.return_invoice_number))

                    p.drawString(240, y1, str(purchase.purchase.purchase_invoice_number))
                    p.drawString(360, y1, purchase.purchase.supplier.name)
                    p.drawString(500, y1, str(purchase.net_amount))
                        
                if y1 <= 135:
                    y1 = y - 110
                    p.showPage()
                    p = header(p, y)
                p.drawString(50, y1 - 80, 'Total Amount:')
                p.drawString(150, y1 - 80, str(total))
                p.showPage()
                p.save()
                return response

class SalesReturnReport(View):

    def get(self, request, *args, **kwargs):    

        status_code = 200
        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1000, 1250))
        y = 1150
        p.setFontSize(15)
        p = header(p, y)

        report_type = request.GET.get('report_type', '')

        if not report_type:
            return render(request, 'reports/sales_return_reports.html', {
                'report_type' : 'date',
                })

        if report_type == 'date': 

            start = request.GET['start_date']
            end = request.GET['end_date']
           
            if not start:            
                ctx = {
                    'msg' : 'Please Select Start Date',
                    'start_date' : start,
                    'end_date' : end,
                    'report_type' : 'date',
                }
                return render(request, 'reports/sales_return_reports.html', ctx)
            elif not end:
                ctx = {
                    'msg' : 'Please Select End Date',
                    'start_date' : start,
                    'end_date' : end,
                    'report_type' : 'date',
                }
                return render(request, 'reports/sales_return_reports.html', ctx)                  
            else:
                total = 0
                p.setFont('Helvetica', 20)
                report_heading = 'Date Wise Sales Return Report' + ' - '+ start + ' - ' + end
                start_date = datetime.strptime(start, '%d/%m/%Y')
                end_date = datetime.strptime(end, '%d/%m/%Y')
                p.drawString(270, y - 70, report_heading)
                p.setFontSize(13)
                p.drawString(50, y - 100, "Date")
                p.drawString(110, y - 100, "Invoice Number")
                p.drawString(210, y - 100, "Sales Invoice")
                p.drawString(350, y - 100, "Customer")
                p.drawString(500, y - 100, "Net Total")

                sales_returns = SalesReturn.objects.filter(date__gte=start_date,date__lte=end_date).order_by('date')
                y1 = y - 110
                for return_sale in sales_returns:
                    y1 = y1 - 30
                    if y1 <= 135:
                        y1 = y - 110
                        p.showPage()
                        p = header(p, y)
                            
                    total = float(total) + float(return_sale.net_amount)
                    
                    p.drawString(50, y1, return_sale.date.strftime('%d/%m/%y'))
                    p.drawString(120, y1, str(return_sale.return_invoice_number))

                    p.drawString(220, y1, return_sale.sales.sales_invoice_number)
                    p.drawString(350, y1, str(return_sale.sales.customer.customer_name))
                    p.drawString(500, y1, str(return_sale.net_amount))
                if y1 <= 135:
                    y1 = y - 110
                    p.showPage()
                    p = header(p, y)
                p.drawString(50, y1 - 80, 'Total Amount:')
                p.drawString(150, y1 - 80, str(total))
                p.showPage()
                p.save()
                return response


