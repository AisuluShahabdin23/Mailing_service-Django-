from datetime import timedelta, datetime
import pytz
from django.conf import settings
from django.core.mail import send_mail
from sendmail.models import Mailing, Logs


def my_job():
    day = timedelta(days=1, hours=0, minutes=0)
    weak = timedelta(days=7, hours=0, minutes=0)
    month = timedelta(days=30, hours=0, minutes=0)

    mailings = Mailing.objects.all().filter(status='Создана') \
        .filter(is_activated=True)\
        .filter(next_date__lte=datetime.now(pytz.timezone('Europe/Moscow')))\
        .filter(end_date__gte=datetime.now(pytz.timezone('Europe/Moscow')))

    for mailing in mailings:
        print(mailing.name)
        mailing.status = 'Активна'
        mailing.save()
        emails_list = [client.email for client in mailing.mail_to.all()]

        result = send_mail(
            subject=mailing.message.title,
            message=mailing.message.content,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=emails_list,
            fail_silently=False,
        )
        print(result)

        if result == 1:
            status = 'отправлено'
        else:
            status = 'ошибка отправки'

        log = Logs(status=status)
        log.save()
        print(log.last_mailing_time)

        if mailing.interval == 'ежедневно':
            mailing.next_date += day
        elif mailing.interval == 'раз в неделю':
            mailing.next_date += weak
        elif mailing.interval == 'раз в месяц':
            mailing.next_date += month

        if mailing.next_date < mailing.end_date:
            mailing.status = 'Создана'
        else:
            mailing.status = 'Завершена'
        mailing.save()
        print(mailing.status)


if __name__ == "__main__":
    my_job()
