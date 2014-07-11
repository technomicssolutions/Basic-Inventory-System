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

from sales.models import *
from expenses.models import *
from purchase.models import *


class PurchaseReport(View):

    def get(self, request, *args, **kwargs):        
        
        status_code = 200
        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1000, 1000))
        p.setFontSize(15)
        report_type = request.GET.get('report_type', '')
        if not report_type:
            return render(request, 'reports/purchase_reports.html',{
                'report_type' : 'project_based',
                })

        project_name = request.GET['project_name']
        print project_name
        
        if project_name == 'select':
            return render(request, 'reports/purchase_reports.html',{
                'msg': 'Please Select Project',
                'report_type' : 'project_based',
                
            })

        project = Project.objects.get(id = project_name)
        purchases = Purchase.objects.filter(project = project)
        heading = 'Purchase Report' + ' - ' + project.name
        p.drawCentredString(400, 900, heading)
        p.setFontSize(13)
        p.drawString(50, 875, "Date")
        p.drawString(150, 875, "Invoice No")
        p.drawString(250, 875, "Supplier")
        p.drawString(390, 875, "Discount")
        p.drawString(490, 875, "Amount")
        p.drawString(590, 875, "Purchase Expense")
        p.setFontSize(12)  
        y = 850
        total_amount = 0
        total_discount = 0
        total_purchase_expense = 0
        for purchase in purchases:
                        
            y = y - 30
            if y <= 270:
                y = 850
                p.showPage()
            p.drawString(50, y, purchase.purchase_invoice_date.strftime('%d/%m/%y'))
            p.drawString(160, y, str(purchase.purchase_invoice_number))
            p.drawString(260, y, str(purchase.supplier.name))
            p.drawString(390, y, str(purchase.discount))
            p.drawString(490, y, str(purchase.grant_total))
            p.drawString(590, y, str(purchase.purchase_expense))

            total_amount = total_amount + purchase.grant_total
            total_discount = total_discount + purchase.discount
            total_purchase_expense = total_purchase_expense + purchase.purchase_expense
        y = y - 50
        if y <= 270:
            y = 850
            p.showPage()
        p.drawString(450, y, 'Total:')
        p.drawString(490, y, str(total_amount))    
        p.drawString(350, y, 'Total:')
        p.drawString(390, y, str(total_discount))    
        p.drawString(550, y, 'Total:')
        p.drawString(590, y, str(total_purchase_expense))    
        p.showPage()
        p.save()
                  
        return response      

