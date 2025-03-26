from celery import shared_task
from datetime import timedelta
from django.utils import timezone

from users.models import User


@shared_task()
def is_online_active():
    users = User.objects.all()
    for user in users:
        if user.last_login:

            if timezone.now() - user.last_login > timedelta(days=30):
                user.is_active = False
                user.save()


