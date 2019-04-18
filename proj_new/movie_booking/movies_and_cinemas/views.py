from django.shortcuts import render
from django.http import HttpResponse
from collections import OrderedDict
import requests,json
from .models import *
from threading import Thread
import time,datetime
import base64
#------------------------------------------------------------------------------------------------------------------------
"""
def city(request,city):

    theatre_city = theatre.objects.filter(city=city)
    movies=movie.objects.all()
    movie_list=[];unique_list=[];movies_city=[];
    for i in theatre_city:
        movie_list.append(i.now_playing.movie_name);
    for x in movie_list:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    for i in unique_list:
        m=movie.objects.filter(movie_name=i)
        movies_city.append(m)
    print(movies_city);
    context = {'t_list_city':theatre_city,'movies_city':movies_city,'movies':movies}
    return render(request,"movies_and_cinemas/city_movies.html", context)
"""


def select_city(request):
    city_name=theatre.objects.order_by('city').values('city').distinct()
    cities=[]
    for i in range(len(city_name)):
        cities.append(city_name[i]['city'])
    return render(request,"movies_and_cinemas/city.html",{'cities':cities})


#------------------------------------------------------------------------------------------------------------------------


def book_movie(request):

    theatre_=theatre.objects.filter(theatre_name='lakshmi complex')[0]#this will be function argument
    date='2019-03-08'#this will be function argument
    showtimings='12:00:00'#this will be function argument

    url = 'http://127.0.0.1:8000/api/bookedticket'
    r = requests.get(url, headers={'Authorization': 'Token 51f39e2ea9001c26cdf14ac514c6acbba7d38f67'})
    r = json.loads(r.text)

    m=[]
    for d in r:
        n={}
        for key, value in d.items():
            n[key]=value
        m.append(n)
    print(m)
    seats_booked_string=''
    for i in m:
        if (i['movie_details']['theatre_id']['id'] == theatre_.__dict__['id'] and i['movie_details'][
            'show_timings'] == showtimings and i['movie_details']['date'] == date):
            seats_booked_string+=i['ticket_seat_no']

    seat_string=theatre_.seat_string

    seats_booked=seats_booked_string.split(',')
    seats_booked.remove('')
    seats=seat_string.split(',')
    seats.remove('')

    for i in range(len(seats_booked)):
        seats_booked[i] = seats_booked[i].split('_')
    for i in range(len(seats)):
        seats[i] = seats[i].split('_')

    seats_booked_dict=OrderedDict()
    seats_dict=OrderedDict()

    for seat in seats_booked:
        try:
            seats_booked_dict[seat[0]].append([seat[1],seat[2]])
        except:
            seats_booked_dict[seat[0]]=[[seat[1],seat[2]],]

    for seat in seats:
        try:
            seats_dict[seat[0]].append([seat[1],seat[2]])
        except:
            seats_dict[seat[0]]=[[seat[1],seat[2]],]

    seats_booked = OrderedDict()
    seats = OrderedDict()
    for section,seat in seats_booked_dict.items():
        seats_booked[section]={}
        for each_seat in seat:
            try:
                seats_booked[section][each_seat[0]].append(each_seat[1])
            except:
                seats_booked[section][each_seat[0]]=[each_seat[1],]

    for section,seat in seats_dict.items():
        seats[section]={}
        for each_seat in seat:
            try:
                seats[section][each_seat[0]].append(each_seat[1])
            except:
                seats[section][each_seat[0]]=[each_seat[1],]

    print(seats,seats_booked)
    return render(request,'movies_and_cinemas/book_movie_2.html',{
        'seats_booked' : seats_booked,
        'seats' : seats,
    })


#------------------------------------------------------------------------------------------------------------------------


