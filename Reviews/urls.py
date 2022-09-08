from django.urls import path
from .views import *
urlpatterns = [
    path('create_review/', CreateReivew.as_view(), name='create_review'),
    path('get_review/', GetReview.as_view(), name='get_review'),
    path('update_review/<id>/', UpdateReview.as_view(), name='update_review'),
    path('viewupdatereview/', ViewUpdateReview.as_view(), name='viewupdatereview'),
    path('calulate_average_rating/<id>', calulate_average_rating, name="receiver_id"),
]
