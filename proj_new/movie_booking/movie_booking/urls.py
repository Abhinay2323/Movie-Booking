
from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('movies_and_cinemas.urls')),
    path('', include('registration.urls')),
]