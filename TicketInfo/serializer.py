from django.db import models
from rest_framework import serializers
from .models import *


class CreateTicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ['id', 'creator_id', 'title', 'describtion',
                  'summery', 'creation_date', 'category']


class GetTicketStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ['id', 'creator_id', 'title', 'describtion',
                  'summery', 'creation_date', 'category', 'ticket_status']


class TicketStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('__all__')
