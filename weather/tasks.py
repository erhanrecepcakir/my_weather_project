from celery import shared_task
from django.core.mail import send_mail


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
