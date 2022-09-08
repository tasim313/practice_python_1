from django.contrib import admin
from . models import *
from import_export.admin import ImportExportModelAdmin


class TicketAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'creator_id', 'suporter_id', 'supervisor_id',
                    'title', 'creation_date', 'category', 'ticket_status')

    list_filter = ('category', 'ticket_status')

admin.site.register(Ticket, TicketAdmin)
