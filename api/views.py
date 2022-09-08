from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse
from rest_framework.views import APIView
from rest_framework import generics, mixins, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import pagination
from rest_framework import filters
from rest_framework import status

from datetime import timedelta
from django_filters.rest_framework import DjangoFilterBackend
import time



from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView

from .models import *
from .serializers import *


from authapp.models import *
from authapp.serializers import *

from datetime import timedelta, datetime
from django.http import Http404
from authapp.permissions import ServiceProviderPermission, CustomerPermission
from rest_framework.parsers import JSONParser, FileUploadParser, MultiPartParser, FormParser







"""This section work Naznin"""


class StandardResultsSetPagination(pagination.PageNumberPagination):

    """
    Naznin: This is for pagination. Here we can change page_size number as we want to see.
    """
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 1000






# Finding day by giving appointment date .....Naznin
def find_day(date):
    
    date = str(date)
    day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').weekday()
    return day_name[day]
    

# Creating appointment by serviceprovider .....Naznin 
class ProviderAppointmentCreate(APIView):

    """
    Provider Appointment schedule create.
    """

    # user should authenticated user
    permission_classes = [IsAuthenticated, ServiceProviderPermission]
    serializer_class = ProviderAvailableSerialiser
    pagination_class = StandardResultsSetPagination
    
    # Creating appointment by serviceprovider post function
    def post(self, request):

        # getting day name by user's selecting fields
        select_day_name_list = {
            'Saturday': request.data.get('saturday'),
            'Sunday': request.data.get('sunday'),
            'Monday': request.data.get('monday'),
            'Tuesday': request.data.get('tuesday'),
            'Wednesday': request.data.get('wednesday'),
            'Thursday': request.data.get('thursday'),
            'Friday': request.data.get('friday'),
            'All': request.data.get('all')
        }

        print('select_day_name_list', select_day_name_list)

        # getting fields value from ProviderAvailableSerialiser's fields
        day_start_time = request.POST.get('day_start_time')
        day_end_time = request.POST.get('day_end_time')
        duration = request.POST.get('duration')
        appointment_start_date = request.POST.get('appointment_start_date')
        appointment_end_date = request.POST.get('appointment_end_date')
        given_appointment_start_date = datetime.strptime(appointment_start_date, '%Y-%m-%d')
        given_appointment_end_date = datetime.strptime(appointment_end_date, '%Y-%m-%d')
        
        # getting loggedin service provider... 
        appointment_service_provider = User.objects.filter(role=3)
        print('appointment_service_provider', appointment_service_provider)

        ## Checking that the requested ser is provider or not....
        for provider_user in appointment_service_provider:
            if provider_user == request.user:

                if Service.objects.filter(service_user__id=provider_user.id).exists() == False:
                    msg = 'Please create a service first'
                else:
                    # getting loggedin service provider's service which service he select...
                    provider_service = Service.objects.filter(service_user__id=provider_user.id)
                    print('provider_service', provider_service)

                print('provider_user.id', provider_user.id)

                print('request.user', request.user)

                
        
                # checking appointment ending is elder then appointment start date...
                while given_appointment_start_date <= given_appointment_end_date:

                    print('given_appointment_start_date', given_appointment_start_date)
                    
                    # Finding day name..
                    day_name = find_day(given_appointment_start_date)
                    print('day_name', day_name)

                    
                    my_date = given_appointment_start_date
                    print('-----------------my_date-------------', my_date)
                    count = 0
                    given_day_start_time = datetime.strptime(day_start_time, '%H:%M')
                    given_day_end_time = datetime.strptime(day_end_time, '%H:%M')
                    
                    is_appointment_exits_start_date = Appointment.objects.filter(appointment_date=given_appointment_start_date).exists()
                    is_appointment_exits_start_time = Appointment.objects.filter(start_time=given_day_start_time).exists()
                    print('is_appointment_exits_date', is_appointment_exits_start_date)
                    print('is_appointment_exits_time', is_appointment_exits_start_time)

                    ## Checking that the given date time is smaller then the given end date time....
                    if given_day_start_time >= given_day_end_time:
                        raise ValidationError("start time must be smaller than end time")
                    
                    # if given_appointment_start_date == given_appointment_end_date:
                    #     if (is_appointment_exits_start_date and is_appointment_exits_start_time) == True:
                    #         msg = 'You have already created for this days and this time'
                    #         break
                        

                    if select_day_name_list['All'] == 'true':
                        while select_day_name_list['All'] == 'true':
                            while given_day_start_time < given_day_end_time:
                                if count == 0:
                                    if (is_appointment_exits_start_date and is_appointment_exits_start_time) == True:
                                        msg = 'You have already created for this days and this time'
                                        break
                                    else:
                                        for service_of_provider in provider_service:
                                            Appointment.objects.create(appointment_provider_id=provider_user.id, appointment_service_id=service_of_provider.id, appointment_type='instant_call', appointment_date=my_date, start_time=str(
                                                datetime.strptime(str(given_day_start_time), '%Y-%m-%d %H:%M:%S').time()), end_time=str(
                                                datetime.strptime(str(given_day_start_time + timedelta(minutes=int(duration))), '%Y-%m-%d %H:%M:%S').time()), duration=duration, status='open', created_by_id=provider_user.id, day_name=day_name)
                                else:
                                    if (is_appointment_exits_start_date and is_appointment_exits_start_time) == True:
                                        msg = 'You have already created for this days and this time'
                                        break
                                    else:
                                        for service_of_provider in provider_service:
                                            Appointment.objects.create(appointment_provider_id=provider_user.id, appointment_service_id=service_of_provider.id, appointment_type='instant_call', appointment_date=my_date, start_time=str(
                                                datetime.strptime(str(given_day_start_time), '%Y-%m-%d %H:%M:%S').time()), end_time=str(
                                                datetime.strptime(str(given_day_end_time), '%Y-%m-%d %H:%M:%S').time()), duration=duration, status='open', created_by_id=provider_user.id, day_name=day_name)

                                given_day_start_time = given_day_start_time + timedelta(minutes=int(duration))
                                count += 1
                            msg = 'appointment created'
                            break
                        given_appointment_start_date = given_appointment_start_date + timedelta(days=1)
                    else:
                        if given_appointment_start_date < given_appointment_end_date:
                            while given_appointment_start_date < given_appointment_end_date:
                                if select_day_name_list[day_name] == 'true':
                                    while select_day_name_list[day_name] == 'true':
                                        while given_day_start_time < given_day_end_time:
                                            if count == 0:
                                                if (is_appointment_exits_start_date and is_appointment_exits_start_time) == True:
                                                    msg = 'You have already created for this days and this time'
                                                    break
                                                else:
                                                    for service_of_provider in provider_service:
                                                        Appointment.objects.create(appointment_provider_id=provider_user.id, appointment_service_id=service_of_provider.id, appointment_type='instant_call', appointment_date=my_date, start_time=str(
                                                            datetime.strptime(str(given_day_start_time), '%Y-%m-%d %H:%M:%S').time()), end_time=str(
                                                            datetime.strptime(str(given_day_start_time + timedelta(minutes=int(duration))), '%Y-%m-%d %H:%M:%S').time()), duration=duration, status='open', created_by_id=provider_user.id, day_name=day_name)
                                            else:
                                                if (is_appointment_exits_start_date and is_appointment_exits_start_time) == True:
                                                    msg = 'You have already created for this days and this time'
                                                    break
                                                else:
                                                    for service_of_provider in provider_service:
                                                        Appointment.objects.create(appointment_provider_id=provider_user.id, appointment_service_id=service_of_provider.id, appointment_type='instant_call', appointment_date=my_date, start_time=str(
                                                            datetime.strptime(str(given_day_start_time), '%Y-%m-%d %H:%M:%S').time()), end_time=str(
                                                            datetime.strptime(str(given_day_end_time), '%Y-%m-%d %H:%M:%S').time()), duration=duration, status='open', created_by_id=provider_user.id, day_name=day_name)

                                            given_day_start_time = given_day_start_time + timedelta(minutes=int(duration))
                                            count += 1
                                        msg = 'appointment created'
                                        break
                                    break
                                else:
                                    break  
                            given_appointment_start_date = given_appointment_start_date + timedelta(days=1)
                            # msg = 'appointment created'
                        else:
                            if given_appointment_start_date == given_appointment_end_date:
                                if select_day_name_list[day_name] == 'true':
                                    while select_day_name_list[day_name] == 'true':
                                        while given_day_start_time < given_day_end_time:
                                            if count == 0:
                                                if (is_appointment_exits_start_date and is_appointment_exits_start_time) == True:
                                                    msg = 'You have already created for this days and this time'
                                                    break
                                                else:
                                                    for service_of_provider in provider_service:
                                                        Appointment.objects.create(appointment_provider_id=provider_user.id, appointment_service_id=service_of_provider.id, appointment_type='instant_call', appointment_date=my_date, start_time=str(
                                                            datetime.strptime(str(given_day_start_time), '%Y-%m-%d %H:%M:%S').time()), end_time=str(
                                                            datetime.strptime(str(given_day_start_time + timedelta(minutes=int(duration))), '%Y-%m-%d %H:%M:%S').time()), duration=duration, status='open', created_by_id=provider_user.id, day_name=day_name)
                                            else:
                                                if (is_appointment_exits_start_date and is_appointment_exits_start_time) == True:
                                                    msg = 'You have already created for this days and this time'
                                                    break
                                                else:
                                                    for service_of_provider in provider_service:
                                                        Appointment.objects.create(appointment_provider_id=provider_user.id, appointment_service_id=service_of_provider.id, appointment_type='instant_call', appointment_date=my_date, start_time=str(
                                                            datetime.strptime(str(given_day_start_time), '%Y-%m-%d %H:%M:%S').time()), end_time=str(
                                                            datetime.strptime(str(given_day_end_time), '%Y-%m-%d %H:%M:%S').time()), duration=duration, status='open', created_by_id=provider_user.id, day_name=day_name)

                                            given_day_start_time = given_day_start_time + timedelta(minutes=int(duration))
                                            count += 1
                                        # msg = 'appointment created'
                                        break
                                    break
                                else:
                                    # msg = 'appointment created'
                                    break
                            else:
                                # msg = 'appointment created'
                                break
                            
                return Response({"msg": msg}, status=status.HTTP_201_CREATED)




