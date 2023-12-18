from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from sendmail.forms import MailingCreateForm
from sendmail.models import Mailing, Message


# Create your views here.


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingCreateForm
    success_url = reverse_lazy('sendmail:home')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mailing
    form_class = MailingCreateForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.user != self.object.owner:
            mailing_fields = [field for field in form.fields.keys()]
            for field in mailing_fields:
                if not self.request.user.has_perm(f'sendmail.set_{field}'):
                    del form.fields[field]
        return form

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return self.request.user == Mailing.objects.get(pk=self.kwargs['pk']).owner

    def get_success_url(self):
        return reverse('sendmail:mailing_view', args=[self.kwargs.get('pk')])


class MailingListView(ListView):
    model = Mailing


class MailingDetailView(DetailView):
    model = Mailing


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('sendmail:home')


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ('title', 'content',)
    success_url = reverse_lazy('sendmail:message_list')


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ('title', 'content',)

    def get_success_url(self):
        return reverse('sendmail:message_view', args=[self.kwargs.get('pk')])


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'sendmail/message_detail.html'


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    extra_context = {
        'title': 'Список Ваших сообщений'
    }


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('sendmail:home')
