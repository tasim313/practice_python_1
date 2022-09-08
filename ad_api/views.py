from django.shortcuts import render
from .models import *
from api.views import StandardResultsSetPagination
from authapp.models import *
from .Serializer import *
from rest_framework import viewsets
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from utill import image_upload, video_upload
from operator import and_, or_
from functools import reduce
from django.db.models import Q
from rest_framework.parsers import MultiPartParser, FormParser





# Create your views here.


class AdApiView(generics.ListCreateAPIView):

    """  User can Create Ad.  user also see how many ad he/she created """

    permission_classes = [IsAuthenticated]
    serializer_class = AD_Serializer

    def get_queryset(self):
        ad_user = self.request.user.id
        if ad_user is not None:
            queryset = queryset.filter(user_id=ad_user)
        return queryset


class Ad_By_Tag(generics.ListAPIView):

    """Any user can visit this Api.There are no need to registered . User Input keyword matched by the  model field ad_tag_list and the api gives us best possible match data."""

    pagination_class = StandardResultsSetPagination
    serializer_class = AD_Serializer

    def get_queryset(self, *args, **kwargs):
        user_tag_insert = self.request.query_params.get('user_tag_insert')
        queryset = ad.objects.all()
        if user_tag_insert is not None:
            queryset = ad.objects.filter(
                ad_tag_list__icontains=user_tag_insert)
        return queryset


class AD_Interest(generics.ListAPIView):

    """Here we can see user ad interest by user id and also filter ad_tag_list, entry_date. """

    permission_classes = [IsAuthenticated]
    serializer_class = AdInterestSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ['ad_tag_list', 'entry_date']

    def get_queryset(self, *args, **kwargs):
        user_id = self.request.query_params.get('user_id')
        queryset = UserAdInterest.objects.all()
        if user_id is not None:
            queryset = UserAdInterest.objects.filter(user_id=user_id)
        return queryset


class DeleteAdInterest(generics.RetrieveUpdateDestroyAPIView):

    """Here we can Delete user ad interest data by user id . lookup_field[id] identify individual ad_interest data and query_params.get('user_id') filter user id and gives ad_interest user data"""

    permission_classes = [IsAuthenticated]
    serializer_class = AdInterestSerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        user_id = self.request.query_params.get('user_id')
        queryset = UserAdInterest.objects.all()
        if user_id is not None:
            queryset = UserAdInterest.objects.filter(user_id=user_id)
        return queryset


class Ad_Interest_Create(APIView):

    """AdInterest enries are created and saved when a logged-in customer or provider seach for specific service.Data will save in ad_tag_list in  UserAdInterest Table"""

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_id = self.request.user.id
        ad_tag_list = request.data.get('ad_tag_list')
        ad_interest_ad_tag_list = UserAdInterest.objects.filter(
            user_id=user_id, ad_tag_list=ad_tag_list)
        if ad_interest_ad_tag_list.exists():
            return Response("Already Save in DataBase", status=status.HTTP_200_OK)
        else:
            data = {'ad_tag_list': ad_tag_list, 'user_id': user_id}

            serializer = AdInterestSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes((IsAuthenticated, ))
def get_ad_by_user_id(request, id):
    
    """registered users ad interest table ad_tag_list and ad table ad_tag_list data match then return ad data set from ad table"""

    if request.method == 'GET':
        user_ad_interest = UserAdInterest.objects.filter(user_id=id)
        print('user_ad_interest', user_ad_interest)
        ad_tag_list = []
        for ad_interest in (user_ad_interest):
            print("AD Interest tag list====", ad_interest.ad_tag_list)
            for i in ad_interest.ad_tag_list:
                print("I ==============", i)
                ad_tag_list.append(i)
        print('Ad Tag List==============', ad_tag_list)

        try:
            user_ad_tag = ad.objects.filter(
                reduce(or_, [Q(ad_tag_list__icontains=k) for k in ad_tag_list]))

            serializer = GetADSerializer(user_ad_tag, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class user_adimage_upload(APIView):

    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser,)
    serializer_class = UploadImageADMediaSerializer

    
    def post(self, request, *args, **kwargs):
        '''
        Create image data in request user. Request user can upload image . It will save Media folder in AD_Image subfolder
        '''
        data = {
            'image': request.data.get('image'),
            'user_id': request.user.id
        }
        serializer = UploadImageADMediaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class user_advideo_upload(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = UploadVideoADMediaSerializer

    def post(self, request, *args, **kwargs):
        '''
         Create video data in request user. Request user can upload video . It will save Media folder in AD_video subfolder
        '''
        data = {
            'video': request.data.get('video'),
            'user_id': request.user.id
        }
        serializer = UploadVideoADMediaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class upload_Ad_Media(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Link_Serializer
    
    def post(self, request, *args, **kwargs):
        link_type = request.data.get('link_type')
        if link_type == 'IMAGE_TYPE':
            user_id = request.user.id
            link_name = request.data.get('link_name')
            description = request.data.get('description')
            link_url = user_adimage_upload()
            data = {
                'link_name': link_name,
                'description': description,
                'link_type': link_type,
                'link_url': link_url,
                'user_id': user_id
            }
            serializer = Link_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif link_type == 'VIDEO_TYPE':
            user_id = request.user.id
            link_name = request.data.get('link_name')
            description = request.data.get('description')
            link_url = user_advideo_upload()
            data = {
                'link_name': link_name,
                'description': description,
                'link_type': link_type,
                'link_url': link_url,
                'user_id': user_id
            }
            serializer = Link_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((IsAuthenticated, ))
def User_image_Link_Create(request, user_id, image):
    if request.method == 'POST':
        pass
