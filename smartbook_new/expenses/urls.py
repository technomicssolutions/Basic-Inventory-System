from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from expenses.views import AddExpenseHead, ExpenseHeadList, AddExpense, ExpenseList

urlpatterns = patterns('',
	url(r'^new_expense_head/$', login_required(AddExpenseHead.as_view()), name='new_expense_head'),
	url(r'^expense_head_list/$', login_required(ExpenseHeadList.as_view()), name='expense_heads'),
	url(r'^new_expense/$', login_required(AddExpense.as_view()), name='new_expense'),
	url(r'^expenses/$', login_required(ExpenseList.as_view()), name='expenses'),
)