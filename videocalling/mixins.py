from authapp.models import User
from rest_framework.generics import GenericAPIView
from .models import *

class RequireUserContextView(GenericAPIView):
    
    """
    Handles with Generics of views
    """

    def get_serializer(self, *args, **kwargs):

        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """

        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)


    def get_serializer_context(self):

        context = super().get_serializer_context()
        context.update({
            'request': self.request,
            'user' : self.request.user,
        })
        return context


class ThreadMixin:

    """
    Everything related with a thread, is placed here.
    """

    def get_thread(self):
        try:
            return Thread.objects.get(uuid=self.kwargs.get('uuid'))
        except Thread.DoesNotExist:
            return
    
    def get_user(self):
        
        """Gets a User to whom which the message will be sent"""

        try:
            return User.objects.get(pk=self.kwargs.get('user_id'))
        except User.DoesNotExist:
            return
    
    def get_thread_by_id(self):

        """Gets a thread by id"""

        try:
            return Thread.objects.get(id=self.kwargs.get('thread_id'))
        except Thread.DoesNotExist:
            return 


class CurrentThreadDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['thread']
    
    def __repr__(self):
        return '%s()' % self.__class__.__name__