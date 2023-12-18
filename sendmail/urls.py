from django.urls import path

from sendmail.apps import SendmailConfig
from sendmail.views import MailingListView, MailingCreateView, MailingDetailView, MailingUpdateView, MailingDeleteView, \
    MessageListView, MessageCreateView, MessageUpdateView, MessageDetailView, MessageDeleteView

app_name = SendmailConfig.name

urlpatterns = [
    path('', MailingListView.as_view(), name='home'),
    path('mailing_create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing_view/<int:pk>', MailingDetailView.as_view(), name='mailing_view'),
    path('mailing_edit/<int:pk>/', MailingUpdateView.as_view(), name='mailing_edit'),
    path('mailing_delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('message_list/', MessageListView.as_view(), name='message_list'),
    path('message_create/', MessageCreateView.as_view(), name='message_create'),
    path('message_edit/<int:pk>/', MessageUpdateView.as_view(), name='message_edit'),
    path('message_view/<int:pk>/', MessageDetailView.as_view(), name='message_view'),
    path('message_delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
]