class SalesReport(View):

    def get(self, request, *args, **kwargs):

        status_code = 200
        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1000, 1250))
        y = 1150
        p = header(p, y)
        p = footer(p, y)
        p.setFontSize(15)
        report_type = request.GET.get('report_type', '')
        total_amount = 0
        total_discount = 0
        total_roundoff = 0
        if not report_type:
            return render(request, 'reports/sales_reports.html',{})

        if report_type == 'select':
            return render(request, 'reports/sales_reports.html',{
                'msg' : 'Please Choose Report Type',
                })

        
        if report_type == 'project_based':
            project_name = request.GET['project_name']
            if project_name == 'select':
                return render(request, 'reports/sales_reports.html',{
                    'msg': 'Please Select Project',
                    'report_type' : 'project_based',
                    
                })


            project = Project.objects.get(id = project_name)
            sales = Sales.objects.filter(project = project).order_by('id')
            heading = 'Sales Report' + ' - ' + project.name
            p.drawCentredString(400, y - 70, heading)
            p.setFontSize(13)
            p.drawString(50, y - 100, "Date")
            p.drawString(150, y - 100, "Invoice No")
            p.drawString(250, y - 100, "Customer")
            p.drawString(390, y - 100, "Total")
            p.drawString(490, y - 100, "Discount")
            p.drawString(590, y - 100, "Roundoff")
            p.drawString(690, y - 100, "Grant Total")
            p.setFontSize(12)  
            y1 = y - 110
            
            for sale in sales:
                            
                y1 = y1 - 30
                if y1 <= 135:
                    y1 = y - 110
                    p.showPage()
                    p = header(p, y)
                    p = footer(p, y)
                p.drawString(50, y1, sale.sales_invoice_date.strftime('%d/%m/%y'))
                p.drawString(160, y1, str(sale.sales_invoice_number))
                p.drawString(250, y1, str(sale.customer.customer_name))
                p.drawString(390, y1, str(sale.net_amount))
                p.drawString(490, y1, str(sale.discount_for_sale))
                p.drawString(590, y1, str(sale.round_off))
                p.drawString(690, y1, str(sale.grant_total))

                total_amount = total_amount + sale.net_amount
                total_discount = total_discount + sale.discount_for_sale
                total_roundoff = total_roundoff + sale.round_off
            y1 = y1 - 50
            if y1 <= 135:
                y1 = y - 110
                p.showPage()
                p = header(p, y)
                p = footer(p, y)
            grant_total = total_amount - (total_discount + total_roundoff)
            p.drawString(600, y1, 'Total Amount :')
            p.drawString(690, y1, str(total_amount))    
            p.drawString(600, y1 - 30, 'Total Discount :')
            p.drawString(690, y1 - 30, str(total_discount))    
            p.drawString(600, y1 - 60, 'Total Roundoff :')
            p.drawString(690, y1 - 60, str(total_roundoff)) 
            p.drawString(600, y1 - 90, 'Grant Total :')
            p.drawString(690, y1 - 90, str(grant_total))
            p.showPage()
            p.save()
        elif report_type == 'date_based':
            start = request.GET['start_date']
            end = request.GET['end_date']
            heading = 'Date Wise Sales Report' + ' - ' + start + ' - ' + end
            p.drawCentredString(400, y - 70, heading)
            p.setFontSize(13)
            p.drawString(50, y - 100, "Date")
            p.drawString(150, y - 100, "Invoice No")
            p.drawString(250, y - 100, "Customer")
            p.drawString(390, y - 100, "Total")
            p.drawString(490, y - 100, "Discount")
            p.drawString(590, y - 100, "Roundoff")
            p.drawString(690, y - 100, "Grant Total")
            p.setFontSize(12)  
           
            if not start:            
                ctx = {
                    'msg' : 'Please Select Start Date',
                    'start_date' : start,
                    'end_date' : end,
                    'report_type' : 'date_based',
                }
                return render(request, 'reports/sales_reports.html', ctx)
            elif not end:
                ctx = {
                    'msg' : 'Please Select End Date',
                    'start_date' : start,
                    'end_date' : end,
                    'report_type' : 'date_based',
                }
                return render(request, 'reports/sales_reports.html', ctx)                  
            else:
                start_date = datetime.strptime(start, '%d/%m/%Y')
                end_date = datetime.strptime(end, '%d/%m/%Y')
                projects = Project.objects.filter(start_date__gte=start_date, expected_end_date__lte=end_date).order_by('id')
                y1 = y - 120
                for project in projects:
                    project_name = 'Project Name - ' + project.name
                    p.drawCentredString(400, y1 , project_name)
                    y1 = y1 - 40
                    sales = Sales.objects.filter(project=project).order_by('id')
                    for sale in sales:

                        p.drawString(50, y1, sale.sales_invoice_date.strftime('%d/%m/%y'))
                        p.drawString(160, y1, str(sale.sales_invoice_number))
                        p.drawString(260, y1, str(sale.customer.customer_name))
                        p.drawString(390, y1, str(sale.net_amount))
                        p.drawString(490, y1, str(sale.discount_for_sale))
                        p.drawString(590, y1, str(sale.round_off))
                        p.drawString(690, y1, str(sale.grant_total))
                        y1 = y1 - 30
                        if y1 <= 135:
                            y1 = y - 110
                            p.showPage()
                            p = header(p, y)
                            p = footer(p, y)
                        if y1 <= 135:
                            y1 = y - 110
                            p.showPage()
                            p = header(p, y)
                            p = footer(p, y)
                p.save()

                  
        return response

