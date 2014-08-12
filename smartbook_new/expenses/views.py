
import ast
import simplejson
import datetime as dt
from datetime import datetime
from decimal import *


from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from expenses.models import ExpenseHead,Expense
from .models import *


class AddExpenseHead(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'expenses/add_expense_head.html', {})

    def post(self, request, *args, **kwargs):

        post_dict = request.POST
        status = 200

        try:
            if len(post_dict['head_name']) > 0 and not post_dict['head_name'].isspace():
                expense_head, created = ExpenseHead.objects.get_or_create(expense_head = post_dict['head_name'])
                if created:
                    context = {
                        'message' : 'Added successfully',
                    }
                    res = {
                        'result': 'ok',
                        'head_id': expense_head.id,
                    }
                else:
                    context = {
                        'message' : 'This Head name is Already Existing',
                    }
                    res = {
                        'result': 'error',
                        'message': 'This Head name is Already Existing',
                    }

            else:
                context = {
                    'message' : 'Head name Cannot be null',
                }
        except Exception as ex:
            context = {
                'message' : post_dict['head_name']+' is already existing',
            }
            res = {
                'result': 'error',
                'message': post_dict['head_name']+' is already existing',
            }
        if request.is_ajax():
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')
        return render(request, 'expenses/add_expense_head.html', context)

class ExpenseHeadList(View):

    def get(self, request, *args, **kwargs):

        ctx_expense_head = []
        status_code = 200
        expense_heads = ExpenseHead.objects.all()
        if len(expense_heads) > 0:
            for head in expense_heads:
                ctx_expense_head.append({
                    'head_name': head.expense_head,
                    'id': head.id, 
                })
        res = {
            'result': 'ok',
            'expense_heads':ctx_expense_head
        }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=status_code, mimetype="application/json")

class Expenses(View):

    def get(self, request, *args, **kwargs):

        current_date = dt.datetime.now().date()
        expenses = Expense.objects.all().count()
        if int(expenses) > 0:
            latest_expense = Expense.objects.latest('id')
            voucher_no = int(latest_expense.voucher_no) + 1
        else:
            voucher_no = 1
        context = {
            'current_date': current_date.strftime('%d/%m/%Y'),
            'voucher_no': voucher_no
        }
        
        return render(request, 'expenses/expense.html', context)

    def post(self, request, *args, **kwargs):

        post_dict = ast.literal_eval(request.POST['expense'])
        expense = Expense.objects.create(created_by=request.user, voucher_no=post_dict['voucher_no'])
        expense.expense_head = ExpenseHead.objects.get(id = post_dict['expense_head_id'])
        expense.date = datetime.strptime(post_dict['date'], '%d/%m/%Y')
        expense.amount = post_dict['amount']
        expense.payment_mode = post_dict['payment_mode']
        expense.narration = post_dict['narration']
        if post_dict['payment_mode'] == 'cheque':
            expense.cheque_no = post_dict['cheque_no']
            expense.cheque_date = datetime.strptime(post_dict['cheque_date'], '%d/%m/%Y')
            expense.bank_name = post_dict['bank_name']
            expense.branch = post_dict['branch']
        expense.save()
        try:
            project = Project.objects.get(id=post_dict['project_id'])
            project.expense_amount = float(project.expense_amount) + float(post_dict['amount'])
            project.save()
            expense.project = project
            expense.save()
        except Exception as ex:
            print str(ex)
            project = None
            
        res = {
            'result': 'ok'
        }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype="application/json")