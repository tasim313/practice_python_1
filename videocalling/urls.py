from django.urls import path
from .views import *
from .api import *


urlpatterns = [
    
    # videoconf url path

    path('create_account/',
         VideoCallAccountCreate.as_view(), name="create_account"),
    path('update_account/<str:token>', UpdateVideoCallAccount.as_view(), name='update_account'),
    path('demo_meeting_create/<str:token>', VideoCallCreateDemoMeeting.as_view(), name='demo_meeting_create'),
    path('create_meeting/<str:token>', VideoCallCreateMeeting.as_view(), name='meeting_create'),
    path('get_meeting_info/<str:token>', VideoCallGetMeetingInfo.as_view(), name='get_meeting_info'),
    path('VideoCallUpdateMeetingInfo/<str:token>', VideoCallUpdateMeetingInfo.as_view(), name='update_meeting'),
    path('VideoCallDeleteMeetingInfo/<str:token>', VideoCallDeleteMeetingInfo.as_view(), name='VideoCallDeleteMeetingInfo'),


    # messaging url path
    
    path('inbox/', InboxListApiView.as_view(), name='inbox'),
    path('message/thread/<uuid>/', ThreadListApiView.as_view(), name='thread'),
    path('message/thread/<user_id>/send/', ThreadCRUDApiView.as_view(), name='thread-create'),
    path('message/thread/<uuid>/<user_id>/send/', ThreadCRUDApiView.as_view(), name='thread-send'),
    path('message/thread/<user_id>/<thread_id>/edit/', EditMessageApiView.as_view(), name='message-edit'),
    path('thread/<uuid>/delete', ThreadCRUDApiView.as_view(), name='thread-delete'),

]
