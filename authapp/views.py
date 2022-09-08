import cv2
import tempfile
from pathlib import Path
from multiprocessing import context
from urllib import request, response
from django.http import HttpResponse, JsonResponse
from rest_framework import status

from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, mixins, viewsets
from rest_framework.generics import ListAPIView

from rest_framework.response import Response
from rest_framework.views import APIView

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.parsers import JSONParser, FileUploadParser, MultiPartParser, FormParser

from django.http import Http404

from .models import *
from .serializers import *
from .permissions import *
from .pagination import StandardResultsSetPagination

from api.serializers import *
from api.models import *

from datetime import timedelta, datetime





# Provider User, ServiceProvider and Address table data GET, UPDATE and DELETE ---Naznin


class ServiceProviderProfile(APIView):
    """
    Provider Profile Retrieve and Update.
    """
    permission_classes = [IsAuthenticated, ServiceProviderPermission]

    # Getting user id from authenticate user
    def get_object(self, pk):
       
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    # Getting Provider information from three table as User, ServiceProvider, Addresss by user id
    
    def get(self, request, pk, format=None):
        
        user = self.get_object(pk)

        if user.role == 3:
            provider_user = User.objects.get(id=pk)
            provider_profile = ServiceProvider.objects.get(
                user_service_provider__id=pk)
            provider_address = Address.objects.filter(address_user__id=pk)

            provider_user_serializer = CustomUserSerialiser(provider_user)
            profile_serializer = ServiceProviderSerialiser(provider_profile)
            address_serializer = AddressSerialiser(provider_address, many=True)

            try:
                context = {
                    'user': provider_user_serializer.data,
                    'provider': profile_serializer.data,
                    'address': address_serializer.data
                }
                return Response(context, status=status.HTTP_200_OK)
            except:
                return Response('User not found!!', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('This Is Not Provider user!!', status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):

        provider_user = self.get_object(pk)
        print('provider_user', provider_user)

        # Checking the user is provider or not...
        if provider_user.role == 3:
            # User table data update
            first_name = request.data['first_name']
            middle_name = request.data['middle_name']
            last_name = request.data['last_name']
            phone_number = request.data['phone_number']
            gender = request.data['gender']
            account_status = request.data['account_status']
            online_status = request.data['online_status']
            activity_status = request.data['activity_status']
            payment_to_method = request.data['payment_to_method']
            payment_from_method = request.data['payment_from_method']

            # ServiceProvider table data update
            businees_goal = request.data['businees_goal']
            spent_money_in_business = request.data['spent_money_in_business']
            number_of_employees = request.data['number_of_employees']
            founding_year = request.data['founding_year']
            experience_level = request.data['experience_level']
            company_name = request.data['company_name']
            social_media_link = request.data['social_media_link']
            website_url = request.data['website_url']
            avg_res_time = request.data['avg_res_time']
            avg_rating = request.data['avg_rating']
            lifetime_service_count = request.data['lifetime_service_count']
            positive_review_id = request.data['positive_review_id']
            nagetive_review_id = request.data['nagetive_review_id']

            # Address table data update
            street_address = request.data['street_address']
            apt = request.data['apt']
            zip_code = request.data['zip_code']
            city = request.data['city']
            state = request.data['state']
            country = request.data['country']

            try:
                User.objects.filter(id=pk).update(first_name=first_name,
                                                  middle_name=middle_name, last_name=last_name,
                                                  phone_number=phone_number, gender=gender, account_status=account_status, online_status=online_status, activity_status=activity_status, payment_to_method=payment_to_method, payment_from_method=payment_from_method)

                ServiceProvider.objects.filter(user_service_provider__id=pk).update(businees_goal=businees_goal, spent_money_in_business=spent_money_in_business,
                                                                                    number_of_employees=number_of_employees, founding_year=founding_year, experience_level=experience_level, company_name=company_name,
                                                                                    social_media_link=social_media_link, website_url=website_url, avg_res_time=avg_res_time, avg_rating=avg_rating, lifetime_service_count=lifetime_service_count,
                                                                                    positive_review_id=positive_review_id, nagetive_review_id=nagetive_review_id, user_service_provider_id=pk)

                Address.objects.filter(address_user__id=pk).update(
                    street_address=street_address, apt=apt, zip_code=zip_code, city=city, state=state, country=country)

                return Response(status=status.HTTP_200_OK)

            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('This Is Not Provider User!!', status=status.HTTP_400_BAD_REQUEST)


# Customer User, Customer and Address table data GET, UPDATE and DELETE ---Naznin
class CustomerProfile(APIView):
    """
    Customer Profile Retrieve and Update.
    """
    permission_classes = [IsAuthenticated, CustomerPermission]

    # Getting user id from authenticate user
    def get_object(self, pk):

        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    # Getting Provider information from three table as User, ServiceProvider, Addresss by user id
    
    def get(self, request, pk, format=None):

        user = self.get_object(pk)

        if user.role == 2:
            customer_user = User.objects.get(id=pk)
            customer_profile = Customer.objects.get(user_customer__id=pk)
            customer_address = Address.objects.filter(address_user__id=pk)
            print('customer_address', customer_address)

            customer_user_serializer = CustomUserSerialiser(customer_user)
            profile_serializer = CustomerSerialiser(customer_profile)
            address_serializer = AddressSerialiser(customer_address, many=True)

            try:
                context = {
                    'user': customer_user_serializer.data,
                    'customer': profile_serializer.data,
                    'address': address_serializer.data
                }
                return Response(context, status=status.HTTP_200_OK)
            except:
                return Response('User not found!!', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('This Is Not Customer User!!', status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):

        customer_user = self.get_object(pk)
        print('customer_user', customer_user)

        # Checking the user is customer or not...
        if customer_user.role == 2:
            # User table data update
            first_name = request.data['first_name']
            middle_name = request.data['middle_name']
            last_name = request.data['last_name']
            phone_number = request.data['phone_number']
            gender = request.data['gender']
            account_status = request.data['account_status']
            online_status = request.data['online_status']
            activity_status = request.data['activity_status']
            payment_to_method = request.data['payment_to_method']
            payment_from_method = request.data['payment_from_method']

            # Customer table data update
            avg_rating = request.data['avg_rating']
            lifetime_service_count = request.data['lifetime_service_count']
            positive_review_id = request.data['positive_review_id']
            nagetive_review_id = request.data['nagetive_review_id']

            # # Address table data update
            street_address = request.data['street_address']
            apt = request.data['apt']
            zip_code = request.data['zip_code']
            city = request.data['city']
            state = request.data['state']
            country = request.data['country']

            try:
                User.objects.filter(id=pk).update(first_name=first_name,
                                                  middle_name=middle_name, last_name=last_name,
                                                  phone_number=phone_number, gender=gender, account_status=account_status, online_status=online_status, activity_status=activity_status, payment_to_method=payment_to_method, payment_from_method=payment_from_method)

                Customer.objects.filter(user_customer__id=pk).update(
                    avg_rating=avg_rating, lifetime_service_count=lifetime_service_count, positive_review_id=positive_review_id, nagetive_review_id=nagetive_review_id)

                Address.objects.filter(address_user__id=pk).update(street_address=street_address, apt=apt, zip_code=zip_code,
                                                                   city=city, state=state, country=country, address_user_id=pk)

                return Response(status=status.HTTP_201_CREATED)

            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('This Is Not Customer User!!', status=status.HTTP_400_BAD_REQUEST)



# Service Provider Lists with filtering
class ServicesProviderListView(generics.ListAPIView):
    """
    Service Provider List with filtering all fields of user and locations.
    """
    
    permission_classes = [IsAuthenticated]
    queryset = User.objects.filter(role=3)
    serializer_class = UserListSerialiser
    # pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'first_name', 'middle_name', 'last_name', 'email', 'phone_number',
                        'online_status', 'activity_status', 'account_status',
                        'payment_to_method', 'payment_from_method',
                        'user_address__street_address', 'user_address__zip_code',
                        'user_address__state', 'user_address__city', 'user_address__country']


# Customer Lists with filtering
class CustomerListView(generics.ListAPIView):
    """
    Customer List with filtering all fields of user and locations.
    """
    permission_classes = [IsAuthenticated]
    queryset = User.objects.filter(role=2)
    serializer_class = UserListSerialiser
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'username', 'online_status', 'activity_status', 'account_status',
                        'payment_to_method', 'payment_from_method',
                        'user_address__street_address', 'user_address__zip_code',
                        'user_address__state', 'user_address__city', 'user_address__country']