class CashReport(View):

    def get(self, request, *args, **kwargs):

        status_code = 200
        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1000, 1000))
        p.setFontSize(15)
        report_type = request.GET.get('report_type', '')
        total_amount = 0
        total_discount = 0
        total_roundoff = 0
        if not report_type:
            return render(request, 'reports/cash_report.html',{
                'report_type' : 'project_based',
                })
        
        project_name = request.GET['project_name']
        
        if project_name == 'select':
            return render(request, 'reports/cash_report.html',{
                'msg': 'Please Select Project',
                'report_type' : 'project_based',
                
            })

        project = Project.objects.get(id = project_name)
        sales = Sales.objects.filter(project = project, payment_mode='cash')
        heading = 'Cash Report' + ' - ' + project.name
        p.drawCentredString(400, 900, heading)
        p.setFontSize(13)
        p.drawString(50, 875, "Date")
        p.drawString(150, 875, "Invoice No")
        p.drawString(250, 875, "Customer")
        p.drawString(390, 875, "Item")
        p.drawString(490, 875, "Selling Price")
        p.drawString(590, 875, "Quantity")
        p.drawString(690, 875, "Amount")
        p.setFontSize(12)  
        y = 850
        
        for sale in sales:
                        
            y = y - 30
            if y <= 270:
                y = 850
                p.showPage()
            for s_item in sale.salesitem_set.all():
                p.drawString(50, y, sale.sales_invoice_date.strftime('%d/%m/%y'))
                p.drawString(160, y, str(sale.sales_invoice_number))
                p.drawString(260, y, str(sale.customer.customer_name))
                p.drawString(390, y, str(s_item.item.name))
                p.drawString(490, y, str(s_item.selling_price))
                p.drawString(590, y, str(s_item.quantity_sold))
                p.drawString(690, y, str(s_item.net_amount))
                y = y - 30
                if y <= 270:
                    y = 850
                    p.showPage()

            total_amount = total_amount + sale.net_amount
            total_discount = total_discount + sale.discount_for_sale
            total_roundoff = total_roundoff + sale.round_off
        y = y - 50
        if y <= 270:
            y = 850
            p.showPage()
        grant_total = total_amount - (total_discount + total_roundoff)
        p.drawString(600, y, 'Total Amount :')
        p.drawString(690, y, str(total_amount))    
        p.drawString(600, y - 30, 'Total Discount :')
        p.drawString(690, y - 30, str(total_discount))    
        p.drawString(600, y - 60, 'Total Roundoff :')
        p.drawString(690, y - 60, str(total_roundoff)) 
        p.drawString(600, y - 90, 'Grant Total :')
        p.drawString(690, y - 90, str(grant_total))
        p.showPage()
        p.save()
        return response

class BankIncomeReport(View):

    def get(self, request, *args, **kwargs):

        status_code = 200
        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1000, 1000))
        p.setFontSize(15)
        report_type = request.GET.get('report_type', '')
        total_amount = 0
        total_discount = 0
        total_roundoff = 0
        print report_type
        if not report_type:
            return render(request, 'reports/bank_income_report.html',{
                'report_type' : 'project_based',
                })
        
        project_name = request.GET['project_name']
        
        if project_name == 'select':
            return render(request, 'reports/bank_income_report.html',{
                'msg': 'Please Select Project',
                'report_type' : 'project_based',
                
            })

        project = Project.objects.get(id = project_name)
        sales = Sales.objects.filter(project = project, payment_mode='cheque')
        heading = 'Bank Income Report' + ' - ' + project.name
        p.drawCentredString(400, 900, heading)
        p.setFontSize(13)
        p.drawString(50, 875, "Date")
        p.drawString(150, 875, "Invoice No")
        p.drawString(250, 875, "Customer")
        p.drawString(390, 875, "Item")
        p.drawString(490, 875, "Selling Price")
        p.drawString(590, 875, "Quantity")
        p.drawString(690, 875, "Amount")
        p.setFontSize(12)  
        y = 850
        
        for sale in sales:
                        
            y = y - 30
            if y <= 270:
                y = 850
                p.showPage()
            for s_item in sale.salesitem_set.all():
                p.drawString(50, y, sale.sales_invoice_date.strftime('%d/%m/%y'))
                p.drawString(160, y, str(sale.sales_invoice_number))
                p.drawString(260, y, str(sale.customer.customer_name))
                p.drawString(390, y, str(s_item.item.name))
                p.drawString(490, y, str(s_item.selling_price))
                p.drawString(590, y, str(s_item.quantity_sold))
                p.drawString(690, y, str(s_item.net_amount))
                y = y - 30
                if y <= 270:
                    y = 850
                    p.showPage()

            total_amount = total_amount + sale.net_amount
            total_discount = total_discount + sale.discount_for_sale
            total_roundoff = total_roundoff + sale.round_off
        y = y - 50
        if y <= 270:
            y = 850
            p.showPage()
        grant_total = total_amount - (total_discount + total_roundoff)
        p.drawString(600, y, 'Total Amount :')
        p.drawString(690, y, str(total_amount))    
        p.drawString(600, y - 30, 'Total Discount :')
        p.drawString(690, y - 30, str(total_discount))    
        p.drawString(600, y - 60, 'Total Roundoff :')
        p.drawString(690, y - 60, str(total_roundoff)) 
        p.drawString(600, y - 90, 'Grant Total :')
        p.drawString(690, y - 90, str(grant_total))
        p.showPage()
        p.save()
        return response

