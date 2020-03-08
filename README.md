# Forecast Report with DJANGO

Gets forecast report and sends in an email to subscribers mail addresses at scheduled time. <br />

Before run the application, please export below virtual environment definitions:<br />

1- OpenWeather API Key:<br />
Get an account from https://openweathermap.org/api <br />
Export your API key to virtual environment as **OPENWEATHERMAP_API_KEY**<br />

2- Use a Gmail account for system server mail address:<br />
Get an Gmail account for your system email address<br />
Export Gmail mail address name that includes to virtual environment as **EMAIL_HOST_USER**<br />
Export Gmail account password to virtual environment as **EMAIL_HOST_PASSWORD**<br />

### Celery Implementation:
To schedule daily sending forecast report in subscriber list, User Weather Page (**'Schedule to: HH:MM'**) or Django Admin panel (**'Home - Periodic Tasks'**) can be used. <br />

### Run commands:
1- Run Django project: <br />
`python manage.py runserver 0.0.0.0:8000` <br />
2- Start Celery worker: <br />
`celery -A my_weather_project worker -l info` <br />
3- Start Celery beat scheduler: <br />
`celery -A my_weather_project beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler` <br />