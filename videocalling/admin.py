from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *



class ThreadAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'uuid', 'subject']
    list_filter = ["subject"]
    

admin.site.register(Thread, ThreadAdmin)


class UserThreadAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'uuid', "thread", "user", "unread", "deleted"]
    list_filter = ["unread", "deleted"]
    raw_id_fields = ["user"]

admin.site.register(UserThread, UserThreadAdmin)




class MessageAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["thread", "sender", "sent_at"]
    list_filter = ["sent_at", "thread"]
    raw_id_fields = ["sender"]

admin.site.register(Message, MessageAdmin)