class ProjectReport(View):

    def get(self, request, *args, **kwargs):

        status_code = 200
        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1000, 1000))
        p.setFontSize(15)
        report_type = request.GET.get('report_type', '')
        total_amount = 0
        total_discount = 0
        total_roundoff = 0
        if not report_type:
            return render(request, 'reports/project_report.html',{
                'report_type' : 'project_based',
                })
        
        project_name = request.GET['project_name']
        
        if project_name == 'select':
            return render(request, 'reports/project_report.html',{
                'msg': 'Please Select Project',
                'report_type' : 'project_based',
                
            })
        if project_name == 'all':
            projects = Project.objects.all()
            project_name = 'All'
        else:
            projects = Project.objects.filter(id=project_name)
            project_name = projects[0].name
        heading = 'Project Report / Profit Report' + ' - ' + project_name
        p.drawCentredString(400, 900, heading)
        p.setFontSize(13)
        p.drawString(50, 875, "Start Date")
        p.drawString(150, 875, "End Date")
        p.drawString(250, 875, "Name")
        p.drawString(390, 875, "Budjet")
        p.drawString(490, 875, "Purchase Amount")
        p.drawString(590, 875, "Expense Amount")
        p.drawString(690, 875, "Sales Amount")
        p.drawString(790, 875, "Profit")
        p.setFontSize(12)  
        y = 850
        
        for project in projects.order_by('id'):
            y = y - 30
            if y <= 270:
                y = 850
                p.showPage()
            p.drawString(50, y, project.start_date.strftime('%d/%m/%y'))
            p.drawString(160, y, str(project.expected_end_date.strftime('%d/%m/%Y')))
            p.drawString(260, y, str(project.name))
            p.drawString(390, y, str(project.budget_amount))
            p.drawString(490, y, str(project.purchase_amount))
            p.drawString(590, y, str(project.expense_amount))
            p.drawString(690, y, str(project.sales_amount))
            p.drawString(790, y, str(project.sales_amount - (project.purchase_amount + project.expense_amount)))
            
        
        p.showPage()
        p.save()
        return response

