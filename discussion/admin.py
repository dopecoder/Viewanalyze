from django.contrib import admin
from . import models
from models import  Category, SecondaryTag, TertiaryTag, Avatar, Achievement, Personalization, Analyser, Discussion, Discussor, DiscussionTimeLine, PrivateDiscussion, DiscussionReply, discussionUpvote


admin.site.register(Category)
admin.site.register(TertiaryTag)
admin.site.register(SecondaryTag)
admin.site.register(Avatar)
admin.site.register(Achievement)
admin.site.register(Personalization)
admin.site.register(Analyser)
admin.site.register(Discussion)
admin.site.register(DiscussionTimeLine)
admin.site.register(Discussor)
admin.site.register(PrivateDiscussion)
admin.site.register(DiscussionReply)
admin.site.register(discussionUpvote)
admin.site.register(models.DiscussionUpdate)
admin.site.register(models.DiscussionContentUpdate)
admin.site.register(models.IpDataStore)
admin.site.register(models.Notification)
admin.site.register(models.NotificationContainer)
