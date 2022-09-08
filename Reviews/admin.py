from django.contrib import admin
from .models import Review
from import_export.admin import ImportExportModelAdmin
# Register your models here.


class ReviewCreateAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'reviewer_id', 'receiver_id',
                    'service_id', 'rating', 'approved_by', 'approval_date', 'review_status')
    list_filter = ('service_id', 'rating' )
    ordering = ['review_status']
    
    


admin.site.register(Review, ReviewCreateAdmin)
