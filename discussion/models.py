from django.db import models
from django.contrib.auth.models import User
from viewanalyse import path 
from viewanalyse import constants 
from django.db.models import Q
from django.utils.text import slugify
from django.core.urlresolvers import reverse

class Category(models.Model):
    category_name = models.CharField(max_length=11, unique=True)

    def __unicode__(self):
        return "%s" % (self.category_name)

#Tag class used to inflate tags for the user and to get the tags for storing to a specific discussion
class SecondaryTag(models.Model):
    #TODO : create objects for tags in the database
    category = models.ForeignKey(Category)
    secondary_tag = models.CharField(max_length=constants.SECONDARY_TAG_MAX_LENGTH)
    
    def __unicode__(self):
        return "%s" % (self.secondary_tag)
   	

class TertiaryTag(models.Model):
    #TODO : create objects for tags in the database
    #category = models.ForeignKey(Category)
    #secondary_tag = models.CharField(max_length=constants.SECONDARY_TAG_MAX_LENGTH)
    tertiary_tag =models.CharField(max_length=constants.TERTIARY_TAG_MAX_LENGTH)
    
    def __unicode__(self):
        return "%s" % (self.tertiary_tag)

#Avatar class for handling user avatars for flexibility
class Avatar(models.Model):
    image_attachments = models.ImageField(upload_to = path.avatar_upload_path, null=True, blank=True)

class Personalization(models.Model):
    #TODO : Make Skeleton for personalization
    name = models.CharField(max_length=20, null=True, blank=True)
    primaryCategory = models.ManyToManyField(Category)
    secondaryCategory = models.ManyToManyField(SecondaryTag)
    TertiaryTag = models.ManyToManyField(TertiaryTag)
    #the personalized feed should be new and near to his topic of interest.

#A User class over the primitive User class from django authentication system to have decouple proprties and functionality from authentication 
# and have control over the user level permissions seperately and discussion permissions seperately
class Analyser(models.Model):
    #TODO : counry field modification

    #user field for User Object 
    user = models.OneToOneField(User)

    #avatar field for avatars -> class Avatar 
    avatar = models.OneToOneField(Avatar, null=True, blank=True)

    #User common details
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField()
    country = models.CharField(max_length=40, null=True, blank=True)
    dob = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)

    #discussion specific fields
    #TODO:Create User_Following and User_Followers models for this.
    #Users_following = models.ForeignKey(Follow, related_name='users_following')
    #Users_followers = models.ManyToManyField(User, related_name='users_followers')
    total_upvotes = models.IntegerField(default=0, null=False, blank=True) 
    no_discussions = models.IntegerField(default=0, null=False, blank=True)
    no_replied = models.IntegerField(default=0, null=False, blank=True)
    reputation = models.IntegerField(default=0, null=False, blank=True)
    no_achievements = models.IntegerField(default=0, null=True, blank=True)
    #achievements = models.ForeignKey(Achievement, null=True, blank=True)

    #discussion - following
    #TODO:Create Discussion_Following and Reply_Followers models for this.
    #discussions_following = models.ForeignKey(Follow, related_name='discussions_following')
    #replys_following = models.ForeignKey(Follow, related_name='replys_following')

    #personalization field for user Personalization to provide personalized feeds
    personalization = models.OneToOneField(Personalization, null=True, blank=True)

    def __unicode__(self):
        return "%s" % (self.email)

class Achievement(models.Model):
    #TODO : Make Skeleton for achievements
    #TODO : Makespecific objects for achievements
    achievement = models.CharField(max_length=20, null=True, blank=True)
    analyser = models.ForeignKey(Analyser, null=True, blank=False)
    
    def __unicode__(self):
        return "%s_%s -> %s" % (self.analyser.user.first_name, self.analyser.user.last_name, self.achievement)

