from turtle import title

from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db.models.signals import m2m_changed
from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import mail_managers
from django.template.loader import render_to_string
from .models import PostCategory


# функция отправки сообщения подписчикам
def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'Text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        in_category = instance.categories.all()
        subscribers: list[str] = []

        for category in in_category:
            subscribers = category.subscribers.all()
            subscribers = [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.title, subscribers)

#Приветственное сообщение новому пользователю


def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Добро пожаловать на новостной портал'
        message = f"Добро пожаловать, {instance.username}!"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [instance.email])


User = get_user_model()


@receiver(post_save, sender=User)
def user_registered(sender, instance, created, **kwargs):
    if created:
        send_welcome_email(sender, instance, created, **kwargs)


