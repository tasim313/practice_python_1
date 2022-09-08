from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *


class ServiceCategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'category_name',)
    list_filter = ('category_name',)


admin.site.register(ServiceCategory, ServiceCategoryAdmin)


class ServiceSubCategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'service_sub_category_name',
                    'service_sub_category_keyword')
    list_filter = ('service_sub_category_name',)


admin.site.register(ServiceSubCategory, ServiceSubCategoryAdmin)


class ServiceAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'service_user', 'service_category', 'service_sub_category', 'service_keyword_list', 'service_name',
                    'service_experiance_year', 'rate_apt_video_cons', 'rate_inst_video_cons', 'rate_inhouse_cons', 'rate_promotion',
                    'service_created_date', 'service_status', 'service_visibility')
    list_filter = ('service_user','service_name', )
    ordering = ['service_status']


admin.site.register(Service, ServiceAdmin)


class ServiceReceivedAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'start_date', 'received_date',
                    'duration', 'service_status')
    list_filter = ('duration', 'received_date')
    ordering = ['service_status']


admin.site.register(ServiceReceived, ServiceReceivedAdmin),


class violationTypeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'violation_name', 'violation_types', 'message')


admin.site.register(ViolationType, violationTypeAdmin)


class ViolationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'violation_start_date', 'violation_end_date', 'violation_duration',
                    'violation_status')


admin.site.register(Violation, ViolationAdmin)


class warningAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'warning_date', 'warning_type',
                    'num_of_warning', 'warning_status')


admin.site.register(WarningModel, warningAdmin)


class SuspensionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'suspension_start_date', 'suspension_end_date', 'suspension_duration',
                    'suspension_status')
    list_filter = ('suspension_duration', 'suspension_status')


admin.site.register(Suspension, SuspensionAdmin)


class AppointmentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'appointment_provider', 'appointment_customer', 'appointment_service', 'appointment_type',
                    'appointment_date', 'start_time', 'end_time', 'duration', 'status', 'rate_multiplier', 'day_name')
    list_filter = ('appointment_service', 'appointment_type', 'duration', 'status')
    ordering = ['appointment_date']


admin.site.register(Appointment, AppointmentAdmin)


class VideoCallingTokenAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'user_video_call_account', 'token_store')

admin.site.register(videoCallingBearerTokenStore, VideoCallingTokenAdmin)


class ServiceFileAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'service_user', 'service', 'service_image', 'service_certificate')

admin.site.register(ServiceFile, ServiceFileAdmin)


