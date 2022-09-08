from xmlrpc.client import Server
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse

from rest_framework import mixins
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import pagination

from .models import *
from .serializers import *
from .pagination import *
from api.models import ServiceReceived
from authapp.models import Customer, ServiceProvider
from authapp.permissions import *



class CustomerBillingInfoAdd(APIView):

    """
    Customer Billing Info Add.
    """

    permission_classes = [IsAuthenticated, CustomerPermission]
    serializer_class = BilingInfoSerializer
    
    def post(self, request, format=None):

        billing_date = request.data['billing_date']
        billing_time = request.data['billing_time']
        payment_method = request.data['payment_method']
        billing_amount = request.data['billing_amount']
        billing_type = request.data['billing_type']
        billing_due_date = request.data['billing_due_date']
        # service_received_id_list = request.data['service_received_id_list']
        billing_status = request.data['billing_status']

        user_info = User.objects.filter(pk=request.user.id)

        service_received_id_list = [] 
        print(f'user_info {user_info}')
        for customer_user in user_info:
            customer_obj = Customer.objects.filter(user_customer__id=customer_user.id)
            print(f'customer {customer_obj}')

            for customer_user in customer_obj:

                service_received = ServiceReceived.objects.filter(service_customer__id=customer_user.id)
                print(f'service_received {service_received}')
                for s_r_id in service_received:
                    service_received_id_list.append(s_r_id.id)


        try:
            BillingInfo.objects.create(billing_user=request.user, billing_date=billing_date, billing_time=billing_time, 
                                        payment_method=payment_method, billing_amount=billing_amount, 
                                        billing_type=billing_type, billing_due_date=billing_due_date, 
                                        service_received_id_list=service_received_id_list, billing_status=billing_status)
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class ProviderBillingInfoAdd(APIView):

    """
    Provider Billing Info Add.
    """

    permission_classes = [IsAuthenticated, ServiceProviderPermission]
    serializer_class = BilingInfoSerializer
    
    
    def post(self, request, format=None):

        billing_date = request.data['billing_date']
        billing_time = request.data['billing_time']
        payment_method = request.data['payment_method']
        billing_amount = request.data['billing_amount']
        billing_type = request.data['billing_type']
        billing_due_date = request.data['billing_due_date']
        # service_received_id_list = request.data['service_received_id_list']
        billing_status = request.data['billing_status']

        user_info = User.objects.filter(pk=request.user.id)

        service_received_id_list = [] 
        print(f'user_info {user_info}')
        for provider_user in user_info:
            provider_obj = ServiceProvider.objects.filter(user_service_provider__id=provider_user.id)
            print(f'provider_obj {provider_obj}')

            for provider_user in provider_obj:

                service_received = ServiceReceived.objects.filter(service_provider__id=provider_user.id)
                print(f'service_received {service_received}')
                for s_r_id in service_received:
                    service_received_id_list.append(s_r_id.id)


        try:
            BillingInfo.objects.create(billing_user=request.user, billing_date=billing_date, billing_time=billing_time, 
                                        payment_method=payment_method, billing_amount=billing_amount, 
                                        billing_type=billing_type, billing_due_date=billing_due_date, 
                                        service_received_id_list=service_received_id_list, billing_status=billing_status)
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)




