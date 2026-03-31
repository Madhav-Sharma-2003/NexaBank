from django.contrib import admin
from .models import BankAccount, Transaction

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'account_number', 'account_type', 'balance', 'created_at']
    list_filter = ['account_type']
    search_fields = ['user__username', 'account_number']
    readonly_fields = ['account_number', 'created_at']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['account', 'transaction_type', 'amount', 'description', 'timestamp']
    list_filter = ['transaction_type']
    search_fields = ['account__user__username', 'account__account_number']
    readonly_fields = ['timestamp']