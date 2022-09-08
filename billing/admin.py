from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *


class BankInfoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'bank_info_user', 'bank_name', 'bank_branch_name', 'bank_account_name',
                    'bank_account_number')
    list_filter = ('bank_name', 'bank_info_user' )
    ordering = ['id']
                    
admin.site.register(BankInfo, BankInfoAdmin)


class CreditCardInfoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'credit_card_info_user', 'credit_card_name',
                    'credit_card_number', 'credit_card_expire_date')
   
    list_filter = ('credit_card_info_user', 'credit_card_name' )
    ordering = ['id']


admin.site.register(CreditCardInfo, CreditCardInfoAdmin)


class BillingInfoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'billing_user', 'billing_date',
                    'billing_time', 'payment_method', 'billing_amount', 
                    'billing_type', 'billing_due_date', 'service_received_id_list', 'billing_status')
    
    list_filter = ('billing_user', 'billing_status', 'service_received_id_list')
    ordering = ['billing_status']


admin.site.register(BillingInfo, BillingInfoAdmin)

