from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from django.views.generic import TemplateView
from users.apps import UsersConfig
from users.views import RegisterView, verification, get_users_list, UserUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify_message/', TemplateView.as_view(template_name='users/verify_message.html'), name='verify_message'),
    path('email/verify/<str:verify_code>', verification, name='verify'),
    path('success_verify/', TemplateView.as_view(template_name='users/success_verify.html'), name='success_verify'),
    path('invalid_verify/', TemplateView.as_view(template_name='users/invalid_verify.html'), name='invalid_verify'),
    path('users_list/', get_users_list, name='list_view'),
    path('edit/<int:pk>', UserUpdateView.as_view(), name='edit')
]
