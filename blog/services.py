from django.conf import settings
from django.core.cache import cache

from blog.models import Blog
from config.settings import CACHE_ENABLED


def cache_blog():
    if CACHE_ENABLED:
        # Проверяем включенность кеша
        key = f'blog_list'
        blog_list = cache.get(key)
        if blog_list is None:
            # Если данные не были получены из кеша, то выбираем из БД и записываем в кеш
            blog_list = Blog.objects.all()
            cache.set(key, blog_list)
    else:
        # Если кеш не был подключен, то просто обращаемся к БД
        blog_list = Blog.objects.all()
    return blog_list
