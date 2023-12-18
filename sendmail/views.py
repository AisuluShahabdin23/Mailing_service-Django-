import random
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from blog.models import Blog
from sendmail.forms import MailingForm, MessageForm, ClientForm, MailingModeratorForm
from sendmail.models import Mailing, Message, Client, Logs
from sendmail.services import get_cache_for_mailings, get_cache_for_active_mailings


# Create your views here.


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('sendmail:mailing_list')
    extra_context = {
        'title': 'Создание рассылки'
    }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form, *args, **kwargs):
        if form.is_valid():
            new_mailing = form.save(commit=False)
            new_mailing.owner = self.request.user
            new_mailing.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('sendmail:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return self.request.user == Mailing.objects.get(pk=self.kwargs['pk']).owner

    def get_success_url(self):
        return reverse('sendmail:mailing_view', args=[self.kwargs.get('pk')])


class MailingUpdateModeratorView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingModeratorForm
    success_url = reverse_lazy('sendmail:mailing_list')
    permission_required = 'sendmail.set_is_activated'


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    # extra_context = {
    #     'title': 'Список рассылок'
    # }


class MailingDetailView(DetailView):
    model = Mailing

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['clients'] = list(self.object.mail_to.all())
        context_data['logs'] = list(Logs.objects.filter(mailing=self.object))
        return context_data


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('sendmail:mailing_list')


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('sendmail:message_list')
    extra_context = {
        'title': 'Создание сообщения'
    }

    def form_valid(self, form):
        new_message = form.save()
        new_message.owner = self.request.user
        new_message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse('sendmail:message_view', args=[self.kwargs.get('pk')])


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    #template_name = 'sendmail/message_detail.html'


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    extra_context = {
        'title': 'Список Ваших сообщений'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = Message.objects.filter(owner=self.request.user)
        return queryset


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('sendmail:message_list')


class HomeView(ListView):
    model = Mailing
    template_name = 'sendmail/home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['mailings_count'] = get_cache_for_mailings()
        context_data['active_mailings_count'] = get_cache_for_active_mailings()
        blog_list = list(Blog.objects.all())
        random.shuffle(blog_list)
        context_data['blog_list'] = blog_list[:3]
        context_data['clients_count'] = len(Client.objects.all())
        return context_data


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    extra_context = {
        'title': 'Список клиентов'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = Client.objects.filter(owner=self.request.user)
        return queryset


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('sendmail:client_list')
    extra_context = {
        'title': 'Добавить клиента'
    }

    def form_valid(self, form):
        new_client = form.save()
        new_client.owner = self.request.user
        new_client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('sendmail:client_list')

    def test_func(self):
        return self.request.user == Client.objects.get(pk=self.kwargs['pk']).owner
