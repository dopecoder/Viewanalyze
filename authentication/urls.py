from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^password/reset/(?P<resetcode>[A-Fa-f0-9]{64})/$', views.PasswordResetActivationView.as_view(), name = 'password-reset-activation'),
	url(r'^password-reset/$', views.PasswordResetView.as_view(), name = 'password-reset'),
]