class CashFlows(View):

    def get(self, request, *args, **kwargs):

        status_code = 200
        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1000, 1250))
        y = 1150
        p = header(p, y)
        p = footer(p, y)
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        if start_date is None:
            return render(request, 'reports/cash_flow_report.html', {})
        if not start_date:            
            ctx = {
                'msg' : 'Please Select Start Date ',
                'start_date' : start_date,
                'end_date' : end_date,
            }
            return render(request, 'reports/cash_flow_report.html', ctx)
        elif not end_date:
            ctx = {
                'msg' : 'Please Select End Date',
                'start_date' : start_date,
                'end_date' : end_date,
            }
            return render(request, 'reports/cash_flow_report.html', ctx)

        else:
            start = request.GET['start_date']
            end = request.GET['end_date']                    
            start_date = datetime.strptime(start, '%d/%m/%Y')
            end_date = datetime.strptime(end, '%d/%m/%Y')

            p.drawString(370, y - 70, 'Cash Flows')

            p.drawString(50, y - 100, "Date")
            p.drawString(150, y - 100, "Particulars/Narration")
            p.drawString(550, y - 100, "Income")
            p.drawString(650, y - 100, "Expense")           

            y1 = y - 110
            
            round_off = 0
            discount = 0
            total_income = 0
            total_expense = 0
            
            sales = Sales.objects.filter(sales_invoice_date__gte=start_date,sales_invoice_date__lte=end_date).order_by('sales_invoice_date')
            if sales.count()>0:
                for sale in sales:
                    y1 = y1 - 30
                    if y1 <= 135:
                        y1 = y - 110
                        p.showPage()
                        p = header(p, y)
                        p = footer(p, y)
                    p.drawString(50, y1, (sale.sales_invoice_date).strftime('%d-%m-%Y'))
                    p.drawString(150, y1, 'By Sales '+str(sale.sales_invoice_number))
                    p.drawString(550, y1, str(sale.grant_total))
                    p.drawString(650, y1, '') 

                    round_off = round_off+sale.round_off
                    discount = discount+sale.discount_for_sale
                    total_income = total_income + sale.grant_total
            purchases = Purchase.objects.filter(purchase_invoice_date__gte=start_date,purchase_invoice_date__lte=end_date)
            if purchases.count()>0:
                for purchase in purchases:
                    y1 = y1 - 30
                    if y1 <= 135:
                        y1 = y - 110
                        p.showPage()
                        p = header(p, y)
                        p = footer(p, y)
                    p.drawString(50, y1, (purchase.purchase_invoice_date).strftime('%d-%m-%Y'))
                    p.drawString(150, y1, 'By Purchase '+str(purchase.purchase_invoice_number))
                    p.drawString(550, y1, '')
                    p.drawString(650, y1, str(purchase.grant_total)) 
                    total_expense = total_expense + purchase.grant_total            
            
            expenses = Expense.objects.filter(date__gte=start_date, date__lte=end_date)
            if expenses.count()>0:
                for expense in expenses:   
                    y1 = y1 - 30
                    if y1 <= 135:
                        y1 = y - 110
                        p.showPage()
                        p = header(p, y)
                        p = footer(p, y)
                    
                    p.drawString(50, y1, (expense.date).strftime('%d-%m-%Y'))
                    p.drawString(150, y1, 'By Voucher '+str(expense.voucher_no)+','+expense.narration)
                    p.drawString(550, y1, '')
                    p.drawString(650, y1, str( expense.amount))    
                    
                    total_expense = total_expense + expense.amount 
            total_expense = total_expense + round_off + discount
            difference = total_income - total_expense

            y1 = y1 - 30
            if y1 <= 135:
                y1 = y - 110
                p.showPage()
                p = header(p, y)
                p = footer(p, y)
            p.drawString(50, y1, '')
            p.drawString(150, y1, 'TotalRoundOff-Sales')
            p.drawString(550, y1, '')
            p.drawString(650, y1, str(round_off))

            y1 = y1 - 30
            if y1 <= 135:
                y1 = y - 110
                p.showPage()
                p = header(p, y)
                p = footer(p, y)
            p.drawString(50, y1, '')
            p.drawString(150, y1, 'TotalDiscount-Sales')
            p.drawString(550, y1, '')
            p.drawString(650, y1, str(discount))            
            
            y1 = y1 - 30
            if y1 <= 135:
                y1 = y - 110
                p.showPage()
                p = header(p, y)
                p = footer(p, y)
            p.drawString(50, y1, '')
            p.drawString(150, y1, 'Total')
            p.drawString(550, y1, str(total_income))
            p.drawString(650, y1, str(total_expense))            

            p.showPage()
            p.save()
        return response

