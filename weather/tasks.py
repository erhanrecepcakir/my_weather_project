from celery import shared_task
from my_weather_project.celery import app

from django.core.mail import send_mail
from .utils import mail_sender_to_all_subscribers, send_mail_for_citylist

@shared_task
def send_mail_func(context):
    return (
        send_mail(
            context['subject'], 
            context['plain_message'], 
            context['email_host_user'], 
            context['recepient_list'], 
            html_message=context['html_message'])            
    )

@app.task(name='periodic_report_sender_to_subs_list')
def periodic_report_sender_to_subs_list():
    mail_sender_to_all_subscribers()
    print('Periodic task is executed!!!')
    
@app.task(name='configurable_periodic_mail_sender', bind=True)
def configurable_periodic_mail_sender(self, citylist_id):
    send_mail_for_citylist(citylist_id)
    return True