# Search Service Provider by service category and sub category and location---Naznin
class SearchServicesProviderListView(generics.ListAPIView):
    """
    Search Service Provider by Service Category and Sub Category.
    """
    # permission_classes = [IsAuthenticated]

    queryset = User.objects.filter(role=3)
    serializer_class = SearchServicesProviderSerialiser
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id','username','online_status', 'activity_status','account_status', 
                            'payment_to_method', 'payment_from_method', 
                            'user_address__street_address', 'user_address__zip_code',
                            'user_address__state', 'user_address__city', 'user_address__country',
                            'user_service_provider__businees_goal', 'service_of_user__service_category', 'service_of_user__service_sub_category']
    
    


# Service Provider online status and service status ---Naznin
class GetServiceProviderStatus(APIView):
    """
    Get and Update Service Provider Status.
    """

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    
    
    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        user_status = User.objects.get(id=pk)
        print('online_status', user_status.online_status)

        try:

            context = {
                'username': user_status.username,
                'online_status': user_status.online_status,
                'activity_status': user_status.activity_status,
                'user_status': user_status.account_status

            }
            return Response(context, status=status.HTTP_200_OK)

        except:
            return Response('This user has no service!!', status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        user_object = self.get_object(pk)
        # set partial=True to update a data partially
        serializer = PatchUserStatusSerialiser(
            user_object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


# Customer online status and service status ---Naznin
class GetCustomerStatus(APIView):
    """
    Get and Update Customer Status.
    """

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    
    
    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        user_status = User.objects.get(id=pk)
        print('online_status', user_status.online_status)

        try:

            context = {
                'username': user_status.username,
                'online_status': user_status.online_status,
                'activity_status': user_status.activity_status,
                'account_status': user_status.account_status,

            }
            return Response(context, status=status.HTTP_200_OK)

        except:
            return Response('This user has no service!!', status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        user_object = self.get_object(pk)
        # set partial=True to update a data partially
        serializer = PatchUserStatusSerialiser(
            user_object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


# Patch User Status for changing user status---Naznin
class PatchUserStatus(APIView):

    """
    Patch User Status.
    """

    pagination_class = StandardResultsSetPagination
    
   
    def get_object(self, pk):
        return User.objects.get(pk=pk)

    def patch(self, request, pk):
        user_object = self.get_object(pk)
        # set partial=True to update a data partially
        serializer = UserStatusSerialiser(
            user_object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class pref_provider_Customer_ApiView(APIView):

    """Customer who sign up for a specific service provider.When a Customer Sign Up from a provider home page This list should be updated with that provider id"""
    
    
    permission_classes = [IsAuthenticated]
    
    serializer_class = pref_provider_Customer_Serializer

    
    def post(self, request, *args, **kwargs):
        user_customer = request.data.get('user_customer')
        provider = request.data.get('provider')
        customer_name = request.data.get('customer_name')
        provider_name = request.data.get('provider_name')
        user_add_pre_provider_id = PreProvider.objects.filter(provider=provider, user_customer=user_customer).values_list('id', flat=True)
        print('user_add_pre_provider_id', user_add_pre_provider_id)
        if user_add_pre_provider_id.exists():
            return Response("Already Save in DataBase", status=status.HTTP_200_OK)
        else:
            data = {
            'user_customer': user_customer, 
            'provider': provider, 
            "customer_name" : customer_name, 
            'provider_name' :  provider_name
            }

            serializer = pref_provider_Customer_Serializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class PreProviderListDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):

    """From Customer homepage customer can Delete and Get  preferd provider in his or her account"""

    permission_classes = [IsAuthenticated]
    queryset = PreProvider.objects.all()
    serializer_class = pref_provider_Customer_Serializer
    lookup_field = 'id'
    
    
    def get_queryset(self, *args, **kwargs):
        user_customer = self.request.query_params.get('user_customer')
        print('user_customer', user_customer)
        queryset = PreProvider.objects.all()
        if user_customer is not None:
            queryset = queryset.filter(user_customer=user_customer)
            print('QuerySet', queryset)
        return queryset





class customer_view_service_provider_list(generics.ListAPIView):

    """	A customer can view all his pre providers as a list """

    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated,  CustomerPermission]
    serializer_class = pref_provider_Customer_Serializer
    
   
    def get_queryset(self, *args, **kwargs):
        customerId = self.request.query_params.get('customerId')
        queryset = PreProvider.objects.all()
        if customerId is not None:
            queryset = PreProvider.objects.filter(
                user_customer=customerId)
        return queryset




class service_provider_view_customer_list(generics.ListAPIView):

    """	A service_provider can view all his customer as a list """

    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated, ServiceProviderPermission]
    serializer_class = pref_provider_Customer_Serializer
    
    
    def get_queryset(self, *args, **kwargs):
        provider_id = self.request.query_params.get(
            'provider_id')
        queryset = PreProvider.objects.all()
        if provider_id is not None:
            queryset = PreProvider.objects.filter(
                provider=provider_id)
        return queryset




class Profile_Picture_ViewSet(viewsets.ModelViewSet):
    
    """User Profile Picture Upload"""

    permission_classes = [IsAuthenticated]
    # pagination_class = StandardResultsSetPagination
    queryset = ProfilePicture.objects.all()
    serializer_class = UploadProfilePictureSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)





# Customer  Profile Picture table data GET, UPDATE 
class CustomerProfilePicture(generics.ListAPIView):
    """
    Customer Profile Picture Retrieve .
    """
    permission_classes = [IsAuthenticated, CustomerPermission]
    serializer_class = UploadProfilePictureSerializer
    # pagination_class = StandardResultsSetPagination

    
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        print('user', user_id)
        queryset =  ProfilePicture.objects.all()
        if user_id is not None:
            queryset = queryset.filter(uploaded_user__id=user_id)
        return queryset




# Service Provider  Profile Picture table data GET, UPDATE 
class ServiceProviderProfilePicture(generics.ListAPIView):
    """
    Service  Provider Picture Retrieve.
    """
    permission_classes = [IsAuthenticated, ServiceProviderPermission]
    serializer_class = UploadProfilePictureSerializer
    # pagination_class = StandardResultsSetPagination


    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        print('user', user_id)
        queryset =  ProfilePicture.objects.all()
        if user_id is not None:
            queryset = queryset.filter(uploaded_user__id=user_id)
        return queryset


class Profile_Picture_Create(APIView):

    """ Here User Can Post Image One Time. If image is post and id create second time image can not post and give us error message"""

    permission_classes = [IsAuthenticated]
    serializer_class = UploadProfilePictureSerializer
    
    def post(self, request, *args, **kwargs):
        user_id = self.request.user.id
        print('User Id', user_id)
        profile_picture = request.FILES['profile_picture']
        user_upload_proile_pic_id = ProfilePicture.objects.filter(uploaded_user__id=user_id).values_list('id', flat=True)
        print('user_upload_profile_pic', user_upload_proile_pic_id)
        if user_upload_proile_pic_id.exists():
            return Response("Already Save in DataBase", status=status.HTTP_200_OK)
        else:
            data = {'profile_picture': profile_picture, 'uploaded_user': self.request.user.id}

            serializer = UploadProfilePictureSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class CustomerProfileUpdate(APIView):
    """
    Customer Profile Retrieve and Update.
    """
    permission_classes = [IsAuthenticated, CustomerPermission]

    # Getting user id from authenticate user
    def get_object(self, pk):

        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    # Getting Provider information from three table as User, ServiceProvider, Addresss by user id
    
    def get(self, request, pk, format=None):

        user = self.get_object(pk)

        if user.role == 2:
            customer_user = User.objects.get(id=pk)
           
            customer_user_serializer = CustomUserSerialiser(customer_user)
            

            try:
                context = {
                    'user': customer_user_serializer.data,
                    
                }
                return Response(context, status=status.HTTP_200_OK)
            except:
                return Response('User not found!!', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('This Is Not Customer User!!', status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):

        customer_user = self.get_object(pk)
        print('customer_user', customer_user)

        # Checking the user is customer or not...
        if customer_user.role == 2:
            # User table data update
            first_name = request.data['first_name']
            middle_name = request.data['middle_name']
            last_name = request.data['last_name']
            
            try:
                User.objects.filter(id=pk).update(first_name=first_name,
                                                  middle_name=middle_name, last_name=last_name,
                                                  )

                return Response(status=status.HTTP_201_CREATED)

            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('This Is Not Customer User!!', status=status.HTTP_400_BAD_REQUEST)







class CustomerProfileAddressUpdate(APIView):
    """
    Customer Address Retrieve and Update.
    """
    permission_classes = [IsAuthenticated, CustomerPermission]

    # Getting user id from authenticate user
    def get_object(self, pk):

        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    # Getting Provider information from three table as User, Customer, Addresss by user id
    
    def get(self, request, pk, format=None):

        user = self.get_object(pk)

        if user.role == 2:
            customer_user = User.objects.get(id=pk)
            customer_address = Address.objects.filter(address_user__id=pk)
            print('customer_address', customer_address)

            # customer_user_serializer = CustomUserSerialiser(customer_user)
            address_serializer = AddressSerialiser(customer_address, many=True)

            try:
                context = {
                    # 'user': customer_user_serializer.data,
                    'address': address_serializer.data
                }
                return Response(context, status=status.HTTP_200_OK)
            except:
                return Response('User not found!!', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('This Is Not Customer User!!', status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):

        customer_user = self.get_object(pk)
        print('customer_user', customer_user)

        # Checking the user is customer or not...
        if customer_user.role == 2:
            
            # # Address table data update
            street_address = request.data['street_address']
            apt = request.data['apt']
            zip_code = request.data['zip_code']
            city = request.data['city']
            state = request.data['state']
            country = request.data['country']

            try:
               
                Address.objects.filter(address_user__id=pk).update(street_address=street_address, apt=apt, zip_code=zip_code,
                                                                   city=city, state=state, country=country)

                return Response(status=status.HTTP_200_OK)

            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('This Is Not Customer User!!', status=status.HTTP_400_BAD_REQUEST)



class ProviderProfileAddressUpdate(APIView):
    """
    provider Address Retrieve and Update.
    """
    permission_classes = [IsAuthenticated, ServiceProviderPermission]

    # Getting user id from authenticate user
    def get_object(self, pk):

        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    # Getting Provider information from three table as User, ServiceProvider, Addresss by user id
    
    def get(self, request, pk, format=None):

        user = self.get_object(pk)

        if user.role == 3:
            provider_user = User.objects.get(id=pk)
            provider_address = Address.objects.filter(address_user__id=pk)
            print('provider_address', provider_address)

            address_serializer = AddressSerialiser(provider_address, many=True)

            try:
                context = {
                   
                    'address': address_serializer.data
                }
                return Response(context, status=status.HTTP_200_OK)
            except:
                return Response('User not found!!', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('This Is Not provider User!!', status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):

        provider_user = self.get_object(pk)
        print('provider_user', provider_user)

        # Checking the user is provider or not...
        if provider_user.role == 3:
            
            # # Address table data update
            street_address = request.data['street_address']
            apt = request.data['apt']
            zip_code = request.data['zip_code']
            city = request.data['city']
            state = request.data['state']
            country = request.data['country']

            try:
               
                Address.objects.filter(address_user__id=pk).update(street_address=street_address, apt=apt, zip_code=zip_code,
                                                                   city=city, state=state, country=country)

                return Response(status=status.HTTP_200_OK)

            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('This Is Not provider User!!', status=status.HTTP_400_BAD_REQUEST)




class UserIDWiseAddressZipCodeAPIView(generics.ListAPIView):

    """Get User ID  and see  video calling account token  are here"""

    permission_classes = [IsAuthenticated]
    serializer_class = AddressZipCodeSerialiser

   
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        print('user', user_id)
        queryset = Address.objects.all()
        if user_id is not None:
            queryset = queryset.filter(address_user__id=user_id)
        return queryset







class UserInfo(viewsets.ModelViewSet):
    # User Profile Update in Patch Method 
    """
    Here user update there info if they need . User can change any info 
    """
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = CustomUserSerialiser
    



class search_result_for_provider_info(APIView):
   
    """ This api use when a customer view provider info """

    # Getting user id from authenticate user
    def get_object(self, pk):

        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    # Getting Provider information from three table as User, ServiceProvider, Addresss by user id
    
    def get(self, request, pk, format=None):

        user = self.get_object(pk)

        if user.role == 3:
            provider_user = User.objects.get(id=pk)
            provider_profile = ServiceProvider.objects.get(
                user_service_provider__id=pk)
            provider_address = Address.objects.filter(address_user__id=pk)

            provider_user_serializer = CustomUserSerialiser(provider_user)
            profile_serializer = ServiceProviderSerialiser(provider_profile)
            address_serializer = AddressSerialiser(provider_address, many=True)

            try:
                context = {
                    'user': provider_user_serializer.data,
                    'provider': profile_serializer.data,
                    'address': address_serializer.data
                }
                return Response(context, status=status.HTTP_200_OK)
            except:
                return Response('User not found!!', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('This Is Not Provider user!!', status=status.HTTP_400_BAD_REQUEST)




# Service Provider  Profile Picture table data GET, UPDATE 
class Search_Service_Provider_Profile_Picture(generics.ListAPIView):
    """
    Service  Provider Picture Retrieve. This api use when a user search any service and see service details which provider give this service
    """
    
    serializer_class = UploadProfilePictureSerializer
    # pagination_class = StandardResultsSetPagination


    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        print('user', user_id)
        queryset =  ProfilePicture.objects.all()
        if user_id is not None:
            queryset = queryset.filter(uploaded_user__id=user_id)
        return queryset