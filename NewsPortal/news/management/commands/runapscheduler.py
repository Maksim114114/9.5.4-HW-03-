import datetime
import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from news.models import Category

from news.models import Post

logger = logging.getLogger(__name__)


def my_job():
    today = timezone.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_in_post__gte=last_week)
    categories = set(posts.values_list('categories__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'daily_post.html',
        {
            #'link': settings.SITE_URL,
            'link': f'{settings.SITE_URL}/news/',
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Статьи за неделю(runapscheduler.py)',
        body='',
        from_email='smax85@yandex.ru',
        #settings.EMAIL_HOST_USER_FULL,
        to=['maksimus114114@gmail.com', 'sel-max@mail.ru'],
        #subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def my_job_2():
    #  Your job processing logic here...
    # print('hello from job')
    send_mail(
        'Job mail',
        'Hello from job! D954 Modul. Next Gen!(my_job_2)проверка',
        from_email='smax85@yandex.ru',
        recipient_list=['maksimus114114@gmail.com', 'sel-max@mail.ru'],
        fail_silently=False,
    )


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(minute="*/1"),
            #trigger=CronTrigger(hour="19",minute="36",day_of_week="thu", timezone="utc"),
           # trigger=CronTrigger(day_of_week='mon', hour='09', minute='30'),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="09", minute="46"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить,
            # либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )


        scheduler.add_job(
            my_job_2,
            trigger=CronTrigger(minute="*/1"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job_2",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job_2'.")


        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")