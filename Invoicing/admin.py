from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *


class InvoiceAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'service_provider', 'customer', 'sub_category', 'rate',
                    'customer_phone_number', 'provider_phone_number', 'invoice_status')
    
    ordering = ['invoice_status']
    list_filter = ('service_provider', 'customer', 'rate')

admin.site.register(Invoice, InvoiceAdmin)
