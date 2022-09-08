from django.db import models
from authapp.models import User
from api.models import Service
# Create your models here.


class Review(models.Model):
    rating_choice = (
        (1, "Worst"),
        (2, "Bad"),
        (3, "Average"),
        (4, "Good"),
        (5, "Excellent"),
    )
    receiver_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_receiver')
    reviewer_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_reviewer')
    service_id = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name='user_service_use')
    approved_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_approve', blank=True, null=True)
    rating = models.IntegerField(choices=rating_choice, blank=True, null=True)
    review_text = models.CharField(max_length=1000, blank=True, null=True)
    response_text = models.CharField(max_length=1000, blank=True, null=True)
    response_date = models.DateTimeField(blank=True, null=True)
    review_status_choice = [
        ('PUBLISHED', 'Published'),
        ("UNPUBLISHED", 'Unpublished')
    ]
    review_status = models.CharField(
        max_length=20, choices=review_status_choice, blank=True, null=True)
    approval_date = models.DateTimeField(blank=True, null=True)


