from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db.models.signals import post_save

from api.models import *
from django.contrib.postgres.fields import ArrayField


class CustomUserManager(BaseUserManager):
    # def create_user(self, email, username, first_name, last_name, phone_number, password=None, **extra_fields):
    def create_user(self, email, username, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, username,
        first name, last name, phone number and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')
        # if not first_name:
        #     raise ValueError('Users must have to give there first name')
        # if not last_name:
        #     raise ValueError('Users must have to give there last name')
        # if not phone_number:
        #     raise ValueError('User must have to give there phone number')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            # first_name=first_name,
            # last_name=last_name,
            # phone_number=phone_number,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # def create_superuser(self, email, username, first_name, last_name, password, **extra_fields):

    def create_superuser(self, email, username, password, **extra_fields):
        """
        Creates and saves a Super User with the given email, username,
        first name, last name, phone number and password.
        """

        extra_fields.setdefault('role', 1)
        if extra_fields.get('role') != 1:
            raise ValueError('Superuser must have role of Global Admin')
        # return self.create_user(email, password, **extra_fields)

        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            # first_name=first_name,
            # last_name=last_name,
            **extra_fields,
        )

        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    username = models.CharField(
        verbose_name='username',
        max_length=255,
        null=True,
    )

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    first_name = models.CharField(max_length=255, blank=False)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=False)
    phone_number = models.CharField(max_length=20, blank=False, null=True)

    # Created by tasim.........
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    gender = models.CharField(
        max_length=20, choices=GENDER_CHOICES, blank=True, null=True)

    ADMIN = 1
    CUSTOMER = 2
    SERVICE_PROVIDER = 3
    CUSTOMER_SUPPORT = 4

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (CUSTOMER, 'Customer'),
        (SERVICE_PROVIDER, 'Service_provider'),
        (CUSTOMER_SUPPORT, 'Customer_support'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES)
    joining_date = models.DateTimeField(auto_now_add=True)

    account_status_choise = [
        ('active', 'Active'),
        ('disable', 'Disable'),
        ('suspended', 'Suspend')
    ]
    account_status = models.CharField(
        max_length=20, choices=account_status_choise)
    online_status = models.BooleanField(default=False)
    # ---(busy(is he in call with someone), available)
    activity_status = models.BooleanField(default=False)

    # Service provider payment info- we will pay to service provider
    payment_to_method = models.CharField(
        max_length=255, verbose_name='Payment To Method', null=True, blank=True)
    # Customer payment info- we will recieve from customer
    payment_from_method = models.CharField(
        max_length=255, verbose_name='Payment From Method', null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    # REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone_number', 'role']
    REQUIRED_FIELDS = ['username', 'role']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class ProfilePicture(models.Model):

    uploaded_user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='profile_picture', null=True, blank=True)

    def __str__(self):
        return self.uploaded_user.username


class UploadVideoModel(models.Model):

    # uploaded_user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_link = models.FileField(null=True, blank=True)

    # def __str__(self):
    #     return self.uploaded_user.username


class ServiceProvider(models.Model):

    user_service_provider = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user_service_provider')
    businees_goal = models.CharField(max_length=255, blank=True, null=True)
    spent_money_in_business = models.CharField(
        max_length=255, blank=True, null=True)
    number_of_employees = models.CharField(
        max_length=255, blank=True, null=True)
    founding_year = models.CharField(max_length=255, blank=True, null=True)
    experience_level = models.CharField(max_length=255, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    social_media_link = models.CharField(max_length=255, blank=True, null=True)
    website_url = models.CharField(max_length=255, blank=True, null=True)
    batch_level = models.CharField(max_length=255, blank=True, null=True)
    avg_res_time = models.CharField(max_length=255, blank=True, null=True)
    avg_rating = models.CharField(max_length=255, blank=True, null=True)
    lifetime_service_count = models.CharField(
        max_length=255, blank=True, null=True)
    positive_review_id = models.CharField(
        max_length=255, blank=True, null=True)
    nagetive_review_id = models.CharField(
        max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user_service_provider.username


def create_service_provider(sender, instance, created, **kwargs):

    if created:
        service_provider = User.objects.get(id=instance.id)
        print('test', service_provider)

        if service_provider.role == 3:
            ServiceProvider.objects.create(user_service_provider=instance)
            print(
                f'sender:{sender}, instance-{instance}, created-{created}, kw-{kwargs}')


post_save.connect(create_service_provider, sender=User)


class Customer(models.Model):

    user_customer = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user_customer')
    avg_rating = models.CharField(max_length=255, blank=True, null=True)
    lifetime_service_count = models.CharField(
        max_length=255, blank=True, null=True)
    positive_review_id = models.CharField(
        max_length=255, blank=True, null=True)
    nagetive_review_id = models.CharField(
        max_length=255, blank=True, null=True)
    

    def __str__(self):
        return self.user_customer.username


def create_customer(sender, instance, created, **kwargs):

    if created:
        customer = User.objects.get(id=instance.id)
        print('testttttttt', customer)

        if customer.role == 2:
            Customer.objects.create(user_customer=instance)
            print(
                f'sender:{sender}, instance-{instance}, created-{created}, kw-{kwargs}')
            # print("Prifile picture modal created")


post_save.connect(create_customer, sender=User)


class Address(models.Model):

    address_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_address')
    street_address = models.CharField(max_length=255, blank=True, null=True)
    apt = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.address_user.username


def create_user_address_profile_picture(sender, instance, created, **kwargs):

    if created:
        user = User.objects.get(id=instance.id)
        print('user', user)

        if user:
            Address.objects.create(address_user=instance)
            ProfilePicture.objects.create(uploaded_user=instance)
            print(
                f'sender:{sender}, instance-{instance}, created-{created}, kw-{kwargs}')
            # print("Prifile picture modal created")


post_save.connect(create_user_address_profile_picture, sender=User)


class AddressType(models.Model):

    address_id = models.OneToOneField(
        Address, on_delete=models.CASCADE, related_name='user_address_type')
    address_type = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.address_type


class PreProvider(models.Model):
    # pref_provider_list model
    user_customer = models.CharField(max_length=30, blank=True, null=True)
    provider = models.CharField(max_length=30, blank=True, null=True)
    customer_name = models.CharField(max_length=550, blank=True, null=True)
    provider_name = models.CharField(max_length=550, blank=True, null=True)

