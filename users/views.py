from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
from users.forms import RegisterForm, ModeratorForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:success_verify')

    def form_valid(self, form):
        if form.is_valid():
            new_user = form.save()
            send_mail(
                subject='Регистрация',
                message=f'Код {new_user.verify_code}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[self.object.email],
                fail_silently=False,
            )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('users:verify_message')


def verification(request, verify_code):
    try:
        user = User.objects.filter(verify_code=verify_code).first()
        user.is_active = True
        user.save()
        return redirect('users:success_verify')
    except (AttributeError, ValidationError):
        return redirect('users:invalid_verify')


class UserUpdateView(PermissionRequiredMixin, UpdateView):
    model = User
    form_class = ModeratorForm
    permission_required = 'set_is_active'
    success_url = 'users:users_list'

    def get_success_url(self):
        return reverse('users:list_view')


@login_required
@permission_required(['users.view_user', 'users.set_is_active'])
def get_users_list(request):
    users_list = User.objects.all()
    context = {
        'object_list': users_list,
        'title': 'Список пользователей сервиса',
    }
    return render(request, 'users/users_list.html', context)
