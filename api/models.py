from django.db import models
from django.contrib.postgres.fields import ArrayField
from authapp.models import User, ServiceProvider, Customer

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Max


class ServiceCategory(models.Model):
    """Create Service Category model or Database"""
    id = models.AutoField(primary_key=True, verbose_name="Service Category ID")
    category_name = models.CharField(
        max_length=255, blank=True, null=True, verbose_name='Category Name')

    def __str__(self):
        return self.category_name


class ServiceSubCategory(models.Model):
    """Create Service SubCategory model or Database"""
    category = models.ForeignKey(
        ServiceCategory, on_delete=models.CASCADE, related_name='category')
    service_sub_category_name = models.CharField(
        max_length=255, blank=True, null=True)
    service_sub_category_keyword = ArrayField(models.TextField(
        null=True, blank=True), null=True, blank=True, default=[])

    def __str__(self):
        return self.service_sub_category_name


class Service(models.Model):
    """Create Service  model or Database || relation ServiceProvider,ServiceCategory, ServiceSubCategory model"""
    service_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='service_of_user')

    service_category = models.ForeignKey(
        ServiceCategory, on_delete=models.CASCADE, related_name='service_cat')

    service_sub_category = models.ForeignKey(
        ServiceSubCategory, on_delete=models.CASCADE, related_name='service_sub_category')

    service_keyword_list = ArrayField(models.TextField(
        null=True, blank=True), null=True, blank=True, default=[])
    service_name = models.CharField(max_length=255, blank=True, null=True)
    service_description = models.TextField(
        max_length=555, blank=True, null=True, verbose_name='Service Description')
    service_experiance_year = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Service Experiance Year")
    rate_apt_video_cons = models.CharField(
        max_length=255, blank=True, null=True)
    rate_inst_video_cons = models.CharField(
        max_length=255, blank=True, null=True)
    rate_inhouse_cons = models.CharField(max_length=255, blank=True, null=True)
    rate_promotion = models.CharField(max_length=255, blank=True, null=True)
    service_created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    service_status = models.BooleanField(default=False)
    service_visibility = models.BooleanField(default=False)
    service_zip_code = models.CharField(max_length=255, blank=True, null=True)
    

    def __str__(self):
        return f'{self.service_name}'


class ServiceReceived(models.Model):
    """Create Service Received model or Database || relation  ServiceProvider, Customer, Service, BillingInfo model """
    service_provider = models.ForeignKey(
        ServiceProvider, on_delete=models.CASCADE, related_name='service_rec_provider')
    service_customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='service_rec_customer')
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name='received_service')
    start_date = models.DateTimeField(blank=True, null=True)
    received_date = models.DateTimeField(blank=True, null=True)
    duration = models.CharField(max_length=255, blank=True, null=True)
    service_status = models.BooleanField(default=False)

    def __str__(self):
        return self.service.service_name


class ViolationType(models.Model):
    MISSING_APOINTMENT = 'MISSING_APOINTMENT'
    IMPROPER_CONTENT = 'IMPROPER_CONTENT'
    USER__COMPLAIN = 'USER__COMPLAIN'
    MISSING_PAYMENT = 'MISSING_PAYMENT'
    Violation_Types_CHOICES = [("MISSING_APOINTMENT", 'Missing_Apointment'), ('IMPROPER_CONTENT',
                                                                              'Improper_Content'), ('USER__COMPLAIN', 'User_Complain'), ('MISSING_PAYMENT', 'Missing_Payment')]
    violation_name = models.CharField(max_length=255, blank=True, null=True)
    violation_types = models.CharField(
        max_length=30, choices=Violation_Types_CHOICES)
    message = models.TextField()

    def __str__(self):
        return self.violation_name


