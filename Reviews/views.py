from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from . models import *
from .serializer import *
from api.views import StandardResultsSetPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authapp.permissions import CustomerSupportPermission
from rest_framework import filters
from datetime import timedelta, datetime
from rest_framework.decorators import api_view
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.db.models import Avg




class CreateReivew(APIView):

    """This api create new review . user can input service id, receiver id, rating, revicw text . Any register user can  create review like(Customer can submit a review and rating for a provider and Similarly a provider can a review and rating for a customer)"""

    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        data = {
            'receiver_id': request.data.get('receiver_id'),
            'service_id': request.data.get('service_id'),
            'rating': request.data.get('rating'),
            'review_text': request.data.get('review_text'),
            'reviewer_id': self.request.user.id
        }

        serializer = CreateReivewSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetReview(generics.ListAPIView):

    """This api user can see how many review other user can given.receiver_id could a customer_id or a provider_id.The review will show rating and response_date orderlist"""

    permission_classes = [IsAuthenticated]
    serializer_class = CreateReivewSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        receiver_id = self.request.user.id
        orderbyList = ['response_date', 'rating']
        if receiver_id is not None:
            queryset = Review.objects.filter(
                receiver_id=receiver_id).order_by(*orderbyList)
        return queryset


class UpdateReview(APIView):

    """Customer Support Admin or SuperAdmin can access this api.Customer Support Admin or SuperAdmin update user review by review id"""
  
    permission_classes = [IsAuthenticated, CustomerSupportPermission]
    pagination_class = StandardResultsSetPagination
    
    
    def put(self, request, id):
        service_id = request.data['service_id']
        rating = request.data['rating']
        review_text = request.data['review_text']
        response_text = request.data['response_text']
        response_date = request.data['response_date']
        review_status = request.data['review_status']
        approved_by = request.data['approved_by']
        approval_date = request.data['approval_date']
        try:
            Review.objects.filter(id=id).update(service_id=service_id, rating=rating, review_text=review_text,
                                                response_text=response_text, response_date=response_date, review_status=review_status, approval_date=approval_date, approved_by=approved_by)
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ViewUpdateReview(generics.ListAPIView):

    """Customer Support Admin or SuperAdmin can access this api.Customer Support Admin or SuperAdmin filter review status like published or unpublished. Last 30 days data will return """

    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated, CustomerSupportPermission]
    queryset = Review.objects.all()
    serializer_class = UpdateReivewSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ['review_status', 'receiver_id__id', 'reviewer_id__id']

    def get_queryset(self):
        from_date = datetime.now() - timedelta(days=30)
        queryset = Review.objects.filter(response_date__gt=from_date)
        return queryset



@api_view(["GET"])
def calulate_average_rating(request, id):

    """ This api returns how many reviews a user recived. Total review count and average of review rating"""

    average_rating = Review.objects.all().filter(receiver_id=id).aggregate(Avg('rating'))
    review_count = Review.objects.filter(receiver_id=id).count()
    context = {
        'average_rating' : average_rating,
        'review_count' : review_count,
    }
    return JsonResponse(context)