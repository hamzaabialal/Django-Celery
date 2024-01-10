# task.py
from myproject.celery import app
from django.core.mail import send_mail
from .models import Notification
from celery import shared_task
from myproject import settings
from django.contrib.auth import get_user_model


@shared_task(bind=True)
def send_mail_func(self):
    users = get_user_model().objects.all()
    unread_notification = Notification.objects.filter(status='unread').last()  # Fetch the latest unread notification

    if unread_notification:
        mail_subject = unread_notification.title
        message = unread_notification.body

        for user in users:
            to_email = user.email
            send_mail(
                subject=mail_subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[to_email],
                fail_silently=True,
            )
            return f"Notification Sent to {to_email}"  # Indentation fixed to return inside the loop

    return "No unread notifications or users found"  # Move the return statement outside the loop
