from django.shortcuts import render
from .models import Invoice
from .serializer import *
from api.views import StandardResultsSetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from datetime import timedelta, datetime
from rest_framework import filters


class InvoiceRequestCreateAPIView(generics.ListCreateAPIView):

    """ Create the Invoice Request with given invoice data. Any authenticated user can create  invoice request """

    permission_classes = [IsAuthenticated]
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    pagination_class = StandardResultsSetPagination


class InvoiceAcceptanceCreate_APIView(generics.RetrieveUpdateDestroyAPIView):

    """ Create the Invoice Acceptance with given invoice data. Any authenticated user can create invoice acceptance """

    permission_classes = [IsAuthenticated]
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    pagination_class = StandardResultsSetPagination
    lookup_field = 'id'


class InvoiceUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):

    """ Update the Invoice  with given invoice data . Any authenticated user can update invoice """

    permission_classes = [IsAuthenticated]
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    pagination_class = StandardResultsSetPagination
    lookup_field = 'id'


class GetCustomerInvoiceAPIView(generics.ListAPIView):

    """Get Invoice information userID and filters By invoice ID, Last 5 invoices, invoices by status """

    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    serializer_class = InvoiceSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ['id', 'invoice_status', 'end_date']

    def get_queryset(self, *args, **kwargs):
        user_id = self.request.query_params.get('user_id')
        orderbyList = ['end_date', 'start_date']
        from_date = datetime.now() - timedelta(days=30)
        queryset = Invoice.objects.all()
        if user_id is not None:
            queryset = Invoice.objects.filter(
                customer=user_id, end_date__gt=from_date).order_by(*orderbyList) | Invoice.objects.filter(service_provider=user_id, end_date__gt=from_date).order_by(*orderbyList)
        return queryset