def update_tables():
    while True:
        updated=False
        url = 'http://127.0.0.1:8000/api/'
        try:
            movie_req=requests.get(url+'movie', headers={'Authorization': 'Token 51f39e2ea9001c26cdf14ac514c6acbba7d38f67'})
            theatre_req=requests.get(url+'theatre', headers={'Authorization': 'Token 51f39e2ea9001c26cdf14ac514c6acbba7d38f67'})
            ticket_req=requests.get(url+'ticket', headers={'Authorization': 'Token 51f39e2ea9001c26cdf14ac514c6acbba7d38f67'})
        except:
            movie_req = None
            theatre_req = None
            ticket_req = None

        if movie_req is not None and theatre_req is not None and ticket_req is not None:
            if movie_req.ok==True and theatre_req.ok==True and ticket_req.ok==True :
                movie.objects.all().delete()
                theatre.objects.all().delete()
                ticket_price_and_time.objects.all().delete()
                movie_req=json.loads(movie_req.text)
                theatre_req=json.loads(theatre_req.text)
                ticket_req=json.loads(ticket_req.text)
                for d in movie_req:
                    movie_post_1=base64.b64decode(d['movie_poster_1'])
                    movie_post_2=base64.b64decode(d['movie_poster_2'])
                    movie_name=d['movie_name'].replace(" ","")
                    filename1 = 'movies_and_cinemas/media/poster_1/'+movie_name+'movie_poster_1.jpg'  # I assume you have a way of picking unique filenames
                    with open(filename1, 'wb') as f:
                        f.write(movie_post_1)
                    filename2 = 'movies_and_cinemas/media/poster_2/'+movie_name+'movie_poster_2.jpg'  # I assume you have a way of picking unique filenames
                    filename2.replace(" ","")
                    with open(filename2, 'wb') as f:
                        f.write(movie_post_2)
                        
                    m = movie(movie_name=d['movie_name'], movie_genre=d['movie_genre'], movie_release_date=d['movie_release_date'],
                              movie_age_rating=d['movie_age_rating'],
                              movie_duration_mins=d['movie_duration_mins'], movie_language=d['movie_language'], movie_actors=d['movie_actors'],
                              movie_directors=d['movie_directors'], movie_producers=d['movie_producers'],
                              movie_writers=d['movie_writers'], imdb_movie_rating=d['imdb_movie_rating'], movie_description=d['movie_description'],
                              movie_trailer_link=d['movie_trailer_link'],
                              movie_poster_1='poster_1/'+movie_name+'movie_poster_1.jpg',
                              movie_poster_2='poster_2/'+movie_name+'movie_poster_2.jpg')
                    m.save()
                for d in theatre_req:
                        t = theatre(theatre_name=d['theatre_name'], adressline1=d['adressline1'],
                                    adressline2=d['adressline2'], city=d['city'], state=d['state'], pincode=d['pincode'],
                                    screen_no=d['screen_no'], seat_string=d['seat_string'],
                                    theatre_rating=d['theatre_rating'], now_playing=movie.objects.filter(movie_name=d['now_playing']['movie_name'], movie_genre=d['now_playing']['movie_genre'], movie_release_date=d['now_playing']['movie_release_date'],
                              movie_age_rating=d['now_playing']['movie_age_rating'],
                              movie_duration_mins=d['now_playing']['movie_duration_mins'], movie_language=d['now_playing']['movie_language'], movie_actors=d['now_playing']['movie_actors'],
                              movie_directors=d['now_playing']['movie_directors'], movie_producers=d['now_playing']['movie_producers'],
                              movie_writers=d['now_playing']['movie_writers'], imdb_movie_rating=d['now_playing']['imdb_movie_rating'], movie_description=d['now_playing']['movie_description'],
                              movie_trailer_link=d['now_playing']['movie_trailer_link'])[0],
                                    up_coming=movie.objects.filter(movie_name=d['up_coming']['movie_name'], movie_genre=d['up_coming']['movie_genre'], movie_release_date=d['up_coming']['movie_release_date'],
                              movie_age_rating=d['up_coming']['movie_age_rating'],
                              movie_duration_mins=d['up_coming']['movie_duration_mins'], movie_language=d['up_coming']['movie_language'], movie_actors=d['up_coming']['movie_actors'],
                              movie_directors=d['up_coming']['movie_directors'], movie_producers=d['up_coming']['movie_producers'],
                              movie_writers=d['up_coming']['movie_writers'], imdb_movie_rating=d['up_coming']['imdb_movie_rating'], movie_description=d['up_coming']['movie_description'],
                              movie_trailer_link=d['up_coming']['movie_trailer_link'])[0])
                        t.save()
                for d in ticket_req:
                            tic = ticket_price_and_time(theatre_id=theatre.objects.filter(theatre_name=d['theatre_id']['theatre_name'], adressline1=d['theatre_id']['adressline1'],
                                    adressline2=d['theatre_id']['adressline2'], city=d['theatre_id']['city'], state=d['theatre_id']['state'], pincode=d['theatre_id']['pincode'],
                                    screen_no=d['theatre_id']['screen_no'])[0],show_timings=d['show_timings'],date=d['date'],seat_class=d['seat_class'],price=d['price'])
                            tic.save()
                            updated=True
                print('updated')
            else:
                print('not updated due to data not found')
        else:
            print('not updated due to server not found')
        naive = updat.objects.all().order_by('-last_update')[0].last_update.replace(tzinfo=None)
        time_difference= datetime.datetime.now()-naive
        if(divmod(time_difference.total_seconds(), 60)[0]>1440):
            time.sleep(86400)
        else:
            time.sleep(3600)

thread=Thread(target=update_tables)
thread.start()
