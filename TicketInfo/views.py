from django.shortcuts import render
from .models import *
from . serializer import *
from api.views import StandardResultsSetPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import generics
from authapp.permissions import CustomerSupportPermission



class CreateTicket(APIView):

    """User Can Create Ticket. Customer or Provider can create ticket"""

    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        data = {
            'creator_id': request.user.id,
            'title': request.data.get('title'),
            'describtion': request.data.get('describtion'),
            'summery': request.data.get('summery'),
            'category': request.data.get('category'),
        }

        serializer = CreateTicketSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTickets(generics.ListAPIView):

    """User can see ticket status. Data will sort by creation_date and status"""

    permission_classes = [IsAuthenticated]
    serializer_class = GetTicketStatusSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user_id = self.request.user.id
        orderbyList = ['creation_date', 'status']
        if user_id is not None:
            queryset = Ticket.objects.filter(
                creator_id=user_id).order_by(*orderbyList)
        return queryset


class UpdateTicket(APIView):

    """Customer Suport Admin or Admin Can Update User Ticket Info"""

    permission_classes = [IsAuthenticated, CustomerSupportPermission]
    pagination_class = StandardResultsSetPagination
    
   
    def put(self, request, id):
        title = request.data['title']
        describtion = request.data['describtion']
        summery = request.data['summery']
        category = request.data['category']
        update_date = request.data['update_date']
        ticket_status = request.data['ticket_status']
        closing_date = request.data['closing_date']
        try:
            Ticket.objects.filter(id=id).update(title=title, describtion=describtion, summery=summery,
                                                category=category, update_date=update_date, ticket_status=ticket_status, closing_date=closing_date)
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class getTicketStatus(generics.ListAPIView):

    """ This api returns ticket status """

    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    serializer_class = TicketStatusSerializer

    def get_queryset(self, *args, **kwargs):
        ticket_id = self.request.query_params.get('ticket_id')
        queryset = Ticket.objects.all()
        if ticket_id is not None:
            queryset = Ticket.objects.filter(
                id=ticket_id)
        return queryset