class ProviderAppointmentGet(generics.ListAPIView):
    
    """
    This api provider can check how many appointment he/she create. provider can filter service name, appointment date, duration , day name, start time, end time, appointment type
    """
    
    permission_classes = [IsAuthenticated, ServiceProviderPermission]
    serializer_class = AppointmentSerialiser
    filter_backends = (filters.SearchFilter,)
    search_fields =  ['appointment_service__service_name', 'appointment_provider__id', 'appointment_date', 'day_name', 'duration', 'start_time', 'end_time', 'appointment_type']
    
    
    def get_queryset(self):
        provider_id = self.request.query_params.get('provider_id')
        queryset = Appointment.objects.all()
        if provider_id is not None:
            queryset = queryset.filter(appointment_provider__id=provider_id)
        return queryset
   





# Customer Booked Appointment ---Naznin
class CustomerAppointmentCreate(APIView):
    """
    Customer Booked Appointment.
    """

    permission_classes = [IsAuthenticated, CustomerPermission]
    serializer_class = CustomerBookAppointmentSerialiser

    def get_object(self, pk):
        try:
            return Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            raise Http404

    
    def patch(self, request, pk, format=None):

        appointment = self.get_object(pk)
        appointment_type = request.data['appointment_type']
        user_customer = User.objects.get(id=request.user.id)
        customer = Customer.objects.get(user_customer_id=user_customer)

        appointment_data = {
            'appointment_type': appointment_type,
            'appointment_customer': customer.id,
            'status': 'booked'
        }

        serializer = CustomerBookAppointmentSerialiser(
            appointment, data=appointment_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Cancel Appointment ---Naznin
class CancelAppointment(APIView):
    """
    Cancel Appointment.
    """

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            raise Http404
    
       
    def patch(self, request, pk, format=None):

        appointment = self.get_object(pk)

        appointment_data = {

            'canceled_by': request.user.id
        }

        serializer = CancelAppointmentSerialiser(
            appointment, data=appointment_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Appointment Lists with filtering
class AppointmentListView(generics.ListAPIView):
    """
    Appointment Lists with filtering.
    """

    permission_classes = [IsAuthenticated]

    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerialiser
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = '__all__'


# Single privider appointment info .....Naznin
class DurationWiseAppointmentInfo(generics.GenericAPIView, mixins.ListModelMixin):

    """
    Get Single provider appointment.
    """

    # user should authenticated user
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentSerialiser
    # pagination_class = DurationWiseAppointmentInfoSerialiser

    def get(self, request):
        return self.list(request)

    def get_queryset(self):
        
        start_date = self.request.query_params.get('appointment_start_date')
        end_date = self.request.query_params.get('appointment_end_date')

        print('start_date', start_date)
        print('end_date', end_date)
        queryset = Appointment.objects.all()
        if id and start_date and end_date is not None:
            queryset = queryset.filter(appointment__appointment_date__date__range=[
                                       start_date, end_date]).order_by('appointment__appointment_date')
            print(queryset)
        return queryset




# Single privider appointment info .....Naznin 
class GetSingleProviderAppointmentInfo(APIView):

    """
    Get Single provider appointment.
    """

    # user should authenticated user
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentSerialiser
    pagination_class = StandardResultsSetPagination

    def get(self, request, provider_id):
        
        try:
            queryset = Appointment.objects.filter(appointment_provider_id = provider_id)
            serializer = AppointmentSerialiser(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response('No Appointment Info found!!', status=status.HTTP_400_BAD_REQUEST)






"""This section work Tasim"""


# Created By Tasim
class ServiceCategoryListCreateAPIView(generics.ListCreateAPIView):

    ''' Creating Service Category and List of  all Service Category '''

    permission_classes = [IsAuthenticated]
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCatSerialiser
    # pagination_class = StandardResultsSetPagination

    filter_backends = (filters.SearchFilter,)
    search_fields =  ['category_name', 'id']


# Created By Tasim
class ServiceCategoryUpdate_Detials_Delete_APIView(generics.RetrieveUpdateDestroyAPIView):

    ''' Update, Delete and Details Service Category  API View '''

    permission_classes = [IsAuthenticated]
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCatSerialiser
    # pagination_class = StandardResultsSetPagination
    lookup_field = 'id'




class ServiceSubCategoryListAPIView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin):

    """Create Service Sub Category"""

    permission_classes = [IsAuthenticated]
    queryset = ServiceSubCategory.objects.all()
    serializer_class = ServiceSubCategorySerializer
    # pagination_class = StandardResultsSetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields =  ['service_sub_category_name', 'id', 'service_sub_category_keyword']
    
    
    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class ServiceSubCategoryUpdate_Detials_Delete_APIView(generics.RetrieveUpdateDestroyAPIView):

    ''' Update, Delete and Details Service Sub Category  API View '''

    permission_classes = [IsAuthenticated]
    queryset = ServiceSubCategory.objects.all()
    serializer_class = ServiceSubCategorySerializer
    # pagination_class = StandardResultsSetPagination
    lookup_field = 'id'

    filter_backends = (filters.SearchFilter,)



class CategoryWiseSubCategoryAPIView(generics.ListAPIView):

    """Get Category ID  and see how many sub category are here"""

    permission_classes = [IsAuthenticated]
    serializer_class = ServiceSubCategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields =  ['service_sub_category_name', 'id', 'service_sub_category_keyword']
    
    
    def get_queryset(self):
        category_id = self.request.query_params.get('category_id')
        queryset = ServiceSubCategory.objects.all()
        if category_id is not None:
            queryset = queryset.filter(category__id=category_id)
        return queryset



class provider_service_create(APIView):

    """add permission to check if user is authenticated"""

    permission_classes = [IsAuthenticated, ServiceProviderPermission]
    serializer_class = ServiceSerialiser
    

    """ Create """
    def post(self, request, *args, **kwargs):
        '''
        Create the Service with given service data
        '''
        data = {
            'service_user': request.user.id,
            'service_category': request.data.get('service_category'),
            'service_sub_category': request.data.get('service_sub_category'),
            'service_keyword_list': request.data.get('service_keyword_list'),
            'service_name': request.data.get('service_name'),
            'service_description': request.data.get('service_description'),
            'service_experiance_year': request.data.get('service_experiance_year'),
            'rate_apt_video_cons': request.data.get('rate_apt_video_cons'),
            'rate_inst_video_cons': request.data.get('rate_inst_video_cons'),
            'rate_inhouse_cons': request.data.get('rate_inhouse_cons'),
            'rate_promotion': request.data.get('rate_promotion'),
            'service_status': request.data.get('service_status'),
            'service_visibility': request.data.get('service_visibility'),
            'service_zip_code' : request.data.get('service_zip_code')
        }
        serializer = ServiceSerialiser(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class provider_service_update(APIView):

    """add permission to check if user is authenticated """

    permission_classes = [IsAuthenticated, ServiceProviderPermission]
    serializer_class = ServiceSerialiser
   

    def get_object(self, service_id, user_id):
        '''
        Helper method to get the object with given service_id, and user_id
        '''
        try:
            return Service.objects.get(id=service_id, service_user=user_id)
        except Service.DoesNotExist:
            return None

    # 4. Update
    def put(self, request, service_id, *args, **kwargs):
        '''
        Updates the Service item with given service_id if exists
        '''
        service_instance = self.get_object(service_id, request.user.id)
        if not service_instance:
            return Response(
                {"res": "Object with service id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'service_user': request.user.id,
            'service_category': request.data.get('service_category'),
            'service_sub_category': request.data.get('service_sub_category'),
            'service_keyword_list': request.data.get('service_keyword_list'),
            'service_name': request.data.get('service_name'),
            'service_description': request.data.get('service_description'),
            'service_experiance_year': request.data.get('service_experiance_year'),
            'rate_apt_video_cons': request.data.get('rate_apt_video_cons'),
            'rate_inst_video_cons': request.data.get('rate_inst_video_cons'),
            'rate_inhouse_cons': request.data.get('rate_inhouse_cons'),
            'rate_promotion': request.data.get('rate_promotion')
            
        }
        serializer = ServiceSerialiser(
            instance=service_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def ServiceListProviderAPIView(request):
    """ Here provider can see how many service he/she created. If request service provider ID match in service table  then service provider can see all of services he/she created """

    if request.method == 'GET':
        service_user = User.objects.filter(role=3)
        for provider_user in service_user:
            if provider_user == request.user:
                service_provider = request.user
                print('Service Provider', service_provider)
                provider_service_list = Service.objects.filter(
                    service_user=service_provider)
                print('Provider_Service_List', provider_service_list)

                for x in provider_service_list:
                    print('Service', x.service_name)

                Service_serializer = ServiceSerialiser(
                    provider_service_list, many=True).data
                return Response(Service_serializer, status=status.HTTP_200_OK)
                


class serviceListAPIView(generics.ListAPIView):

    """This api return request service_provider service list and service_provider can filter category,subcategory and provider experience_level"""

    permission_classes = [IsAuthenticated]
    serializer_class = ServiceSerialiser
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ['service_category__category_name',
                     'service_sub_category__service_sub_category_name', 'service_experiance_year']
    
    def get_queryset(self):
        service_user = User.objects.filter(role=3)
        for provider_user in service_user:
            if provider_user == self.request.user:
                service_provider = self.request.user
                queryset = Service.objects.filter(
                    service_user=service_provider)
        return queryset


class ServiceDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):

    '''Creating Service Details API View . Insert service ID and get Service Details. Here we can see Service Details by using service id '''

    permission_classes = [IsAuthenticated]
    queryset = Service.objects.all()
    serializer_class = ServiceSerialiser
    pagination_class = StandardResultsSetPagination
    lookup_field = 'id'
    filter_backends = (filters.SearchFilter,)
    
    def get_queryset(self, *args, **kwargs):
        user_id = self.request.query_params.get('user_id')
        print('user_id', user_id)
        queryset = Service.objects.all()
        if user_id is not None:
            queryset = queryset.filter(service_user__id=user_id)
            print('QuerySet', queryset)
        return queryset


 # created By Tasim


class ServiceReceivedListCreateAPIView(generics.ListCreateAPIView):

    """ Create Service Received Information  and List of  all Service Received Information """

    permission_classes = [IsAuthenticated]
    queryset = ServiceReceived.objects.all()
    serializer_class = ServiceReceivedSerializer

    pagination_class = StandardResultsSetPagination

    filter_backends = (filters.SearchFilter,)


class ServiceReceivedUpdate_Detials_Delete_APIView(generics.RetrieveUpdateDestroyAPIView):

    ''' Update, Delete and Details Service Received  API View '''

    permission_classes = [IsAuthenticated]
    queryset = ServiceReceived.objects.all()
    serializer_class = ServiceReceivedSerializer
    pagination_class = StandardResultsSetPagination
    lookup_field = 'id'

    filter_backends = (filters.SearchFilter,)


class addViolationType(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin):

    """Add Violation Type violation_name ,violation_types, message"""

    permission_classes = [IsAuthenticated]
    queryset = ViolationType.objects.all()
    serializer_class = addViolationTypeSerializer
     
    
    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class creatViolation(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin):

    """Create Violation information"""

    permission_classes = [IsAuthenticated]
    queryset = Violation.objects.all()
    serializer_class = ViolationSerializer
    
    
    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class getViolationsAPIView(APIView):

    """Get Violation information userID/customerID/providerID and violation_duration"""

    permission_classes = [IsAuthenticated]
    serializer = ViolationSerializer()
    filter_backends = (filters.SearchFilter,)
    search_fields = ['violation_duration']
    
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id is not None:
            queryset = Violation.objects.filter(violate_user=user_id)
        return queryset


# @api_view(["GET"])
# @permission_classes((IsAuthenticated, ))
# def get_violations(request, id):
#     if request.method == "GET":
#         duration_month = request.GET.get('duration_month')
#         violation = Violation.objects.filter(
#             violate_user=id,  violation_start_date__month=duration_month)
#         serializer = ViolationSerializer(
#             violation, many=True)

#         return Response(serializer.data)


class creatWarning(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin):

    """Create Warning information"""

    permission_classes = [IsAuthenticated]

    queryset = WarningModel.objects.all()
    serializer_class = WarningSerializer
    
    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class getWarningAPIView(generics.GenericAPIView, mixins.ListModelMixin):

    """Get Warning information userID/customerID/providerID and num_of_warning"""

    permission_classes = [IsAuthenticated]
    serializer_class = WarningSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ['num_of_warning', 'user_id__id']
    
    def get_queryset(self):
        warning_user_id = self.request.query_params.get('warning_user_id')
        queryset = WarningModel.objects.all()
        if warning_user_id is not None:
            queryset = queryset.filter(user_id=warning_user_id)
        return queryset


class getWarningByViolationID(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):

    """Get Warning information userID/customerID/providerID/violationID"""

    permission_classes = [IsAuthenticated]
    serializer_class = WarningSerializer
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        warning_user_id = self.request.query_params.get('warning_user_id')
        violation_id = self.request.query_params.get('violation_id')
        queryset = WarningModel.objects.all()
        if warning_user_id is not None:
            queryset = queryset.filter(
                user_id=warning_user_id, violation__id=violation_id)
        return queryset

    def get(self, request, pk):
        return self.retrieve(request, pk)


@api_view(["GET"])
@permission_classes((IsAuthenticated, ))
def getUserStatus(request, id):
    """Creating the lifetime violation_count, warning_count and suspension_count of the user"""

    from_date = datetime.now() - timedelta(days=30)
    print('from date', from_date)

    violation_count = Violation.objects.filter(
        violate_user=id, violation_start_date__gt=from_date).count()
    warning_count = WarningModel.objects.filter(
        user_id=id, warning_date__gt=from_date).count()
    suspension_count = Suspension.objects.filter(
        user_id=id, suspension_start_date__gt=from_date).count()

    status = User.objects.filter(id=id, joining_date__gt=from_date).get()

    print('Current', status.activity_status)
    activity_status = status.activity_status

    context = {
        'Total Violation': violation_count,
        'Total Warning': warning_count,
        'Total Suspension': suspension_count,
        'Activity Status':  activity_status,
    }

    return JsonResponse(context)


class CustomerServiceReceivedList(generics.ListAPIView):

    """This api returns customer service received list . Customer  can see how many service he/she takes and which provider got this service """

    permission_classes = [IsAuthenticated]
    serializer_class = ServiceReceivedSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ['duration', 'service__id', 'service__service_name']
    
    def get_queryset(self):
        customer = Customer.objects.get(user_customer=self.request.user.id)
        queryset = ServiceReceived.objects.all()
        queryset = queryset.filter(service_customer=customer)
        return queryset


class ProviderServiceGivenList(generics.ListAPIView):

    """This api returns provider service given list . Provider  can see how many service he/she given and which customer took this service """

    permission_classes = [IsAuthenticated]
    serializer_class = ServiceReceivedSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ['duration', 'service__id', 'service__service_name']
    
    def get_queryset(self):
        service_provider = ServiceProvider.objects.get(
            user_service_provider=self.request.user.id)
        queryset = ServiceReceived.objects.all()
        queryset = queryset.filter(service_provider=service_provider)
        return queryset


class ServiceExist(generics.ListAPIView):

    '''This api provider can  see Service already created or not '''

    permission_classes = [IsAuthenticated]
    serializer_class = ServiceSerialiser
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ['service_category__category_name', 'service_sub_category__service_sub_category_name',
                     'service_keyword_list']
    
    def get_queryset(self):
        service_user = User.objects.filter(role=3)
        for provider_user in service_user:
            if provider_user == self.request.user:
                service_provider = self.request.user
                category = ServiceCategory.objects.all()
                sub_category = ServiceSubCategory.objects.all()
                queryset = Service.objects.all()
                if service_user is not None:
                    queryset = Service.objects.filter(
                        service_user=service_provider, service_category__in=category, service_sub_category__in=sub_category)
                return queryset




# Created By Tasim
class VideoCallingTokenListCreateAPIView(APIView):

    ''' Creating Video Calling Token and List of  all Video Calling token '''

    serializer_class = videoCallingSerializer
    
    def post(self, request, format=None):
        serializer = videoCallingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class UserIDWiseVideoCallingTokenListAPIView(generics.ListAPIView):

    """Get User ID  and see  video calling account token  are here"""

    permission_classes = [IsAuthenticated]
    serializer_class = videoCallingSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        queryset = videoCallingBearerTokenStore.objects.all()
        if user_id is not None:
            queryset = queryset.filter(user_video_call_account__id=user_id)
        return queryset



class SearchServiceList(generics.ListAPIView):

    """This api returns provider service given list . Customer  can see which service he/she take and which provider gives this service """

    # permission_classes = [IsAuthenticated]
    serializer_class =  search_serviceSerialiser
    # pagination_class = StandardResultsSetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ['service_name', 'service_keyword_list', 'service_experiance_year', 'service_category__category_name', 'service_sub_category__service_sub_category_name', 'service_sub_category__service_sub_category_keyword']
    
    
    def get_queryset(self, *args,  **kwargs):
        zip_code = self.request.query_params.get('zip_code')
        print('Zip Code', zip_code)
        queryset = Service.objects.all()
        serializer_class =  search_serviceSerialiser(queryset, many=True).data
        if zip_code is not None:
            queryset = queryset.filter(service_zip_code=zip_code)
            print('QuerySet', queryset)
        return queryset


class Service_List_Provider_APIView(generics.ListAPIView):
    
    """Here Service Provider see how many service he/she created.Register Service Provider User ID match in Service Table and provider see service table data """
    
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceSerialiser
    # pagination_class = StandardResultsSetPagination
    
    
    def get_queryset(self, *args, **kwargs):
        user_id = self.request.query_params.get('user_id')
        print('user_id', user_id)
        queryset = Service.objects.all()
        if user_id is not None:
            queryset = queryset.filter(service_user__id=user_id)
            
        return queryset



class service(viewsets.ModelViewSet):

    """This api crud operation  in service."""

    permission_classes = [IsAuthenticated, ServiceProviderPermission]
    queryset = Service.objects.all()
    serializer_class = ServiceSerialiser
    





class servicefile(viewsets.ModelViewSet):
    
    """ This api create service file get service file info, update service file and delete service file"""

    permission_classes = [IsAuthenticated, ServiceProviderPermission]
    queryset = ServiceFile.objects.all()
    serializer_class = ServiceFileSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)





class servicefileGet_APIView(generics.ListAPIView):
    
    """ This api returns service file info result. api match user id and return identified user and specefic service, service image and service certifiacte. Customer can easily view provider service image and service sertificate """
    
    serializer_class =  ServiceFileSerializer
    # pagination_class = StandardResultsSetPagination
    
    
    def get_queryset(self, *args, **kwargs):
        user_id = self.request.query_params.get('user_id')
        print('user_id', user_id)
        service_id = self.request.query_params.get('service_id')
        queryset = ServiceFile.objects.all()
        if user_id and service_id is not None:
            queryset = queryset.filter(service_user__id=user_id, service__id=service_id)
           
        return queryset




class servicefileGetUserID_APIView(generics.ListAPIView):
    
    """ This api returns service file info result. api match user id and return identified user service image and service certifiacte. Customer can easily view provider service image and service sertificate """
    
    permission_classes = [IsAuthenticated]
    serializer_class =  ServiceFileSerializer
    # pagination_class = StandardResultsSetPagination
    
    
    def get_queryset(self, *args, **kwargs):
        user_id = self.request.query_params.get('user_id')
        print('user_id', user_id)
        queryset = ServiceFile.objects.all()
        if user_id is not None:
            queryset = queryset.filter(service_user__id=user_id)
           
        return queryset


class servicekeywordlistAPI_View(APIView):

    """ This api return service name and service keyword list. It is used for a user search anything in search bar and we suggisted some data that user get best match data """
    
    def get(self, request, format=None):
        services = Service.objects.all()
        service_keyword_list = []
        for keyword in services:
            print("keyword tag list====", keyword.service_keyword_list)
            for value in keyword.service_keyword_list:
                service_keyword_list.append(value)
        print('KeywordList', service_keyword_list)

        for name in services:
            service_keyword_list.append(name.service_name)

        context = {
            'service_keyword_list': service_keyword_list,
        }
        return JsonResponse(context)





class Search_Service_Details_APIView(generics.RetrieveAPIView):

    '''Creating Service Details API View . Insert service ID and get Service Details. Here we can see Service Details by using service id '''

    
    queryset = Service.objects.all()
    serializer_class = ServiceSerialiser
    pagination_class = StandardResultsSetPagination
    lookup_field = 'id'
    filter_backends = (filters.SearchFilter,)
    
    
    def get_queryset(self, *args, **kwargs):
        user_id = self.request.query_params.get('user_id')
        print('user_id', user_id)
        queryset = Service.objects.all()
        if user_id is not None:
            queryset = queryset.filter(service_user__id=user_id)
            print('QuerySet', queryset)
        return queryset



class search_service_file_APIView(generics.ListAPIView):

    """ This api use when a user search any service and search result found any service we will show service image , service name etc. api returns service file info result. api match user id and return identified user service image """
    
    serializer_class =  ServiceFileSerializer
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self, *args, **kwargs):
        queryset = ServiceFile.objects.all()
        return queryset


class single_service_total_count(APIView):
    
    """ This api returns a service provider how many service sold in customer. This information comes from service recived table. In service received table we have this info a service provider how many service provide"""

    def get(self, request, service_id, format=None):
        total_service_count = ServiceReceived.objects.filter(service=service_id).count()
        context = {
            'total_service_count': total_service_count,
        }
        return JsonResponse(context)