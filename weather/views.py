import requests
from django.shortcuts import render, redirect
from .models import City, CityList
from .forms import CityForm, SubscribeForm
from my_weather_project.settings import EMAIL_HOST_USER, CELERY_TIMEZONE
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
import os, json, datetime
from .tasks import send_mail_func, configurable_periodic_mail_sender
from django_celery_beat.models import CrontabSchedule, PeriodicTask, PeriodicTasks


@login_required(login_url = "user:login")
def weatherhome(request):
    api_key = os.environ['OPENWEATHERMAP_API_KEY']
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + api_key

    err_msg = ''
    message = ''
    message_class = ''
    crontab_schedule = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if 'name' in request.POST:
            if form.is_valid():
                new_city = form.cleaned_data['name']
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    usercitylists = CityList.objects.filter(user = request.user)
                    if len(usercitylists):
                        usercitylist = usercitylists[0]
                        form.save()
                        usercitylist.cities.add(City.objects.get(name=new_city))
                    else:
                        usercitylist = CityList(user = request.user)
                        usercitylist.save()
                        form.save()
                        usercitylist.cities.add(City.objects.get(name=new_city))
                else:
                    err_msg = 'City can not be found!'
            else:
                err_msg = 'City already exists in the database!'

            if err_msg:
                message = err_msg
                message_class = 'is-danger'
            else:
                message = 'city added succesfully'
                message_class = 'is-success'

    form = CityForm()
    subsform = SubscribeForm()

    usercitylists = CityList.objects.filter(user = request.user)
    if len(usercitylists):
        cities = usercitylists[0].cities.all()
        subscription = usercitylists[0].subscription
        if usercitylists[0].periodictask is not None:
            crontab_schedule = {
                'hour': usercitylists[0].periodictask.crontab.hour,
                'minute': usercitylists[0].periodictask.crontab.minute,
            }        
    else:
        cities = []
        subscription = False

    weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()

        city_weather = {
            'city': r['name'],
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)

    #print(weather_data)

    context = {
        'weather_data'      : weather_data,
        'form'              : form,
        'subsform'          : subsform,
        'message'           : message,
        'message_class'     : message_class,
        'subscription'      : subscription,
        'crontab_schedule'  : crontab_schedule,
    }

    #return render(request, 'weather/weather.html', context)
    return render(request, 'weather/weather.html', context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete(myuser=request.user)
    return redirect('weather:weatherhome')

def extend_city(request, city_name):
    api_key = os.environ['OPENWEATHERMAP_API_KEY']
    url = 'https://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid=' + api_key

    err_msg = ''
    message = ''
    message_class = ''

    r = requests.get(url.format(city_name)).json()

    weather_data = []

    if r['cod'] == '200':
        for list_index in range(r['cnt']):
            city_weather = {
            'date'          : r['list'][list_index]['dt_txt'],
            'temperature'   : r['list'][list_index]['main']['temp'],
            'description'   : r['list'][list_index]['weather'][0]['description'],
            'icon'          : r['list'][list_index]['weather'][0]['icon'],
            }
            weather_data.append(city_weather)
    else:
        err_msg = 'City information can not be found!'

    context = {
        'city_name' : city_name,
        'weather_data': weather_data,
        'message' : err_msg,
        'message_class' : message_class,
    }


    return render(request, 'weather/extended_weather.html', context)


def subscription(request, status):
    if 'task_time' in request.POST:
        subsform = SubscribeForm(request.POST)
        if subsform.is_valid():
            print(subsform.cleaned_data['task_time'])
            planned_time = subsform.cleaned_data['task_time']
            hour = planned_time.hour
            minute = planned_time.minute
        else:
            return redirect('weather:weatherhome')

    citylists = CityList.objects.filter(user=request.user)

    if len(citylists):
        citylists[0].subscription = status

        if status == 'True':
            schedule, _ = CrontabSchedule.objects.get_or_create(
                minute=minute,
                hour=hour,
                day_of_week='*',
                day_of_month='*',
                month_of_year='*',
                timezone=CELERY_TIMEZONE,
            )
            citylists[0].periodictask = PeriodicTask.objects.create(
                crontab=schedule,
                name=('Mail Sender to {}'.format(citylists[0].user.username)),
                task='configurable_periodic_mail_sender',
                args=json.dumps([citylists[0].id,]),
            )
        else:
            if citylists[0].periodictask is not None:
                citylists[0].periodictask.delete()
                citylists[0].periodictask = None
        citylists[0].save()

    return redirect('weather:weatherhome')

def subscribetest(request):
    api_key = os.environ['OPENWEATHERMAP_API_KEY']
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + api_key

    err_msg = ''
    message = ''
    message_class = ''

    if request.user.is_superuser:
        citylists = CityList.objects.all()
    else:
        citylists = CityList.objects.filter(user=request.user)

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
            # print("UserName: {} UserMail: {}".format(citylist.user.username,citylist.user.email))
            # print(context)

            subject = 'Test weather app - Todays Forecast Report'
            html_message = render_to_string('weather/weather_mail.html', context)
            plain_message = strip_tags(html_message)
            #recepient = citylist.user.username,citylist.user.email
            recepient = citylist.user.email
            #send_mail(subject, plain_message, EMAIL_HOST_USER, [recepient], html_message=html_message)
            send_mail_func.delay(
                    {
                    'subject':subject,
                    'plain_message':plain_message, 
                    'email_host_user':EMAIL_HOST_USER,
                    'recepient_list':[recepient],
                    'html_message':html_message,
                }
            )

            #return render(request, 'weather/weather_mail.html', context)

    #return redirect('weather:weatherhome')
    return redirect('index')
