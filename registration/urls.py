from django.conf.urls import include, url
from authentication import views
from django.contrib import admin
from . import views

urlpatterns = [
    url(r"register/$", views.RegistrationView.as_view(), name='register'),
    url(r'^registration-successful/$', views.registation_successful, name='registation-successful'),
    url(r'^activation/(?P<activationcode>[A-Fa-f0-9]{64})/$', views.ActivationView.as_view(), name='registation-activation'),    
    url(r'^activation-successful/$', views.activation_successful, name='activation-successful'),
    url(r'^resend-email/$', views.resend_email.as_view(), name='resend-email'),
]