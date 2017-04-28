from django.conf.urls import url, include
from . import views
urlpatterns = [
	url(r'^$', views.Search.as_view(), name='main-search')
]