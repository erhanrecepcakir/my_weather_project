# Forecast Report with DJANGO

Gets forecast report and sends in an email to subscribers mail addresses. <br />

Before run the application, please export below virtual environment definitions:<br />

1- OpenWeather API Key:<br />
Get an account from https://openweathermap.org/api <br />
Export your API key to virtual environment as 'OPENWEATHERMAP_API_KEY'<br />

2- Use a Gmail account for system server mail address:<br />
Get an Gmail account for your system email address<br />
Export Gmail mail address name that includes to virtual environment as 'EMAIL_HOST_USER'<br />
Export Gmail account password to virtual environment as 'EMAIL_HOST_PASSWORD'<br />

Celery Implementation: <br />
To schedule sending forecast report to subscriber list, Django Admin panel should be used.
"Home - Periodic Tasks" menu includes beat scheduler options.