class Discussion(models.Model):

    """Discussion class is the main center class containg all the fields required for a discussion and it contains the inverse relationship
        to the Discussor class i.e. the replies to the discussion. Refer Documentation -> BASE_DIR/documentation/discussion/models.txt"""

    #User field where each discussion is specific to a single user object.
    analyser = models.ForeignKey(Analyser, null=True)

    #Main content of the discussion
    category = models.ForeignKey(Category, null=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    
    #navigation
    slug = models.SlugField(max_length=100, unique=True,null=True, blank=True)

    #Attachments
    # image_upload_path, document_upload_path - callables for path
    # check modelApp/path.py for more details
    image_attachments = models.ImageField(upload_to = path.image_upload_path, null=True, blank=True)
    document_attachments = models.FileField(upload_to = path.document_upload_path, null=True, blank=True)

    #Timeline of the discussion
    #timeline = models.OneToOneField('DiscussionTimeLine', null=True, blank=True)

    #relative fields for the discusssion
    upvotes = models.IntegerField(default=0, null=True, blank=True)
    views = models.IntegerField(default=0, null=True, blank=True)
    replies = models.IntegerField(default=0, null=True, blank=True)
    #discussion_followers = models.ForeignKey(Follow, related_name='discussion_followers')#need to add User model
    no_replies = models.IntegerField(default=0, null=True, blank=True)
    analyser_upvoted = models.ForeignKey(Analyser, related_name='upvoted', null=True, blank=True)

    #model status
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'
    OPEN_STATUS = (
        (OPEN, 'discussion open'),
        (CLOSED, 'discussion closed')
    )
    open_status = models.CharField(max_length=6, choices=OPEN_STATUS, default=OPEN)

    PUBLIC = 'PUBLIC'
    PRIVATE = 'PRIVATE'
    PRIVACY_STATUS = (
        (PUBLIC, 'public discussion'),
        (PRIVATE, 'private discussion')
    )
    privacy_status = models.CharField(max_length=7, choices=PRIVACY_STATUS, default=PUBLIC)

    #automatic fields 
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now_add=False, auto_now=True, null=True, blank=True)

    #Tags
    #tags = models.ManyToManyField(Tag)
    secondary_tag = models.ManyToManyField(SecondaryTag)
    tertiary_tag = models.ManyToManyField(TertiaryTag)
    ter_tag = models.CharField(max_length = 1000, null=True)

    #To check whether it was converted from public to private
    isFromPublic = models.BooleanField(default=False)

    #weightage of the discussion
    weightage = models.IntegerField(default=0, null=True, blank=True) 

    class Meta:
        ordering = ['-timestamp']

    def __unicode__(self):
        return "%s : %s -> %s" % (self.category.category_name, self.title, self.analyser.user.first_name)

    def get_absolute_url(self):
        return reverse('discussion-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            slugs = path.slugForDiscussion(self) #title + '-' + str(self.timestamp)
            self.slug = slugify(slugs)

        super(Discussion, self).save(*args, **kwargs)


class DiscussionUpdate(models.Model):
    discussion = models.ForeignKey(Discussion)
    context = models.CharField(max_length=100)
    #title = models.CharField()
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ['-timestamp']

    def __unicode__(self):
        return '%s -> %s' % (self.discussion.title, self.timestamp)

class DiscussionContentUpdate(models.Model):
    discussion = models.ForeignKey(Discussion)
    title = models.CharField(max_length=100, null=True, blank=True)
    context = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering=['-timestamp']

    def __unicode__(self):
        return '%s -> %s' % (self.discussion.title, self.title)

#Attachment class to handle attachments for the user and for decoupling
class Attachment(models.Model):
    #Attachments
    # image_upload_path, document_upload_path - callables for path
    # check modelApp/path.py for more details
    #discussion = models.ForeignKey(Discussion)
    #analyser = models.ForeignKey(Analyser)
    image_attachments = models.ImageField(upload_to = path.image_upload_path_generic, null=True, blank=True)
    document_attachments = models.FileField(upload_to = path.document_upload_path_generic, null=True, blank=True)

class DiscussionTimeLine(models.Model):
    discussion = models.ForeignKey(Discussion)
    analyser = models.ForeignKey(Analyser, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    TO_POST = 'TO_POST'
    class Meta:
        ordering = ['timestamp']

    def __unicode__(self):
        if(self.analyser):
            return "%s : %s -> %s_%s" % (self.discussion.title, self.discussion.category.category_name, self.analyser.user.first_name, self.analyser.user.last_name)
        else:
            return "%s : %s -> %s" % (self.discussion.title, self.discussion.category.category_name, self.TO_POST)


class DiscussionReply(models.Model):
    discussion = models.ForeignKey(Discussion)
    analyser = models.ForeignKey(Analyser, null=True, blank=True)
    #timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    #class Meta:
    #    ordering = ['timestamp']

    def __unicode__(self):
        if self.analyser:
            return "%s %s" % (self.analyser.user.first_name, self.analyser.user.last_name)
        else:
            return "to the post"


class Discussor(models.Model):
    #user relation
    analyser = models.ForeignKey(Analyser, null=True)

    #discussion specific fields
    discussion = models.ForeignKey(Discussion)
    content = models.TextField()
    upvotes = models.IntegerField(default=0, null=False, blank=True)
    context = models.CharField(max_length=constants.CONTEXT_MAX_LENGTH, null=True)
    #make sure you add the Analyser who is present in the discussion
    reply_to = models.ForeignKey(DiscussionReply, related_name='reply_to')
    attachments = models.OneToOneField(Attachment, null=True, blank=True)

    #slugfield
    slug = models.SlugField(max_length=1000, null=True, blank=True)

    #reply_followers = models.ForeignKey(Follow, related_name='reply_followers')
    no_reply_followers = models.IntegerField(default=0, null=False, blank=True)

    #tags
    #tags = models.ManyToManyField(Tag)
    secondary_tag = models.ManyToManyField(SecondaryTag)
    tertiary_tag = models.ManyToManyField(TertiaryTag)
    ter_tag = models.CharField(max_length=1000, null=True)

    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)

    class Meta:
        ordering = ['timestamp']

    def __unicode__(self):
        return "%s : %s -> %s" % ( self.analyser.user.first_name, self.discussion.category, self.discussion.title,)

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            slugs = path.slugForDiscussor(self) #title + '-' + str(self.timestamp)
            self.slug = slugify(slugs)

        super(Discussor, self).save(*args, **kwargs)

class discussionUpvote(models.Model):
    discussion = models.ForeignKey(Discussion)
    analyser = models.ForeignKey(Analyser)

    def __unicode__(self):
        return "%s %s -> %s" % (self.analyser.user.first_name, self.analyser.user.last_name, self.discussion.title)

class discussionReplyUpvote(models.Model):
    discussionReply = models.ForeignKey(Discussor)
    analyser = models.ForeignKey(Analyser)

    def __unicode__(self):
        return "%s %s -> %s" % (self.analyser.user.first_name, self.analyser.user.last_name, self.discussionReply.slug)


class PrivateDiscussion(models.Model):
    discussion = models.ForeignKey(Discussion)
    analyser = models.ManyToManyField(Analyser)

    def __unicode__(self):
        if self.analyser:
            return "%s -> %s" % (self.discussion.title, 'to post')
        else:
            return "%s -> %s" % (self.discussion.title, self.analyser.user.first_name)
 
#User_Following  Discussion_Following  User_Followers  Reply_Followers
class Follow(models.Model):
    ANALYSER = 'ANALYSER'
    REPLY = 'REPLY'
    DISCUSSION = 'DISCUSSION'
    FOLLOW_CHOICES = (
	    (ANALYSER, 'analyser'),
	    (REPLY, 'reply'),
        (DISCUSSION, 'discussion'),
    )
    follow_category = models.CharField(max_length=constants.FOLLOW_CATEGORY_MAX_LENGTH, choices=FOLLOW_CHOICES)
    follower = models.ForeignKey(Analyser, related_name="followed_by")
    analyser = models.ForeignKey(Analyser, null=True, blank=True)
    reply = models.ForeignKey(Discussor, null=True, blank=True)
    discussion = models.ForeignKey(Discussion, null=True, blank=True)
    
    def __unicode__(self):
        if(self.analyser):
            return "er:%s_%s -> %s -> ing:%s_%s" % (self.follower.user.first_name, self.follower.last_name, self.follow_category, self.analyser.first_name, self.analyser.last_name)
        elif(self.reply):
            return "er:%s_%s -> %s -> ing:%s_%s" % (self.follower.user.first_name, self.follower.last_name, self.follow_category, self.reply.analyser.first_name, self.reply.discussion.title)
        else:
            return "er:%s_%s -> %s -> ing:%s_%s" % (self.follower.user.first_name, self.follower.last_name, self.follow_category, self.discussion.title, self.discussion.analyser.user.first_name)

class IpDataStore(models.Model):

    ipAddr = models.CharField(max_length=16, unique=True)
    views = models.CharField(max_length=2000, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)        

    def __unicode__(self):
        return '%s' % self.ipAddr   


class Notification(models.Model):
    
    FGU = 'FGU'
    FRU = 'FRU'
    DU = 'DU'
    SU = 'SU'
    INVITE = 'INVITE'

    NOTIF_TYPE_CHOICES = (
        (FGU, 'Following updates'),
        (FRU, 'followers updates'),
        (DU, 'Discussion updates'),
        (SU, 'System updates'),
        (INVITE, 'Invite notification'),
    )
    #Notification type
        #type telling whether its a following's update and if someone is following notif or your
        #discussion's updates -> upvotes,
        # 1) Following update
        # 2) If someone follows you.
        # 3) dicussion updates -> upvotes, views > 100x upto 1000 and 1000x upto 20000, comments, reports
        # 4) system updates -> achievements, security, account, offers.
    notification_type = models.CharField(max_length=6, choices=NOTIF_TYPE_CHOICES)
    #notification title
    title = models.CharField(max_length=100) 
    #notification text
    text = models.CharField(max_length=200, null=True, blank=True)


class NotificationContainer(models.Model):
    
    analyser = models.OneToOneField(Analyser)
    nofications = models.ManyToManyField(Notification)
    isUpdated = models.BooleanField(default=False)

class NotificationPreference(models.Model):
    pass