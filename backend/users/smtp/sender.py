import os

from django.conf import Settings
from django.core.mail import get_connection

from softech import settings


def smtp():
    connection = get_connection(
        host='backend.settings'.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
        use_tls=True,
    )
    return connection
