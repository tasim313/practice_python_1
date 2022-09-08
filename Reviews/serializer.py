from django.db import models
from rest_framework import serializers
from .models import *


class CreateReivewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'receiver_id', 'reviewer_id', 'service_id',
                  'rating', 'review_text']


class UpdateReivewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'receiver_id', 'reviewer_id', 'service_id',
                  'rating', 'review_text', 'response_text', 'response_date', 'review_status', 'approved_by', 'approval_date']
