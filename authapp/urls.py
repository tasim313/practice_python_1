from django.urls import path
from .views import *




from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'profile_picture',  Profile_Picture_ViewSet)
router.register(r'user_info',  UserInfo)



urlpatterns = [
    
    # provider profile info url
    path("provider_profile/<pk>", ServiceProviderProfile.as_view(),
         name="provider_profile"),  # Naznin --- Service Provider Profile update url

    # provider address update url      
    path('Provider/AddressUpdate/<pk>', ProviderProfileAddressUpdate.as_view(), name="ProviderProfileAddressUpdate"),
    
    # customer profile info url
    path("customer_profile/<pk>", CustomerProfile.as_view(),
         name="customer_profile"),  # Naznin --- Customer Profile update url
    
    # customer profile update url
    path("CustomerProfileUpdate/<pk>", CustomerProfileUpdate.as_view(), name='CustomerProfileUpdate'),
   
    # customer address update url
    path("CustomerProfileAddressUpdate/<pk>", CustomerProfileAddressUpdate.as_view(), name="CustomerProfileAddressUpdate"),

    
    #  service provider list url
    path("service_provider_list/", ServicesProviderListView.as_view(),
         name="service_provider_list"),  # Naznin --- Service Provider List url
    
    # customer list url
    path("customer_list/", CustomerListView.as_view(),
         name="customer_list"),  # Naznin --- Customer List url
    
    # provider status url
    path("provider_status/<pk>", GetServiceProviderStatus.as_view(),
         name="get_provider_status"),  # Naznin --- Service Provider Status url

    # customer status url
    path("customer_status/<pk>", GetCustomerStatus.as_view(),
         name="get_customer_status"),  # Naznin --- Customer status List url
   
    # patch account status url
    path("patch_account_status/<pk>", PatchUserStatus.as_view(),
         name="patch_account_status"),  # Naznin --- patch user status url
    
    # search provider url
    path("search_provider/", SearchServicesProviderListView.as_view(),
         name="search_provider"),  # Naznin --- search_provider_by_cat url
    
    # search result for provider info url
    path('search_result_for_provider_info/<pk>', search_result_for_provider_info.as_view(), name='search_result_for_provider_info'),
    
    # search provider profile picture url
    path('Search_Service_Provider_Profile_Picture/', Search_Service_Provider_Profile_Picture.as_view(), name='Search_Service_Provider_Profile_Picture'),
    
    # pre provider customer url
    path('pref_provider_Customer_ApiView/', pref_provider_Customer_ApiView.as_view(), name='pref_provider_Customer_ApiView'),

    # customer view pre provider list url
    path('customer_view_service_provider_list/',
         customer_view_service_provider_list.as_view(), name='service_provider_view_customer'),
    
    # pre provider view customer list 
    path('service_provider_view_customer_list/',service_provider_view_customer_list.as_view(), name='service_provider_view_customer'),
    
    # pre provider update delete url
    path('PreProviderListDetailsAPIView/<id>', PreProviderListDetailsAPIView.as_view(), name='PreProviderListDetailsAPIView'),

    # customer profile picture url
    path('CustomerProfilePicture/', CustomerProfilePicture.as_view(), name='CustomerProfilePicture'),

    # service provider profile picture url
    path('ServiceProviderProfilePicture/', ServiceProviderProfilePicture.as_view(), name='ServiceProviderProfilePicture'),

    # user profile image upload url
    path('user_profile_img/',  Profile_Picture_Create.as_view(), name='Profile_Picture_Create'),

    # user id wise address zip code url
    path('UserIDWiseAddressZipCodeAPIView/', UserIDWiseAddressZipCodeAPIView.as_view(), name='UserIDWiseAddressZipCodeAPIView'),
    
   

] + router.urls
