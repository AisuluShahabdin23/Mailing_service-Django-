from django.db import models
from django.utils import timezone
import users.models

# Create your models here.
NULLABLE = {'null': True, 'blank': True}
STATUS_CHOICES = [
    ('Создана', 'Создана'),
    ('Активна', 'Активна'),
    ('Завершена', 'Завершена'),
]

INTERVAL_CHOICES = [
    ('1 раз', '1 раз'),
    ('Раз в день', 'Раз в день'),
    ('Раз в неделю', 'Раз в неделю'),
    ('Раз в месяц', 'Раз в месяц'),
]


class Client(models.Model):
    full_name = models.CharField(max_length=150, verbose_name='ФИО')
    email = models.EmailField(verbose_name='Почта')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    owner = models.ForeignKey(users.models.User, on_delete=models.CASCADE, null=True, verbose_name='Чей клиент')

    def __str__(self):
        return f'{self.email} ({self.full_name})'

    def __repr__(self):
        return f'{self.email} ({self.full_name})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    title = models.CharField(max_length=250, verbose_name='Тема')
    content = models.TextField(verbose_name='Содержание')
    owner = models.ForeignKey(users.models.User, on_delete=models.CASCADE, null=True, verbose_name='Владелец сообщения')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Mailing(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название рассылки')
    mail_to = models.ManyToManyField(Client, verbose_name='Клиент_кому')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение', **NULLABLE)
    start_date = models.DateTimeField(default=timezone.now, verbose_name='Время старта рассылки')
    next_date = models.DateTimeField(default=timezone.now, verbose_name='Время следующей рассылки')
    end_date = models.DateTimeField(verbose_name='Время окончания рассылки')
    interval = models.CharField(default='1 раз', max_length=50, choices=INTERVAL_CHOICES, verbose_name='Периодичность')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, help_text="Создана/Завершена")

    owner = models.ForeignKey(users.models.User, on_delete=models.CASCADE, null=True, verbose_name='Владелец рассылки')
    is_activated = models.BooleanField(default=True, verbose_name='Действующая')

    def __str__(self):
        return f'"{self.name}"'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ('start_date',)

        permissions = [
            ('set_is_activated', 'Может отключать рассылку')
        ]


class Logs(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка', **NULLABLE)
    last_mailing_time = models.DateTimeField(auto_now=True, verbose_name='Время последней рассылки')
    status = models.CharField(max_length=50, verbose_name='Статус попытки', null=True)
    response = models.TextField(verbose_name='Ответ сервера', default=None, null=True)

    def __str__(self):
        return f'Отправлено: {self.last_mailing_time}, '\
               f'Статус: {self.status}'

    class Meta:
        verbose_name = 'log'
        verbose_name_plural = 'logs'
