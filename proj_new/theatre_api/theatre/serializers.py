from rest_framework import serializers
from .models import *
from django.core.files import File
import base64


class movieSerializer(serializers.ModelSerializer):
    movie_poster_1 = serializers.SerializerMethodField()
    movie_poster_2= serializers.SerializerMethodField()
    class Meta:
        model = movie
        fields=['movie_name','movie_genre','movie_release_date','movie_age_rating','movie_duration_mins','movie_language','movie_actors','movie_directors','movie_producers','movie_writers','imdb_movie_rating','movie_description','movie_trailer_link','movie_poster_1','movie_poster_2']
        read_only_fields=('movie_name','movie_genre','movie_release_date','movie_age_rating','movie_duration_mins','movie_language','movie_actors','movie_directors','movie_producers','movie_writers','imdb_movie_rating','movie_description','movie_trailer_link','movie_poster_1','movie_poster_2')

    def get_movie_poster_1(self, obj):
        f = open(obj.movie_poster_1.path, 'rb')
        image = File(f)
        data = base64.encodestring(image.read())
        f.close()
        return data
    def get_movie_poster_2(self, obj):
        f = open(obj.movie_poster_2.path, 'rb')
        image = File(f)
        data = base64.encodestring(image.read())
        f.close()
        return data

class theatreSerializer(serializers.ModelSerializer):
    now_playing = movieSerializer()
    up_coming = movieSerializer()
    class Meta:
        model = theatre
        exclude = ('theatre_merchant_id',)
        read_only_fields=('theatre_name','adressline1','adressline2','city','pincode','state','screen_no','seat_string','theatre_rating','now_playing','up_coming',)


class ticketSerializer(serializers.ModelSerializer):
    theatre_id = theatreSerializer()

    class Meta:
        model = ticket_price_and_time
        fields=['show_timings','date','theatre_id','seat_class','price']
        read_only_fields=('show_timings','date','theatre_id','seat_class','price')

class bookedticketSerializer(serializers.ModelSerializer):
    movie_details=ticketSerializer()
    class Meta:
        model = booked_tickets
        fields=['ticket_seat_no','movie_details','ticket_book_from','ticket_booking_website','ticket_booking_tranc_id','ticket_booking_username']
        write_only_fields=('ticket_book_from','ticket_booking_website','ticket_booking_tranc_id','ticket_booking_username')
