# -*- coding: utf-8 -*- 

from datetime import datetime

from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.colors import green, black, red, gray
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from smartbook_new import arabic_reshaper

from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.models import User
from django.http import HttpResponse

from sales.models import Sales
from expenses.models import Expense, ExpenseHead
from purchase.models import SupplierAccount, SupplierAccountDetail
from web.models import OwnerCompany

def header(canvas, y):
    try:
        owner_company = OwnerCompany.objects.latest('id')
    except:
        owner_company = None
    canvas.setFont("Helvetica", 30)  
    canvas.setFillColor(black)
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
                round_off = 0
                total_discount = 0
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
                p.drawString(500, y - 100, "Discount")
                p.drawString(600, y - 100, "Roundoff")
                p.drawString(700, y - 100, "Grant Total")

                sales = Sales.objects.filter(sales_invoice_date__gte=start_date,sales_invoice_date__lte=end_date).order_by('sales_invoice_date')
                y1 = y - 110
                for sale in sales:
                    y1 = y1 - 30
                    if y1 <= 135:
                        y1 = y - 110
                        p.showPage()
                        p = header(p, y)
                    p.drawString(50, y1, sale.sales_invoice_date.strftime('%d/%m/%y'))
                    p.drawString(120, y1, str(sale.sales_invoice_number))

                    p.drawString(240, y1, sale.customer.customer_name)
                    p.drawString(400, y1, str(sale.net_amount))
                    p.drawString(500, y1, str(sale.discount_for_sale))
                    p.drawString(600, y1, str(sale.round_off))
                    p.drawString(700, y1, str(sale.grant_total))
                    total = float(total) + float(sale.net_amount)
                    round_off = float(round_off) + float(sale.round_off)
                    total_discount = float(total_discount) + float(sale.discount_for_sale)
                    grant_total = float(grant_total) + float(sale.grant_total)
                                
                if y1 <= 135:
                    y1 = y - 110
                    p.showPage()
                    p = header(p, y)
                p.drawString(50, y1 - 40, 'Round Off : ')
                p.drawString(150, y1 - 40, str(round_off))
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
            head_name = request.GET['expense_head']
            y1 = y - 130
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
                    p.drawString(250, y1, expense.expense_head.expense_head[:38] if len(expense.expense_head.expense_head) > 40 else expense.expense_head.expense_head)
                    p.drawString(500, y1, expense.narration)
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
        p = canvas.Canvas(response, pagesize=(1000, 1100))
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
                start_date = datetime.strptime(start_date, '%d/%m/%Y')
                end_date = datetime.strptime(end_date, '%d/%m/%Y')
                p = header(p,y)

                p.drawString(350, 900, 'Date Wise Vendor Accounts')

                p.setFontSize(13)

                p.drawString(50, 875, "Date")
                p.drawString(150, 875, "Vendor Name")
                p.drawString(250, 875, "Payment Mode")
                p.drawString(350, 875, "Narration")
                p.drawString(470, 875, "Opening Balance")
                p.drawString(580, 875, "Paid Amount")
                p.drawString(650, 875, "Closing Balance") 

                
                y = 850

                purchase_accounts = SupplierAccountDetail.objects.filter(date__gte=start_date, date__lte=end_date).order_by('date')
                if len(purchase_accounts) > 0:
                    for purchase_account in purchase_accounts:

                        y = y - 30
                        if y <= 270:
                            y = 850
                            p.showPage()
                            p = header(p,y)

                        p.drawString(50, y, purchase_account.date.strftime('%d/%m/%Y') if purchase_account.date else '')
                        p.drawString(150, y, purchase_account.supplier_account.supplier.name)
                        p.drawString(250, y, purchase_account.supplier_account.payment_mode)
                        p.drawString(350, y, purchase_account.supplier_account.narration if purchase_account.supplier_account.narration else '')

                        p.drawString(470, y, str(purchase_account.opening_balance))
                        p.drawString(580, y, str(purchase_account.amount))
                        p.drawString(660, y, str(purchase_account.closing_balance)) 
                
                p.showPage()
                p.save()
            
        
                
        elif report_type == 'vendor':

            supplier_name = request.GET['vendor']
            print supplier_name
            if supplier_name == 'select':            
                ctx = {
                    'msg' : 'Please Select Vendor',
                    'report_type' : 'vendor',
                }
                return render(request, 'reports/vendor_accounts_report.html', ctx)
            else:               
                p = header(p,y)

                p.drawString(350, 900, 'Vendor Wise Vendor Accounts')

                p.setFontSize(13)

                p.drawString(50, 875, "Date")
                p.drawString(150, 875, "Payment Mode")
                p.drawString(250, 875, "Narration")
                p.drawString(380, 875, "Opening Balance")
                p.drawString(480, 875, "Paid Amount")
                p.drawString(580, 875, "Closing Balance") 

                y = 850

                vendor = SupplierAccount.objects.get(supplier__name = supplier_name)
                purchase_accounts = SupplierAccountDetail.objects.filter(supplier_account__supplier = vendor)[:10]

                if len(purchase_accounts) > 0:
                    for purchase_account in purchase_accounts:

                        y = y-30
                        if y <= 270:
                            y = 850
                            p.showPage()
                            p = header(p,y)


                        p.drawString(50, y, purchase_account.date.strftime('%d/%m/%Y') if purchase_account.date else '')
                        p.drawString(150, y, purchase_account.supplier_account.payment_mode)
                        p.drawString(250, y, purchase_account.supplier_account.narration if purchase_account.supplier_account.narration else '')
                        p.drawString(380, y, str(purchase_account.opening_balance))
                        p.drawString(480, y, str(purchase_account.amount))
                        p.drawString(580, y, str(purchase_account.closing_balance))
                    y = y - 50
                    if y <= 270:
                        y = 850
                        p.showPage()
                        p = header(p,y)
                    p.drawString(470, y, 'Current Balance:')
                    p.drawString(580, y, str(purchase_account.supplier_account.balance)) 
                p.showPage()
                p.save()
            
        return response 

