from django.urls import path

from .views import *

urlpatterns = [
    
    path('InvoiceCreateAPIView/', InvoiceRequestCreateAPIView.as_view(),
         name='InvoiceCreateAPIView'),
    path('InvoiceAcceptanceCreate_APIView/<id>', InvoiceAcceptanceCreate_APIView.as_view(),
         name='InvoiceAcceptanceCreate_APIView'),
    path('InvoiceUpdateAPIView/<id>/',
         InvoiceUpdateAPIView.as_view(), name='InvoiceUpdateAPIView'),
    path('GetCustomerInvoiceAPIView/', GetCustomerInvoiceAPIView.as_view(),
         name='GetInvoiceAPIView'),
]