class Violation(models.Model):
    ACTIVE = 'ACTIVE'
    DEACTIVE = 'DEACTIVE'
    violate_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='violate_user')
    violation_type_ID = models.ForeignKey(
        ViolationType, on_delete=models.CASCADE, related_name='violation_type_id')
    violation_start_date = models.DateTimeField(auto_now_add=True)
    violation_end_date = models.DateTimeField(blank=True, null=True)
    violation_status_CHOICES = [
        ('ACTIVE', 'Active'),
        ('DEACTIVE', 'Deactive'),
    ]
    violation_status = models.CharField(
        max_length=20, choices=violation_status_CHOICES, default=ACTIVE,)

    violation_duration = models.PositiveIntegerField()

    def __str__(self):
        return self.violation_type_ID.violation_name


class WarningModel(models.Model):
    ACTIVE = 'ACTIVE'
    DEACTIVE = 'DEACTIVE'
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='warning_user')
    violation = models.ForeignKey(
        Violation, on_delete=models.CASCADE, related_name='warning_violation_id')
    warning_date = models.DateTimeField(auto_now_add=True)
    warning_type = models.CharField(max_length=255, blank=True, null=True)
    num_of_warning = models.PositiveIntegerField()
    warning_status_CHOICES = [
        ('ACTIVE', 'Active'),
        ('DEACTIVE', 'Deactive'),
    ]
    warning_status = models.CharField(
        max_length=20, choices=warning_status_CHOICES, default=ACTIVE,)

    def __str__(self):
        return str(self.num_of_warning)


class Suspension(models.Model):
    ACTIVE = 'ACTIVE'
    DEACTIVE = 'DEACTIVE'
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='suspension_user')
    violation = models.ForeignKey(
        Violation, on_delete=models.CASCADE, related_name='suspension_violation_id')
    warning = models.ForeignKey(
        WarningModel, on_delete=models.CASCADE, related_name='warning_id')
    suspension_start_date = models.DateTimeField(auto_now_add=True)
    suspension_end_date = models.DateTimeField(blank=True, null=True)
    suspension_status_CHOICES = [
        ('ACTIVE', 'Active'),
        ('DEACTIVE', 'Deactive'),
    ]
    suspension_status = models.CharField(
        max_length=20, choices=suspension_status_CHOICES, default=ACTIVE,)

    suspension_duration = models.PositiveIntegerField()



# Create your models here.
class Appointment(models.Model):
    
    Appointment_Type_Choices = [
        ('instant_call', 'Instant Call'),
        ('inhouse', 'Inhouse'),
        ('future_call', 'Future Call'),

    ]

    appointment_provider =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointment_provider')
    appointment_customer =  models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='appointment_customer', blank=True, null=True)
    appointment_service =  models.ForeignKey(Service, on_delete=models.CASCADE, related_name='user_recieved_service')
    created_by =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointment_created_by', blank=True, null=True)
    canceled_by =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointment_canceled_by', blank=True, null=True)
    appointment_type = models.CharField(
        max_length = 255,
        choices = Appointment_Type_Choices,
      
    )
    appointment_date =  models.DateField(blank=True, null=True)
    start_time =  models.TimeField(blank=True, null=True)
    end_time =  models.TimeField(blank=True, null=True)
    duration = models.IntegerField(default=30, validators=[MinValueValidator(30), MaxValueValidator(1440)])
    day_name = models.CharField(max_length=255, blank=True, null=True)
    appointment_link = models.CharField(max_length=255, blank=True, null=True)
    appointment_link_id = models.CharField(max_length=255, blank=True, null=True)

    Status_Choices = [
    ('open', 'Open'),
    ('booked', 'Booked'),
    ('done', 'Done'),

    ]

    status = models.CharField(
        max_length = 255,
        choices = Status_Choices,
      
    )
    
    rate_multiplier = models.CharField(max_length=255, default=1)


    
    def __str__(self):
        return self.appointment_service.service_name




class videoCallingBearerTokenStore(models.Model):
    user_video_call_account = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_video_calling')
    token_store = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user_video_call_account.username


class ServiceFile(models.Model):
    service_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_service_user')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='service_info')
    service_image = models.ImageField(upload_to='service_image', null=True, blank=True)
    service_certificate = models.FileField(upload_to="service_certificate", verbose_name='Service Certificate', blank=True, null=True)