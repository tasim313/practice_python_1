from django.urls import path
from .views import *

urlpatterns = [
    path('create_ticket/', CreateTicket.as_view(), name='create_ticket'),
    path('get_ticket/', GetTickets.as_view(), name='get_ticket'),
    path('update_ticket/<id>/', UpdateTicket.as_view(), name='update_ticket'),
    path('getTicketStatus/', getTicketStatus.as_view(), name='getTicketStatus'),
]
