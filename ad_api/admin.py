from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.


class LinkAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'link_name', 'description', 'link_type', 'link_url')
    list_filter = ('link_name', 'link_type')
    


admin.site.register(Link, LinkAdmin)


class adAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'ad_type', 'rate_per_show', 'rate_per_click', 'start_date',
                    'end_date', 'show_count', 'click_count', 'window_size_list', 'window_location_list', 'ad_tag_list', 'audience_interest_type', 'is_published')


admin.site.register(ad, adAdmin)


class adInterestAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'ad_tag_list', 'entry_date')


admin.site.register(UserAdInterest, adInterestAdmin)


class UploadADMediaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'user_id', 'image', 'video')


admin.site.register(UploadADMedia, UploadADMediaAdmin)
