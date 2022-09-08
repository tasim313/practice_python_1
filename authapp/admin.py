from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *


class UserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'middle_name', 'last_name', 'email',
                    'phone_number', 'gender', 'joining_date', 'role', 'online_status', 'account_status',
                    'activity_status', 'payment_to_method', 'payment_from_method')
    list_filter = ('email',)
    ordering = ['account_status']


admin.site.register(User, UserAdmin)


class CustomerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'avg_rating', 'lifetime_service_count',
                    'positive_review_id', 'nagetive_review_id')
    list_filter = ('lifetime_service_count', 'avg_rating')
    ordering = ['id']


admin.site.register(Customer, CustomerAdmin)


class ServiceProviderAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'businees_goal', 'spent_money_in_business', 'number_of_employees', 'founding_year', 'experience_level',
                    'company_name', 'social_media_link', 'website_url', 'batch_level', 'avg_res_time', 'avg_rating',
                    'lifetime_service_count', 'positive_review_id', 'nagetive_review_id')
    list_filter = ('company_name',)


admin.site.register(ServiceProvider, ServiceProviderAdmin)


class AddressAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'street_address', 'apt',
                    'zip_code', 'city', 'state', 'country', 'address_user')
    list_filter = ('country', 'zip_code')


admin.site.register(Address, AddressAdmin)


class AddressTypeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'address_type')


admin.site.register(AddressType, AddressTypeAdmin)


class ProfilePictureAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'uploaded_user', 'profile_picture')


admin.site.register(ProfilePicture, ProfilePictureAdmin)


class PreProviderListAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'user_customer', 'provider', 'customer_name', 'provider_name')
    list_filter = ('customer_name', 'provider_name')

admin.site.register(PreProvider, PreProviderListAdmin)





################### Changing Admin Header ########################################

admin.site.site_header = "Consult24 "
admin.site.index_title = "Consult 24 administration"
admin.site.site_title = "Consult 24 Share Knowledge Eran Money"