class OutstandingCustomerReport(View):

    def get(self, request, *args, **kwargs):

        status_code = 200
        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1000, 1250))
        y = 1150
        p = header(p, y)
        p = footer(p, y)
        
        p.setFontSize(20)

        p.drawString(400, y - 70, 'Outstanding Customers')
        p.setFontSize(15)
        p.drawString(50,  y - 100, "Invoice No")
        p.drawString(140,  y - 100, "Invoice Date")
        p.drawString(240,  y - 100, "Project Name")
        p.drawString(340,  y - 100, "Customer Name")
        p.drawString(500,  y - 100, "Delivery Note")
        p.drawString(600,  y - 100, "Total Amount")
        p.drawString(700, y - 100, "Paid")
        p.drawString(800, y - 100, "Balance")
        p.setFontSize(13)
        sales = Sales.objects.filter(is_processed=False)
        y1 = y - 140
        if sales.count() > 0:
            for sale in sales:

                p.drawString(50, y1, sale.sales_invoice_number)
                p.drawString(150, y1, sale.sales_invoice_date.strftime('%d/%m/%Y'))
                p.drawString(260, y1, sale.project.name if sale.project else '')
                p.drawString(350, y1, str(sale.customer.customer_name))
                p.drawString(500,  y1, sale.delivery_note.delivery_note_number if sale.delivery_note else '')
                p.drawString(600, y1, str(sale.grant_total))
                p.drawString(700, y1, str(float(sale.grant_total) - float(sale.balance)))
                p.drawString(800, y1, str(sale.balance))
                y1 = y1 - 30

                if y1 <= 135:
                    y1 = y - 110
                    p.showPage()
                    p = header(p, y)
                    p = footer(p, y)


        p.showPage()
        p.save()

        return response

class WholeSalesReport(View):

    def get(self, request, *args, **kwargs):    

        status_code = 200
        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1000, 1250))
        y = 1150
        p.setFontSize(15)

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
                    p.drawString(50, y1, sale.sales_invoice_date.strftime('%d/%m/%y'))
                    p.drawString(120, y1, str(sale.sales_invoice_number))

                    p.drawString(250, y1, sale.customer.customer_name)
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

