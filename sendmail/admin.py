from django.contrib import admin
from sendmail.models import Client, Message, Mailing


# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'comment',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Mailing)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'interval','status', 'owner',)
