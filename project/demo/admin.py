from django.contrib import admin

from .models import Account, Transaction


class TransactionInline(admin.TabularInline):
    model = Transaction


class AccountAdmin(admin.ModelAdmin):
    extra = 0
    inlines = [TransactionInline]


admin.site.register(Transaction)
admin.site.register(Account, AccountAdmin)
