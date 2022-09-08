from django.urls import path, include
from .views import *


urlpatterns = [
    path('Ad_By_Tag/', Ad_By_Tag.as_view(), name='Ad_By_Tag'),
    path('get_ad_by_user_id/<id>', get_ad_by_user_id,
         name='get_ad_by_user_id'),
    path('ADInterest/', AD_Interest.as_view(), name='AD_Interest'),
    path('DeleteAdInterest/<id>', DeleteAdInterest.as_view(),
         name='DeleteAdInterest'),
    path('Ad_Interest_Create/', Ad_Interest_Create.as_view(),
         name='Ad_Interest_Create'),

    path('user_adimage/', user_adimage_upload.as_view(),
         name='user_adimage_upload'),
    path('user_advideo_upload/', user_advideo_upload.as_view(),
         name='user_advideo_upload'),
    path('upload_Ad_Media/',  upload_Ad_Media.as_view(), name='upload_Ad_Media'),
    #     path('uploadImageAdMedia/', uploadImageAdMedia.as_view(),
    #          name='uploadImageAdMedia'),
]
