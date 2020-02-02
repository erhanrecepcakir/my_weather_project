from django.urls import path

from . import views


app_name = "weather"

urlpatterns = [
    path('', views.weatherhome, name='weatherhome'),
    path('delete/<city_name>/', views.delete_city, name='delete_city'),
    path('extend/<city_name>/', views.extend_city, name='extend_city'),
    path('subscribe/<status>/', views.subscription, name='subscription'),
    path('substest/', views.subscribetest, name='subscribetest'),
    
]