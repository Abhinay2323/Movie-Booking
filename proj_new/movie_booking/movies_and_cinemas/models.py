from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals

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
    now_playing = models.ForeignKey(movie, on_delete=models.SET_NULL,related_name='now_playing', null=True)
    up_coming = models.ForeignKey(movie, on_delete=models.SET_NULL,related_name='up_coming',null=True)

class ticket_price_and_time(models.Model):
    theatre_id = models.ForeignKey(theatre, on_delete=models.CASCADE)
    show_timings = models.TimeField(null=False)
    date = models.DateField(null=False)
    seat_class = models.CharField(max_length=50)
    price = models.CharField(max_length=100)


class booking_history(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    movie_name = models.CharField(max_length=100)
    movie_release_date = models.DateField(null=False)
    movie_language = models.CharField(max_length=100)
    theatre_name = models.CharField(max_length=50)
    adressline1 = models.CharField(max_length=50)
    adressline2 = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)
    screen_no = models.CharField(max_length=5)
    show_timings = models.TimeField(null=False)
    show_date = models.DateField(null=False)
    seat_no= models.CharField(max_length=50)
    price= models.CharField(max_length=100)
    date_and_time_of_booking= models.DateTimeField(null=False)

class updat(models.Model):
    last_update=models.DateTimeField(null=False)


create_trigger= """    
    CREATE TRIGGER on_update_tables 
    AFTER INSERT ON movies_and_cinemas_ticket_price_and_time
    FOR EACH ROW 
    BEGIN
       INSERT INTO movies_and_cinemas_updat(last_update)
          VALUES (CURRENT_TIMESTAMP());
    END
"""


from django.db import connection
cursor = connection.cursor()
#cursor.execute(create_trigger)


