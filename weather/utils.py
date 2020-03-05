import requests
from .models import City, CityList
import os
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail


def mail_sender_to_subs():
    api_key = os.environ['OPENWEATHERMAP_API_KEY']
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + api_key

    citylists = CityList.objects.all()
    for citylist in citylists:
        weather_data = []
        context = {}

        if citylist.subscription:
            context = {}
            for city in citylist.cities.all():
                r = requests.get(url.format(city)).json()
                if r['cod'] == 200:
                    city_weather = {
                        'city': r['name'],
                        'temperature': r['main']['temp'],
                        'description': r['weather'][0]['description'],
                        'icon': r['weather'][0]['icon'],
                        'id' : r['id'],
                    }
                    weather_data.append(city_weather)
            context = {
                'username'  : citylist.user.username,
                'weather_data' : weather_data,
            }

            subject = 'Test weather app - Todays Forecast Report'
            html_message = render_to_string('weather/weather_mail.html', context)
            plain_message = strip_tags(html_message)
            recepient = citylist.user.email
            send_mail(subject, plain_message, os.environ['EMAIL_HOST_USER'], [recepient],html_message=html_message)
    return(True)

def send_mail_for_citylists(citylist_id):
    citylists = CityList.objects.filter(id=citylist_id)
    if citylists is None:
        print('CityList Error')
        return False    

    mail_cnt = 0

    api_key = os.environ['OPENWEATHERMAP_API_KEY']
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + api_key

    for citylist in citylists:
        weather_data = []
        context = {}

        if citylist.subscription:
            context = {}
            for city in citylist.cities.all():
                r = requests.get(url.format(city)).json()
                if r['cod'] == 200:
                    city_weather = {
                        'city': r['name'],
                        'temperature': r['main']['temp'],
                        'description': r['weather'][0]['description'],
                        'icon': r['weather'][0]['icon'],
                        'id' : r['id'],
                    }
                    weather_data.append(city_weather)
            context = {
                'username'  : citylist.user.username,
                'weather_data' : weather_data,
            }

            subject = 'Test weather app - Todays Forecast Report'
            html_message = render_to_string('weather/weather_mail.html', context)
            plain_message = strip_tags(html_message)
            recepient = citylist.user.email
            send_mail(subject, plain_message, os.environ['EMAIL_HOST_USER'], [recepient],html_message=html_message)
            mail_cnt = mail_cnt + 1 
    print('Send mail counter:{}'.format(mail_cnt))
    return(True)