class CustomerPaymentInfoView(APIView):
    """
    Customer Payment Info View.
    """

    permission_classes = [IsAuthenticated, CustomerPermission]
    serializer_class = BilingInfoSerializer

    def get(self, request, user_id, format=None):
        user_info = BillingInfo.objects.filter(billing_user_id=user_id)
        
        print(f'user info {user_info}')

        try:
            serializer = BilingInfoSerializer(user_info, many=True)
            return Response(serializer.data)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def put(self, request, user_id, format=None):
        user_info = BillingInfo.objects.filter(billing_user_id=user_id)
        serializer = BilingInfoSerializer(user_info, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProviderPaymentInfoView(APIView):
    """
    Provider Payment Info View.
    """

    permission_classes = [IsAuthenticated, ServiceProviderPermission]
    serializer_class = BilingInfoSerializer

    def get(self, request, user_id, format=None):
        user_info = BillingInfo.objects.filter(billing_user_id=user_id)
        
        print(f'user info {user_info}')

        try:
            serializer = BilingInfoSerializer(user_info, many=True)
            return Response(serializer.data)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def put(self, request, user_id, format=None):
        user_info = BillingInfo.objects.filter(billing_user_id=user_id)
        serializer = BilingInfoSerializer(user_info, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CustomerBankInfoAdd(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):

    """
    Customer Bank Info Add Api View.
    """

    permission_classes = [IsAuthenticated, CustomerPermission]
    serializer_class = BankInfoSerializer
    
    queryset = BankInfo.objects.all()
    serializer_class = BankInfoSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CustomerBankInfoCRUD(APIView):
    """
    Retrieve, update or delete a Customer Bank Info.
    """

    permission_classes = [IsAuthenticated, CustomerPermission]
    serializer_class = BankInfoSerializer


    def get_object(self, user_id):
        try:
            return BankInfo.objects.filter(bank_info_user=user_id)
        except BankInfo.DoesNotExist:
            raise Http404
    
    
    def get(self, request, user_id, format=None):
        user_bank_info = self.get_object(user_id)
        serializer = BankInfoSerializer(user_bank_info, many=True)
        return Response(serializer.data)

    def put(self, request, user_id, format=None):
        user_bank_info = self.get_object(user_id)
        serializer = BankInfoSerializer(user_bank_info, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id, format=None):
        user_bank_info = self.get_object(user_id)
        user_bank_info.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProviderBankInfoAdd(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):

    """
    Provider Bank Info Add.
    """

    permission_classes = [IsAuthenticated, ServiceProviderPermission]
    serializer_class = BankInfoSerializer
    
    queryset = BankInfo.objects.all()
    serializer_class = BankInfoSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



class ProviderBankInfoCRUD(APIView):
    """
    Retrieve, update or delete a Provider Bank Info.
    """

    permission_classes = [IsAuthenticated, ServiceProviderPermission]
    serializer_class = BankInfoSerializer


    def get_object(self, user_id):
        try:
            return BankInfo.objects.filter(bank_info_user=user_id)
        except BankInfo.DoesNotExist:
            raise Http404

    def get(self, request, user_id, format=None):
        user_bank_info = self.get_object(user_id)
        serializer = BankInfoSerializer(user_bank_info, many=True)
        return Response(serializer.data)

    def put(self, request, user_id, format=None):
        user_bank_info = self.get_object(user_id)
        serializer = BankInfoSerializer(user_bank_info, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id, format=None):
        user_bank_info = self.get_object(user_id)
        user_bank_info.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class CustomerCreditCardInfoAdd(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):

    """
    Customer Credit Card Info Add Api View.
    """

    permission_classes = [IsAuthenticated, CustomerPermission]
    serializer_class = CreditCardInfoSerializer
    
    queryset = CreditCardInfo.objects.all()
    serializer_class = CreditCardInfoSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CustomerCreditCardInfoCRUD(APIView):
    """
    Retrieve, update or delete a Customer Credit Card Info.
    """

    permission_classes = [IsAuthenticated, CustomerPermission]
    serializer_class = CreditCardInfoSerializer


    def get_object(self, user_id):
        try:
            return CreditCardInfo.objects.filter(credit_card_info_user=user_id)
        except BankInfo.DoesNotExist:
            raise Http404

    def get(self, request, user_id, format=None):
        user_credit_card_info = self.get_object(user_id)
        serializer = CreditCardInfoSerializer(user_credit_card_info, many=True)
        return Response(serializer.data)

    def put(self, request, user_id, format=None):
        user_credit_card_info = self.get_object(user_id)
        serializer = CreditCardInfoSerializer(user_credit_card_info, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id, format=None):
        user_credit_card_info = self.get_object(user_id)
        user_credit_card_info.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class ProviderCreditCardInfoAdd(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):

    """
    Provider Credit Card Info Add Api View.
    """

    permission_classes = [IsAuthenticated, ServiceProviderPermission]
    serializer_class = CreditCardInfoSerializer
    
    queryset = CreditCardInfo.objects.all()
    serializer_class = CreditCardInfoSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProviderCreditCardInfoCRUD(APIView):
    """
    Retrieve, update or delete a Provider Credit CardInfo.
    """

    permission_classes = [IsAuthenticated, ServiceProviderPermission]
    serializer_class = CreditCardInfoSerializer


    def get_object(self, user_id):
        try:
            return CreditCardInfo.objects.filter(credit_card_info_user=user_id)
        except BankInfo.DoesNotExist:
            raise Http404

    def get(self, request, user_id, format=None):
        user_credit_card_info = self.get_object(user_id)
        serializer = CreditCardInfoSerializer(user_credit_card_info, many=True)
        return Response(serializer.data)

    def put(self, request, user_id, format=None):
        user_credit_card_info = self.get_object(user_id)
        serializer = CreditCardInfoSerializer(user_credit_card_info, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id, format=None):
        user_credit_card_info = self.get_object(user_id)
        user_credit_card_info.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class CreateBillApiView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):

    """
    Create Bill Api View For Internal Uses.
    """

    queryset = BillingInfo.objects.all()
    serializer_class = BilingInfoSerializer
    pagination_class = StandardResultsSetPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)




## Service Provider Lists with filtering
class GetBillHistoryListView(generics.ListAPIView):
    """
    Service Provider List with filtering all fields of user and locations.
    """
    
    permission_classes = [IsAuthenticated]

    queryset = BillingInfo.objects.all()
    serializer_class = BilingInfoSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['billing_user', 'billing_date', 'billing_time']





        




