from django.db import models
from authapp.models import User
# Create your models here.


class Ticket(models.Model):
    Pending = 'Pending'
    creator_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='User_Create_Ticket')
    suporter_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='User_Customer_Suport_Admin', blank=True, null=True)
    supervisor_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='User_Supervisor', blank=True, null=True)
    title = models.CharField(max_length=555, blank=True, null=True)
    describtion = models.TextField(blank=True, null=True)
    summery = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)
    category_type = (
        ('Feature Request', 'Feature Request'),
        ('Complain', 'Complain'),
        ('Support request', 'Support request'),
        ('misc', 'misc')
    )
    category = models.CharField(max_length=20, choices=category_type)
    status_type = (
        ('Accepted', 'Accepted'),
        ('Denied', 'Denied'),
        ('Resolved', 'Resolved'),
        ('Pending', 'Pending')
    )
    ticket_status = models.CharField(
        max_length=20, choices=status_type, default=Pending)
    closing_date = models.DateTimeField(blank=True, null=True)

