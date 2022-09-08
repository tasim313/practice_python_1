from django.db import models
from django.contrib.postgres.fields import ArrayField
from authapp.models import User


class BillingInfo(models.Model):
    Pending = "Pending"
    billing_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="billing_user")
    billing_date = models.DateField()
    billing_time = models.TimeField()
    payment_method_choise = [
        ('bank', 'Bank'),
        ('credit_card', 'Credit Card'),
    ]
    payment_method = models.CharField(
        max_length=20, choices=payment_method_choise)
    billing_amount = models.IntegerField()
    billing_type_choise = [
        ('billing', 'Billing'),
        ('payment', 'Payment'),
    ]
    billing_type = models.CharField(max_length=20, choices=billing_type_choise)
    billing_due_date = models.DateTimeField()
    service_received_id_list = ArrayField(models.TextField(
        null=True, blank=True), null=True, blank=True, default=[])
    billing_status_choise = [
        ('Pending', 'Pending'),
        ('UnPaid', 'UnPaid'),
        ('Paid', 'Paid'),
    ]
    billing_status = models.CharField(
        max_length=20, choices=billing_status_choise, default=Pending)

    def __str__(self):
        return self.billing_user.username


class BankInfo(models.Model):

    bank_info_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bank_info_user')
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    bank_branch_name = models.CharField(max_length=255, blank=True, null=True)
    bank_account_name = models.CharField(max_length=255, blank=True, null=True)
    bank_account_number = models.CharField(
        max_length=255, blank=True, null=True)
    # bank_swift_code = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.bank_info_user.username


class CreditCardInfo(models.Model):

    credit_card_info_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='card_info_user')
    credit_card_name = models.CharField(max_length=255, blank=True, null=True)
    credit_card_number = models.CharField(
        max_length=255, blank=True, null=True)
    credit_card_expire_date = models.CharField(
        max_length=255, blank=True, null=True)
    cvv_number = models.CharField(max_length=10, blank=True, null=True)
    def __str__(self):
        return self.credit_card_info_user.username
