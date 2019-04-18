from django.contrib import admin
from .models import *
admin.site.register(theatre)
admin.site.register(movie)
admin.site.register(ticket_price_and_time)
admin.site.register(booked_tickets)
admin.site.register(ticket_booking_website_details)
