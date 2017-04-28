import time
import datetime

#IMAGE_UPLOAD_PATH = 'user_<id>/attachments/'+'<discussion_id>'+'/images/'+'timestamp/'
#DOCUMENT_UPLOAD_PATH = 'user_<id>/attachments/'+'<discussion_id>'+'/documents/'+'timestamp/'
#AVATAR_UPLOAD_PATH = 'user_<id>/avatar/'+'timestamp/'


def image_upload_path(instance, filename):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y/%m/%d')
    #file will be uploaded to MEDIA_ROOT/attachments/<dicussion_id>/images/<timestamp> 
    return '/user_{0}/attachments/{1}/images/{2}/{3}'.format(instance.user.id, instance.pk, st, filename)
    #return 'user_{0}/{1}'.format(instance.user.id, filename)

def document_upload_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/attachments/<dicussion_id>/images/<timestamp>
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y/%m/%d') 
    return '/user_{0}/attachments/{1}/documents/{2}/{3}'.format(instance.user.id, instance.pk, st, filename)
    #return 'user_{0}/{1}'.format(instance.user.id, filename)

def avatar_upload_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/attachments/<dicussion_id>/images/<timestamp>
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y/%m/%d') 
    return '/user_{0}/avatar/{3}'.format(instance.user.id, filename)
    #return 'user_{0}/{1}'.format(instance.user.id, filename)

def image_upload_path_generic(instance, filename):
    # file will be uploaded to MEDIA_ROOT/attachments/<dicussion_id>/images/<timestamp>
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y/%m/%d') 
    return '/user_{0}/attachments/images/{1}/{2}'.format(instance.user.id, st, filename)
    #return 'user_{0}/{1}'.format(instance.user.id, filename)

def document_upload_path_generic(instance, filename):
    # file will be uploaded to MEDIA_ROOT/attachments/<dicussion_id>/images/<timestamp>
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y/%m/%d') 
    return '/user_{0}/attachments/documents/{1}/{2}'.format(instance.user.id, st, filename)
    #return 'user_{0}/{1}'.format(instance.user.id, filename)

def slugForDiscussion(self):
    return self.title + '-' + str(datetime.datetime.now())

def slugForDiscussor(self):
    return self.analyser.user.first_name + '-' + self.discussion.title + '-' + str(datetime.datetime.now())

