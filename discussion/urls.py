from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^discussions/$', views.DiscussionListView.as_view(), name='discussion-list'),
	url(r'^discussion-my/$', views.MyDiscussionListView.as_view(), name='discussion-my'),
	url(r'^discussion-per/$', views.MyPersonalizedListView.as_view(), name='discussion-personalized'),
	url(r'^discussion-private/$', views.PrivateDiscussionListView.as_view(), name='discussion-private'),
	url(r'^discussion/(?P<slug>[-\w]+)/$', views.DiscussionDetailView.as_view(), name='discussion-detail'),
	url(r'^discussion-create/$', views.DiscussionCreateView.as_view(), name='discussion-create'),
	url(r'^discussion-update/(?P<slug>[-\w]+)/$', views.DiscussionUpdateCreateView.as_view(), name='discussion-update'),
	url(r'^discussion-content-update/(?P<slug>[-\w]+)/$', views.DiscussionContentUpdateCreateView.as_view(), name='discussion-content-update'),
	url(r'^discussion-delete/(?P<slug>[-\w]+)/$', views.DiscussionDeleteView.as_view(), name='discussion-delete'),
	url(r'^discussor-create/(?P<slug>[-\w]+)/$', views.DiscussorCreateView.as_view(), name='discussor-create'),
	url(r'^discussor-update/(?P<slug>[-\w]+)/$', views.DiscussorCreateView.as_view(), name='discussor-update'),
	url(r'^get-category/(?P<category>\w+)/$', views.GetSecondaryCategory, name='get-secondary-tag'),
	url(r'^get-tag/(?P<query>\w+)/$', views.GetTertiaryTag, name='get-tertiary-tag'),
	url(r'^get-tag/$', views.GetTertiaryTag, name='get-tertiary-tag-empty'),
	url(r'^upvote/discussion/(?P<slug>[-\w]+)/$', views.SetUpvoteDiscussion, name='set-discussion-upvotes'),
	url(r'^upvote/reply/(?P<slug>[-\w]+)/$', views.SetUpvoteDiscussionReply, name='set-reply-upvotes'),
	url(r'^api-discover/$', views.api_discover, name='api-discover'),	
	url(r'^confirmToPrivate/(?P<slug>[-\w]+)/$', views.ConvertToPrivate.as_view(), name='convert-discussion-private'),
	url(r'^confirmToPublic/(?P<slug>[-\w]+)/$', views.ConvertToPublic.as_view(), name='convert-discussion-public'),	
	url(r'^notifTest/$', views.testNotif, name='test-notif'),	
	url(r'^notification/$', views.NotificationManager, name='notification-manager'),	
]