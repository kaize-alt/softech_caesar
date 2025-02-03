from django.core.mail import EmailMessage

from softech.celery import app
from .smtp.sender import smtp


@app.task
def send_email(email):
    connection = smtp()
    message_text = "Для сброса и обновления пароля перейдите по ссылке: "
    message = EmailMessage(
        subject="Письмо для сброса и обновления пароля",
        body=message_text,
        from_email="amanabdukaimov@gmail.com",
        to=[email]
    )
    connection.send_messages([message])
    print("mail sended")


@app.task
def send_email_beat():
    connection = smtp()
    message_text = "Test Celery Beat "
    message = EmailMessage(
        subject="Test",
        body=message_text,
        from_email="amanabdukaimov@gmail.com",
        to=['amankaize@icloud.com']
    )
    connection.send_messages([message])
    print("mail sended")
