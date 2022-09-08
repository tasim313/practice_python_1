""" This view create video calling authentication url when we call  google api this api also call """


from django.dispatch import receiver
from authapp.models import User
from .api import *
from djoser.signals import user_activated

@receiver(user_activated)
def activate_profile(user, request):
    User.objects.create(user=user)

    