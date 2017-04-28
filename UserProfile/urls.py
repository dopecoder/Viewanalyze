from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'profile/$', views.UserProfile.as_view(), name='profile-main'),
]