from django.db import models
from sendmail.models import NULLABLE


class Blog(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Текст')
    preview = models.ImageField(upload_to='blog/preview/', verbose_name='Изображение', **NULLABLE)
    views_count = models.IntegerField(default=0, verbose_name='Количество просмотров')
    date_public = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"
