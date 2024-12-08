import os

from django.conf import Settings
from django.core.mail import get_connection

from softech import settings


def smtp():
    connection = get_connection(
        host=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        username=settings.EMAIL_ADDRESS,
        password=settings.EMAIL_PASSWORD,
        use_tls=True,
    )
    return connection
