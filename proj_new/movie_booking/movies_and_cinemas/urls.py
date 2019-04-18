from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from movies_and_cinemas import views
urlpatterns = [
      path('city/', views.select_city, name='select-city'),
      #path('city/<str:city>/', views.city, name='city-name'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)