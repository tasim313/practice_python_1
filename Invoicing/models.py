from django.db import models
from authapp.models import User, Address
from api.models import ServiceSubCategory
# Create your models here.


class Invoice(models.Model):
    Requested = 'Requested'
    service_provider = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='service_provider_invoice', blank=True, null=True)
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='customer_invoice', blank=True, null=True)
    sub_category = models.ForeignKey(ServiceSubCategory, on_delete=models.CASCADE,
                                     related_name='service_sub_category_invoice', blank=True, null=True)
    rate = models.CharField(max_length=555, blank=True, null=True)
    number_of_units_of_time = models.CharField(
        max_length=555, blank=True, null=True, verbose_name='Total Service Time')
    transportation_cost = models.CharField(
        max_length=555, blank=True, null=True)
    cost_for_parts = models.CharField(
        max_length=555, blank=True, null=True, verbose_name='Cost for Parts')
    tax_rate = models.CharField(
        max_length=555, blank=True, null=True, verbose_name='Tax Rate')
    customer_address = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name='Customer_Address_Info', blank=True, null=True)
    customer_phone_number = models.CharField(
        max_length=100, blank=True, null=True)
    service_provider_address = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name='Service_Provider_Address', blank=True, null=True)
    provider_phone_number = models.CharField(
        max_length=100, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    job_description = models.TextField(max_length=1000, blank=True, null=True)
    special_notes = models.TextField(max_length=1000, blank=True, null=True)
    invoice_status_choise = [
        ('Requested', 'Requested'),
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Completed', 'Completed')
    ]
    invoice_status = models.CharField(
        max_length=20, choices=invoice_status_choise, default=Requested)