class PurchaseReports(View):

    def get(self, request, *args, **kwargs):

        status_code = 200
        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1000, 1000))
        p.setFontSize(15)

        round_off = 0
        total = 0
        total_discount = 0
        grant_total = 0

        report_type = request.GET.get('report_type', '')

        if not report_type:
            return render(request, 'reports/whole_purchase_reports.html', {
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
                return render(request, 'reports/whole_purchase_reports.html', ctx)
            elif not end:
                ctx = {
                    'msg' : 'Please Select End Date',
                    'start_date' : start,
                    'end_date' : end,
                    'report_type' : 'date',
                }
                return render(request, 'reports/whole_purchase_reports.html', ctx)                  
            else:
                p.drawCentredString(400, 900, 'Purchase Report Date wise')
                start_date = request.GET['start_date']
                end_date = request.GET['end_date']

                start_date = datetime.strptime(start_date, '%d/%m/%Y')
                end_date = datetime.strptime(end_date, '%d/%m/%Y')
                purchases = Purchase.objects.filter(purchase_invoice_date__gte=start_date, purchase_invoice_date__lte=end_date).order_by('purchase_invoice_date')
                p.setFontSize(13)
                p.drawString(50, 850, "Date")
                p.drawString(120, 850, "Invoice No")
                p.drawString(200, 850, "Supplier Invoice")
                p.drawString(300, 850, "Item code")
                p.drawString(380, 850, "Item name")
                p.drawString(650, 850, "Unit Cost price")
                p.drawString(750, 850, "Quantity")
                p.drawString(850, 850, "Amount")

                y = 820
                p.setFontSize(12)
                total_amount = 0
                discount = 0
                grant_total = 0
                for purchase in purchases:
                    purchase_items = purchase.purchaseitem_set.all()
                    for purchase_item in purchase_items:                    
                        y = y - 30
                        if y <= 270:
                            y = 850
                            p.showPage()
                            p = header(p)
                        p.drawString(50, y, purchase_item.purchase.purchase_invoice_date.strftime('%d/%m/%y'))
                        p.drawString(120, y, str(purchase_item.purchase.purchase_invoice_number))
                        p.drawString(200, y, str(purchase_item.purchase.supplier_invoice_number))
                        p.drawString(300, y, purchase_item.item.code)
                        p.drawString(380, y, purchase_item.item.name)
                        p.drawString(650, y, str(purchase_item.cost_price))
                        p.drawString(750, y, str(purchase_item.quantity_purchased))
                        p.drawString(850, y, str(purchase_item.net_amount))
                        total_amount = total_amount + purchase_item.net_amount
                    discount = float(discount) + float(purchase.discount)
                    grant_total = float(grant_total) + float(purchase.grant_total)
                y = y - 30
                if y <= 270:
                    y = 850
                    p.showPage()
                    p = header(p)
                p.drawString(750, y, 'Total Amount:')
                p.drawString(850, y, str(total_amount))
                p.drawString(750, y - 30, 'Total Discount:')
                p.drawString(850, y - 30, str(discount))
                p.drawString(750, y - 60, 'Grant Total:')
                p.drawString(850, y - 60, str(grant_total))
                p.showPage()
                p.save()

                return response

class ExpenseReport(View):

    def get(self, request, *args, **kwargs):

        status_code = 200
        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1000, 1000))
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
            p.setFontSize(16)
            p.drawCentredString(410, 900, heading)
            p.setFontSize(14)
            p.drawString(50, 870, "Date")
            p.drawString(150, 870, "Voucher No")
            p.drawString(250, 870, "Particulars")
            p.drawString(500, 870, "Narration")
            # p.drawString(650, 870, "Project") 
            p.drawString(650, 870, "Amount") 
            y = 850
            p.setFontSize(12)
            head_name = request.GET['expense_head']
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
                    
                    y = y - 30
                    if y <= 270:
                        y = 850
                        p.showPage()
                        p = header(p)

                    p.drawString(50, y, expense.date.strftime('%d/%m/%Y'))
                    p.drawString(150, y, str(expense.voucher_no))
                    p.drawString(250, y, expense.expense_head.expense_head[:38] if len(expense.expense_head.expense_head) > 40 else expense.expense_head.expense_head)
                    p.drawString(500, y, expense.narration)
                    p.drawString(650, y, str(expense.amount))

                    total_amount = total_amount + expense.amount
            y = y - 30

            p.drawString(50, y, '')
            p.drawString(150, y, '')
            p.drawString(550, y, 'Total: ')
            p.drawString(650, y, str(total_amount))

            p.showPage()
            p.save()
        return response

class OutstandingPurchaseReport(View):

    def get(self, request, *args, **kwargs):

        status_code = 200
        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1000, 1250))
        y = 1150
        p = header(p, y)
        p = footer(p, y)
        
        p.setFontSize(20)

        p.drawString(400, y - 70, 'Outstanding Purchase')
        p.setFontSize(15)
        p.drawString(50,  y - 100, "Invoice No")
        p.drawString(140,  y - 100, "Invoice Date")
        p.drawString(240,  y - 100, "Project Name")
        p.drawString(340,  y - 100, "Customer Name")
        p.drawString(500,  y - 100, "Delivery Note")
        p.drawString(600,  y - 100, "Total Amount")
        p.drawString(700, y - 100, "Paid")
        p.drawString(800, y - 100, "Balance")
        p.setFontSize(13)
        sales = Purchase.objects.filter(is_processed=False)
        y1 = y - 140
        if sales.count() > 0:
            for sale in sales:

                p.drawString(50, y1, sale.sales_invoice_number)
                p.drawString(150, y1, sale.sales_invoice_date.strftime('%d/%m/%Y'))
                p.drawString(260, y1, sale.project.name if sale.project else '')
                p.drawString(350, y1, str(sale.customer.customer_name))
                p.drawString(500,  y1, sale.delivery_note.delivery_note_number if sale.delivery_note else '')
                p.drawString(600, y1, str(sale.grant_total))
                p.drawString(700, y1, str(float(sale.grant_total) - float(sale.balance)))
                p.drawString(800, y1, str(sale.balance))
                y1 = y1 - 30

                if y1 <= 135:
                    y1 = y - 110
                    p.showPage()
                    p = header(p, y)
                    p = footer(p, y)


        p.showPage()
        p.save()

        return response