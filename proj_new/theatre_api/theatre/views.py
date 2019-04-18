from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from .models import *
from .serializers import *
import json
#from rest_framework.permissions import IsAuthenticated

class theatre_data(APIView):
    #permission_classes = (IsAuthenticated,)

    def get(self,request):
        theatres=theatre.objects.all()
        serializer=theatreSerializer(theatres,many=True)
        return Response(serializer.data)



class movie_data(APIView):

    def get(self, request):
        movies = movie.objects.all()
        serializer = movieSerializer(movies, many=True)
        #print('hello')
        #print(serializer.data.__dict__['serializer'][0].)
        return Response(serializer.data)

class ticket_data(APIView):

    def get(self, request):
        tickets = ticket_price_and_time.objects.all()
        serializer = ticketSerializer(tickets, many=True)
        return Response(serializer.data)


class booked_ticket_data(APIView):

    def get(self, request):
        booked_ticket = booked_tickets.objects.all()
        serializer = bookedticketSerializer(booked_ticket, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = bookedticketSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
