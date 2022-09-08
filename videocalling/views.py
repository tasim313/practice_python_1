import logging

from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .mixins import RequireUserContextView, ThreadMixin
from .models import Message, Thread
from .pagination import Pagination
from .permissions import DjangoMessageDRFAuthMixin
from .serializers import MessageSerializer

from .settings import (
    EDIT_MESSAGE_SERIALIZER,
    INBOX_SERIALIZER,
    THREAD_REPLY_SERIALIZER,
    THREAD_SERIALIZER,
)

log = logging.getLogger(__name__)


class InboxListApiView(RequireUserContextView, ListAPIView):
    
    """
    Returns the Inbox the logged in User
    """

    serializer_class = INBOX_SERIALIZER
    pagination_class = Pagination

    def get_queryset(self):
        queryset = Thread.inbox(self.request.user)
        return Thread.ordered(queryset)



class ThreadListApiView(ThreadMixin, RequireUserContextView, ListAPIView):
    
    """
    Gets all the messages from a given thread
    """

    serializer_class = THREAD_SERIALIZER

    def get(self, request, *args, **kwargs):
        instace = self.get_thread()
        if not instace:
            raise NotFound()
        
        serializer = self.serializer_class(instace, context=self.get_serializer_context())
        return Response(serializer.data, status=status.HTTP_200_OK)




class ThreadCRUDApiView(ThreadMixin, RequireUserContextView, APIView):
    
    """
    View that allows the reply of a specific message as well as the
    We will apply some pagination to return a list for the results and therefore
    1. This API gets or creates the Thread
    2. If a UUID is passed, then a Thread is validated and created but if only a user_id is
    passed, then it will create a new thread and start a conversation.
    """

    serializer_class = THREAD_REPLY_SERIALIZER

    def post(self, request, uuid=None, *args, **kwargs):
        
        """
        Replies a mensage in given thread
        """
        thread = self.get_thread() if uuid else None
        user = self.get_user()

        if not user:
            raise NotFound()

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        subject = serializer.data.get('subject') or thread.subject
        if not thread:
            msg = Message.new_message(
                from_user = self.request.user, to_users=[user], subject=subject,
                content=serializer.data.get('message')
            )
        
        else:
            msg = Message.new_reply(thread, self.request.user, serializer.data.get('message'))
            thread.subject = subject
            thread.save()
        
        message = MessageSerializer(msg, context=self.get_serializer_context())
        return Response(message.data, status=status.HTTP_201_CREATED)
    

    def delete(self, request, *args, **kwargs):

        """
        Flags a thread as deleted from the system.
        To remove completely, another permanent view can be added to execute the action.
        """

        thread = self.get_thread()
        if not thread:
            raise NotFound()

        thread.userthread_set.filter(user=request.user).update(deleted=True)
        return Response(status=status.HTTP_200_OK)


class EditMessageApiView(ThreadMixin, RequireUserContextView, APIView):

    """
    Edits a message sent from a user in a given thread
    """

    serializer_class = EDIT_MESSAGE_SERIALIZER

    def get_instance(self, user, message_uuid):
        
        """
        Checks of the message exists
        """

        try:
            return Message.objects.get(sender=user, uuid=message_uuid)

        except Message.DoesNotExist:
            return
        
        def get_serializer_context(self):
            context = super().get_serializer_context()
            context.update({
                'thread' : self.get_thread_by_id(),
            })
            return context
        
        def put(self, request, user_id, thread_id, *args, **kwargs):
            
            """
            Edits a mensage in given thread.
            1. Gets the user_id from the URL.
            2. From the request.data gets the uuid of the message
            3. Validates
            4. Saves and returns
            """

            user = self.get_user()

            if not user:
                raise Notfound()

            if (not user.pk == request.user.pk):
                raise PermissionDenied()
            
            instace = self.get_instance(user, request.data.get('uuid'))
            if not instace:
                raise NotFound()

            serializer = self.serializer_class(instance, data=request.data, context=self.get_serializer_context())
            serializer.is_valid(raise_exception=True)
            instace = serializer.save()

            message = MessageSerializer(instace, context=self.get_serializer_context())
            return Response(message.data, status=status.HTTP_200_OK)