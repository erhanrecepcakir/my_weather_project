import requests
from .models import City, CityList
import os
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail


def get_city_weather_data_from_online(city):
	api_key = os.environ['OPENWEATHERMAP_API_KEY']
	url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + api_key
	city_weather = {}
	r = requests.get(url.format(city)).json()
	if r['cod'] == 200:
		city_weather = {
			'city': r['name'],
			'temperature': r['main']['temp'],
			'description': r['weather'][0]['description'],
			'icon': r['weather'][0]['icon'],
			'id' : r['id'],
		}
	else:
		err_msg = 'City can not be found!'
	print('My City Weather:{}'.format(city_weather))
	return city_weather 

def mail_sender_to_all_subscribers():
	citylists = CityList.objects.all()
	for citylist in citylists:
		weather_data = []
		context = {}
		if citylist.subscription:
			for city in citylist.cities.all():
				city_weather = get_city_weather_data_from_online(city)
				if city_weather:
					weather_data.append(city_weather)
			if len(weather_data):
				#weather_data includes at least one city data
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

def send_mail_for_citylist(citylist_id):
	citylist = CityList.objects.get(id=citylist_id)
	if citylist is None:
		print('CityList Error')
		return False
	weather_data = []
	context = {}
	print('My City List: {}'.format(citylist.user))

	if citylist.subscription:
		for city in citylist.cities.all():
			city_weather = get_city_weather_data_from_online(city)
			if city_weather:
				weather_data.append(city_weather)
		print('My Weather Data 2: {}'.format(weather_data))
		if len(weather_data):
			#weather_data includes at least one city data
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