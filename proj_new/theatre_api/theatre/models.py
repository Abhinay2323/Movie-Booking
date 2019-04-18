from django.db import models

class movie(models.Model):
    movie_name = models.CharField(max_length=100)
    movie_genre = models.CharField(max_length=100)
    movie_release_date = models.DateField(null=False)
    movie_age_rating = models.CharField(max_length=100)
    movie_duration_mins = models.CharField(max_length=100)
    movie_language = models.CharField(max_length=100)
    movie_actors = models.CharField(max_length=100)
    movie_directors = models.CharField(max_length=100)
    movie_producers = models.CharField(max_length=100)
    movie_writers = models.CharField(max_length=100)
    imdb_movie_rating = models.CharField(max_length=50)
    movie_description = models.TextField()
    movie_trailer_link = models.CharField(max_length=100)
    movie_poster_1 = models.ImageField(upload_to='poster_1',blank=True)
    movie_poster_2 = models.ImageField(upload_to='poster_2', blank=True)

class theatre(models.Model):
    theatre_name = models.CharField(max_length=50)
    adressline1 = models.CharField(max_length=50)
    adressline2 = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)
    screen_no = models.CharField(max_length=5)
    seat_string = models.TextField()
    theatre_rating = models.CharField(max_length=50)
    now_playing = models.ForeignKey(movie, on_delete=models.CASCADE,related_name='now_playing')
    up_coming = models.ForeignKey(movie, on_delete=models.CASCADE,related_name='up_coming')
    theatre_merchant_id = models.CharField(max_length=50)

class ticket_price_and_time(models.Model):
    theatre_id = models.ForeignKey(theatre, on_delete=models.CASCADE)
    show_timings = models.TimeField(null=False)
    date = models.DateField(null=False)
    seat_class = models.CharField(max_length=50)
    price = models.CharField(max_length=100)

class booked_tickets(models.Model):
    ticket_seat_no = models.TextField()
    movie_details = models.ForeignKey(ticket_price_and_time, on_delete=models.CASCADE)
    ticket_book_from = models.CharField(max_length=50)
    ticket_booking_website = models.CharField(max_length=100)
    ticket_booking_tranc_id = models.CharField(max_length=100)
    ticket_booking_username = models.CharField(max_length=100)

class ticket_booking_website_details(models.Model):
    merchant_id=models.CharField(max_length=100,primary_key=True)
    ticket_booking_website = models.CharField(max_length=100)


from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

