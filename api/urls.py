from django.urls import path
from .views import *



from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'Provider Service',  service)
router.register(r'Service FileUpload',  servicefile)



urlpatterns = [
    
    # service Category create url and service category List url
    path('service_category/',
         ServiceCategoryListCreateAPIView.as_view(), name='category'),

    # service Category update url and Delete url
    path('service_category/update/<id>',
         ServiceCategoryUpdate_Detials_Delete_APIView.as_view(), name='update_delete_details'),

    #  Service Details url
    path('service/Details/<id>',
         ServiceDetailsAPIView.as_view(), name='update_delete_details_service'),

    # Service sub category Create url and List url
    path('service_sub_category/', ServiceSubCategoryListAPIView.as_view(),
         name=' Servic_Sub_Category_List_APIView'),

    # Service sub category Update url and Delete url
    path('service_sub_category/update/<id>',
         ServiceSubCategoryUpdate_Detials_Delete_APIView.as_view(), name='update_delete_details_service_sub_category'),
    path('CategoryWiseSubCategoryAPIView/', CategoryWiseSubCategoryAPIView.as_view(), name='CategoryWiseSubCategoryAPIView'),

    # Service Create Url
    path('provider_service_create/', provider_service_create.as_view(),
         name='provider_service_create'),

    # Service Update url
    path('provider_service_update/<int:service_id>', provider_service_update.as_view(),
         name='provider_service_update_'),

    # Service list url
    path('ServiceListProviderAPIView/', ServiceListProviderAPIView,
         name='ServiceListProviderAPIView'),
    
    # a provider how many service create list url
    path('Service_List_Provider_APIView/', Service_List_Provider_APIView.as_view(), name='Service_List_Provider_APIView'),

    # Service list filter url
    path('serviceListAPIView/', serviceListAPIView.as_view(),
         name='service_List_API_View'),

    # Service Received list
    path('CustomerServiceReceivedList/', CustomerServiceReceivedList.as_view(),
         name='CustomerServiceReceivedList'),

    # Service Received list
    path('ProviderServiceGivenList/', ProviderServiceGivenList.as_view(),
         name=' ProviderServiceGivenList'),

    # service exit list
    path('ServiceExist/', ServiceExist.as_view(), name='ServiceExist'),

    # service received
    path('ServiceReceivedListCreateAPIView/',
         ServiceReceivedListCreateAPIView.as_view(), name='Service_Received_List_Create'),
    
    # service received update and delete url
    path('ServiceReceivedUpdate_Detials_Delete_APIView/<id>',
         ServiceReceivedUpdate_Detials_Delete_APIView.as_view(), name='ServiceReceivedUpdate_Detials_Delete_APIView'),
    
    # for search result in service details
    path('Search_Service_Details/<id>', Search_Service_Details_APIView.as_view(), name='Search_Service_Details'),

    # Violation
    path('addViolationType/', addViolationType.as_view(),
         name='add_Violation_type'),
    path('creatViolation/',  creatViolation.as_view(),
         name='creatViolation'),
    path('getViolationsAPIView/', getViolationsAPIView.as_view(),
         name='getViolationsAPIView'),
    path('creatWarning/', creatWarning.as_view(),
         name='creatWarning'),
    path('getWarningAPIView/',
         getWarningAPIView.as_view(), name='get_warning_api'),
    path('getWarningByViolationID/<int:pk>', getWarningByViolationID.as_view(),
         name='getWarningByViolationID'),
    path('getUserStatus/<id>', getUserStatus, name='getUserStatus1'),
    #     path('get_violations/<id>/', get_violations, name='get_violations'),
    
    # video call token store url
    path('VideoCallingTokenListCreateAPIView/', VideoCallingTokenListCreateAPIView.as_view(), name='VideoCallingTokenListCreateAPIView'),
    
    # video call token get url
    path('UserIDWiseVideoCallingTokenListAPIView/', UserIDWiseVideoCallingTokenListAPIView.as_view(), name='UserIDWiseVideoCallingTokenListAPIView'),
    
    # serach service list url
    path('SearchServiceList/',  SearchServiceList.as_view(), name='SearchServiceList'),
   
    # sevice file url
    path('servicefileGet_APIView/', servicefileGet_APIView.as_view(), name='servicefileGet_APIView'),
    path('servicefileGetUserID_APIView/', servicefileGetUserID_APIView.as_view(), name='servicefileGetUserID_APIView'),

    # service keword suggization url
    path('servicekeywordlistAPI_View/', servicekeywordlistAPI_View.as_view(), name='servicekeywordlistAPI_View'),

    # serach service file url
    path('search_service_file_APIView/', search_service_file_APIView.as_view(), name='search_service_file_APIView'),

    # total service sell or given count url
    path('single/service/total/count/<int:service_id>', single_service_total_count.as_view(), name='single_service_total_count'),
   


    # ----------------------------------------CREATED BY NAZNIN (START)-----------------------------------------
    path("provider_appointment_create/", ProviderAppointmentCreate.as_view(),
         name="provider_appointment_create"),  # Naznin --- provider_appointment_create
    path("ProviderAppointmentGet/", ProviderAppointmentGet.as_view(), name="ProviderAppointmentGet"),

    path("customer_appointment/<int:pk>", CustomerAppointmentCreate.as_view(),
         name="customer_appointment_create"),  # Naznin --- customer_appointment_create

    path("cancel_appointment/<int:pk>", CancelAppointment.as_view(),
         name="cancel_appointment"),  # Naznin --- cancel_appointment

    path("single_provider_appointment_info/<int:provider_id>", GetSingleProviderAppointmentInfo.as_view(),
         name="single_provider_appointment_info"),  # Naznin --- customer_appointment_create

    path("appointment_list/", AppointmentListView.as_view(),
         name="appointment_list"),  # Naznin --- appointment_list

    path("provider_available_list/", DurationWiseAppointmentInfo.as_view(),
         name="provider_available_list"),  # Naznin --- appointment_list


] + router.urls
