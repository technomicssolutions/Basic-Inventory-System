from django.contrib import admin

from expenses.models import *

admin.site.register(Expense)
admin.site.register(ExpenseHead)