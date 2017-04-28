from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'my-groups/$', views.MyGroupListView.as_view(), name='my-group-list'),
    url(r'groups/$', views.GroupListView.as_view(), name='group-list'),
    url(r'group/(?P<slug>[-\w]+)/$', views.GroupDetailView.as_view(), name='group-detail'),
]