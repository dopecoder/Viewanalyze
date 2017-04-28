from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponsePermanentRedirect
from django.forms.formsets import formset_factory
from django.core.urlresolvers import reverse
from search import views as searchViews
from personalization import views as personalize
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from viewanalyse import constants
from . import models, forms
import datetime
import time


class IPDataStore(object):
    IpDataStore = {}

#MIXINS
class LoggedInMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    request.session['isNotification'] = False
    personalization = personalize.getPersonInstance()

    #variable declaration
    st_key = 0
    tt_key = 0
    queryset = 0
    try:
        st_key, tt_key = personalization.getPersonalizeTag(request.user)
    except:
        print("There was a problem in getting the user's st_key, tt_key -> it either does not exist or there was a problem fetching it.")

    if st_key:
        st = models.SecondaryTag.objects.get(pk=st_key)
    if tt_key:
        tt = models.TertiaryTag.objects.get(pk=tt_key)

    #personalized query set
    analyser = models.Analyser.objects.get(user=request.user)
    viewstore = personalize.getViewStoreInstance()
    try:
        discussionpk = viewstore.getDiscussionPk(analyser.pk)
        print "DISCUSSION_PK -> %s" % discussionpk
        pk_list, firstviewflag = viewstore.getPersonalizedQuerySet(analyser.pk, discussionpk)
        print "PK_LIST -> %s" % pk_list
        queryset = viewstore.getDiscussion(pk_list)
        print "QUERYSET -> %s" % queryset
    except:
        print "New user still does not have the personalized data."


    if st_key and tt_key and queryset:
        return render_to_response('discussion/discussion_index.html', {'user': request.user, 'st_tag': st.secondary_tag, 'tt_tag':tt.tertiary_tag, 'per_queryset':queryset, 'first_view_flag':firstviewflag})
    else:
        return render_to_response('discussion/discussion_index.html', {'user': request.user})#, 'st_tag': st.secondary_tag, 'tt_tag':tt.tertiary_tag, 'per_queryset':queryset})


#Discussion Views
class DiscussionListView(ListView):
    model = models.Discussion

    def get_queryset(self):
        return models.Discussion.objects.filter(privacy_status = models.Discussion.PUBLIC)


class MyDiscussionListView(LoggedInMixin, ListView):
    model = models.Discussion
    template_name = 'discussion/discussion_my.html'

    def get_queryset(self):
        analyser = models.Analyser.objects.get(user = self.request.user)
        return models.Discussion.objects.filter(analyser = analyser)


class MyPersonalizedListView(LoggedInMixin, ListView):
    model = models.Discussion
    template_name = 'discussion/discussion_list.html'


    def get_queryset(self):
        analyser = models.Analyser.objects.get(user = self.request.user)
        personalization = analyser.personalization
        print '%s' % personalization.secondaryCategory.all()
        print '%s' % personalization.TertiaryTag.all()
        if personalization:
            queryset = models.Discussion.objects.filter(secondary_tag=personalization.secondaryCategory.all(), 
                tertiary_tag=personalization.TertiaryTag.all()).exclude(privacy_status=models.Discussion.PRIVATE).order_by('-timestamp')
            #queryset
            return queryset
        else:
            return None    


#private discussion ListView
class PrivateDiscussionListView(LoggedInMixin, ListView):
    model = models.PrivateDiscussion
    template_name_suffix = '_private'


    def get_queryset(self):
        analyser = models.Analyser.objects.get(user = self.request.user)
        return models.PrivateDiscussion.objects.filter(analyser = analyser)
        

class DiscussionUpdateView(LoggedInMixin, UpdateView):
    model = models.Discussion
    fields = ['content', 'privacy_status', 'secondary_tag', 'tertiary_tag',]
    template_name_suffix = '_update_form'


    def get_success_url(self):
        print self.contentForSearch
        #search = searchViews.getIndexInstance()
        #search.mainfunc(self.contentForSearch, self.object.pk)
        return reverse('discussion-detail', kwargs={'slug': self.object.slug})


    def get_context_data(self, **kwargs):
        context = super(DiscussionUpdateView, self).get_context_data(**kwargs)
        user = self.request.user
        context['analyser'] = models.Analyser.objects.get(user = user)#, None)
        context['owner'] = self.object
        #context['DiscussorFormSet'] = formset_factory()
        return context


    def form_valid(self, form):
        content = self.object.content + 'Updated on ' + str(datetime.date.today()) + form.instance.content
        form.instance.content = content
        
        self.object = form.save(commit=False)  # Not saved to database.
        #self.object.user = self.request.user
        self.object.save()  # Saved.

        # get all the tags and append it to the contentForSearch
        tagsToAppend = []
        for tags in self.object.secondary_tag.all():
            tagsToAppend.append(tags.secondary_tag)

        for tags in self.object.tertiary_tag.all():
            tagsToAppend.append(tags.tertiary_tag)

        for tag in tagsToAppend:
            self.contentForSearch = self.contentForSearch + ' ' + tag

        super(DiscussionUpdateView, self).form_valid(form)


class ConvertToPublic(LoggedInMixin, View):


    def get(self, request, *args, **kwargs):
        slug = kwargs['slug']
        form = forms.ConfirmForm()
        return render(request, 'discussion/confirm.html', {'form':form, 'slug':slug, 'Message': 'Are you sure you want to convert the discussion to public?'})


    def post(self, request, *args, **kwargs):
        form = forms.ConfirmForm(request.POST)
        slug = kwargs['slug']
        if form.is_valid():
            cleanedForm = form.cleaned_data
            if cleanedForm.get('confirm') == forms.ConfirmForm.YES:
            #perform the conversion
                try:
                    discussion = models.Discussion.objects.get(slug=slug)
                except models.Discussion.DoesNotExist:
                    return HttpResponse('The discussion does not exist!')

                user = self.request.user
                analyser = models.Analyser.objects.get(user = user)
                if user == discussion.analyser.user:
                    privatediscussions = models.PrivateDiscussion.objects.filter(discussion=discussion)
                    discussionreply = models.DiscussionReply.objects.filter(discussion=discussion)
                    privatediscussions.delete()
                    discussionreply.delete()
                    models.DiscussionReply.objects.create(discussion=discussion)
                    #print "Till here!"
                    discussion.privacy_status = 'PUBLIC'
                    #print '%s' % discussion.privacy_status
                    discussion.save()
                    #print '%s' % discussion.privacy_status
                    return HttpResponseRedirect(reverse('discussion-private'))
            else:
                return HttpResponseRedirect(reverse('discussion-private'))


class ConvertToPrivate(LoggedInMixin, View):


    def get(self, request, *args, **kwargs):
        slug = kwargs['slug']
        form = forms.ConfirmForm()
        return render(request, 'discussion/confirm.html', {'form':form, 'slug':slug, 'Message': 'Are you sure you want to convert the discussion to private?'})


    def post(self, request, *args, **kwargs):
        form = forms.ConfirmForm(request.POST)
        slug = kwargs['slug']
        if form.is_valid():
            cleanedForm = form.cleaned_data
            if cleanedForm.get('confirm') == forms.ConfirmForm.YES:

                #perform the conversion
                try:
                    discussion = models.Discussion.objects.get(slug=slug)
                except models.Discussion.DoesNotExist:
                    return reverse('discussion-list')

                user = self.request.user
                analyser = models.Analyser.objects.get(user = user)
                if user == discussion.analyser.user:

                    contentForSearch = discussion.title + ' ' + discussion.content 

                    privateDiscussion = models.Discussion(analyser=analyser, content=discussion.content, category=discussion.category, \
                                                    title=discussion.title , open_status=models.Discussion.OPEN, \
                                                    privacy_status=models.Discussion.PRIVATE, isFromPublic = True)
                    privateDiscussion.save()
                    print 's -> %s' % discussion.secondary_tag.all()
                    print 't -> %s' % discussion.tertiary_tag.all()
                    privateDiscussion.secondary_tag.add(*discussion.secondary_tag.all())
                    privateDiscussion.tertiary_tag.add(*discussion.tertiary_tag.all())
                    privateDiscussion.save()

                    if privateDiscussion.privacy_status == models.Discussion.PRIVATE:
                        privateDiscussionCreate = models.PrivateDiscussion(discussion = privateDiscussion)
                        privateDiscussionCreate.save()
                        privateDiscussionCreate.analyser.add(analyser)
                        privateDiscussionCreate.save()

                    # get all the tags and append it to the contentForSearch
                    tagsToAppend = []
                    for tags in discussion.secondary_tag.all():
                        tagsToAppend.append(tags.secondary_tag)

                    for tags in discussion.tertiary_tag.all():
                        tagsToAppend.append(tags.tertiary_tag)

                    for tag in tagsToAppend:
                        contentForSearch = contentForSearch + ' ' + tag

                    print 'tagsToAppend -> %s' % tagsToAppend
                    print 'contentForSearch -> %s' % contentForSearch
                    search = searchViews.getIndexInstance()
                    search.mainfunc(contentForSearch, privateDiscussion.pk)
                    discussionreply = models.DiscussionReply.objects.create(discussion = privateDiscussion)
                    discussionreply.delete()
                    print "Till here!"
                    return HttpResponseRedirect(reverse('index'))#('discussion-list')#, kwargs={'slug': privateDiscussion.slug})
            else:
                return HttpResponseRedirect(reverse('index'))


class DiscussionCreateView(LoggedInMixin, CreateView):
    model = models.Discussion
    contentForSearch = ''
    form_class = forms.CreateDiscussionForm

    def get_success_url(self):
        #add the user to his private discussion if he starts one 
        if (self.object.privacy_status == models.Discussion.PRIVATE):
            analyser = models.Analyser.objects.get(user = self.request.user)
            privateDiscussion = models.PrivateDiscussion(discussion = self.object)
            privateDiscussion.save()
            privateDiscussion.analyser.add(analyser)
            privateDiscussion.save()

        print self.contentForSearch
        search = searchViews.getIndexInstance()
        search.mainfunc(self.contentForSearch, self.object.pk)
        models.DiscussionReply.objects.create(discussion = self.object)
        #return HttpResponsePermanentRedirect(reverse('discussion-detail', kwargs={'slug': self.object.slug}))
        return reverse('discussion-detail', kwargs={'slug': self.object.slug})
        #return reverse('discussion-detail', kwargs={'slug':self.object.slug, 'object': self.object})


    def form_valid(self, form):
        """
        try:
            user = self.request.user
        except:
            raise ValidationError('No User Found')
            #TODO : handle the exception and do whatever required -> redirect to login or tell he doesnt have permissions
            """
        print 'POST data -> %s' % self.request.POST
        user = self.request.user
        analyser = models.Analyser.objects.get(user = user)
        form.instance.analyser = analyser

        print "DISCUSSION TITLE LENGTH : %s" % len(form.instance.title)
        #Check whether the fields are upto the website standards
        #if(len(form.instance.title) < constants.DISCUSSION_TITLE_MIN_LENGTH):
        #    return render_to_response('discussion/discussion_form.html', {'form':form, 'errors': ['The title should be of atleast 25 characters long.']}, context_instance = RequestContext(self.request))
        #elif(len(form.instance.content) < constants.DISCUSSION_CONTENT_MIN_LENGTH):
        #    return render_to_response('discussion/discussion_form.html', {'form':form, 'errors': ['The description should be of atleast 100 characters long.']}, context_instance = RequestContext(self.request))

        self.contentForSearch = form.instance.title + ' '  + form.instance.content

        #form.instance.tertiary_tag = tertiary_tag
        discussor = models.Discussion.objects.filter(analyser = analyser, title = form.instance.title)
        if discussor:
            return render_to_response('discussion/discussion_form.html',
                                      {'form':form, 'errors': ['you have already have discussion with this title.']})
                                      #context_instance = RequestContext(self.request))

        #search = getIndexInstance()
        #search.mainfunc(contentForSearch, searchViews.DISCUSSION, self.object.id)
        self.object = form.save(commit=False)  # Not saved to database.
        #self.object.user = self.request.user
        self.object.save()  # Saved.
        tags=[]
        tag_names = form.instance.ter_tag.split()
        for tag_name in tag_names:
            tag, dummy = models.TertiaryTag.objects.get_or_create(tertiary_tag=tag_name)
            self.object.ter_tag = tag_names
            self.object.tertiary_tag.add(tag)


        # get all the tags and append it to the contentForSearch
        tagsToAppend = []
        for tags in self.object.secondary_tag.all():
            tagsToAppend.append(tags.secondary_tag)

        for tags in self.object.tertiary_tag.all():
            tagsToAppend.append(tags.tertiary_tag)

        for tag in tagsToAppend:
            self.contentForSearch = self.contentForSearch + ' ' + tag


        #update the no_discussion started by the user
        analyser.no_discussions += 1
        analyser.save()

        return super(DiscussionCreateView, self).form_valid(form)



class DiscussionUpdateCreateView(LoggedInMixin, CreateView):
    model=models.DiscussionUpdate
    fields = ['context', 'content']


    def get_context_data(self, **kwargs):
        context = super(DiscussionUpdateCreateView, self).get_context_data(**kwargs)
        self.discussion = models.Discussion.objects.get(slug=self.kwargs['slug'])
        analyser = models.Analyser.objects.get(user=self.request.user)
        if self.discussion.analyser != analyser:
            context['notAllowed'] = True
        return context


    def get_success_url(self):
        print self.contentForSearch
        search = searchViews.getIndexInstance()
        search.mainfunc(self.contentForSearch, self.discussion.pk)
        return reverse('discussion-detail', kwargs={'slug': self.discussion.slug})

        
    def form_valid(self, form):

        print 'POST data -> %s' % self.request.POST
        user = self.request.user
        analyser = models.Analyser.objects.get(user = user)
        self.discussion = models.Discussion.objects.get(slug=self.kwargs['slug'])
        form.instance.discussion = self.discussion
        #form.instance.analyser = analyser
        self.contentForSearch = form.instance.context + ' '  + form.instance.content

        #form.instance.tertiary_tag = tertiary_tag
        alteration = models.DiscussionUpdate.objects.filter(discussion=self.discussion, context = form.instance.context, content = form.instance.content)
        if alteration:
            return render_to_response('discussion/discussionupdate_form.html', {'form':form, 'errors': ['you already have this correction for the discussion.']}, context_instance = RequestContext(self.request))

        return super(DiscussionUpdateCreateView, self).form_valid(form)


class DiscussionContentUpdateCreateView(LoggedInMixin, CreateView):
    model=models.DiscussionContentUpdate
    fields = ['context', 'content']
    template_name = 'discussion/discussionupdate_form.html'

    #def dispatch(self, *args, **kwargs):
    #    super(DiscussionUpdateCreateView, self).dispatch(*args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(DiscussionContentUpdateCreateView, self).get_context_data(**kwargs)
        self.discussion = models.Discussion.objects.get(slug=self.kwargs['slug'])
        analyser = models.Analyser.objects.get(user=self.request.user)
        if self.discussion.analyser != analyser:
            context['notAllowed'] = True
        return context


    def get_success_url(self):
        print self.contentForSearch
        search = searchViews.getIndexInstance()
        search.mainfunc(self.contentForSearch, self.discussion.pk)
        return reverse('discussion-detail', kwargs={'slug':self.discussion.slug})


    def form_valid(self, form):

        print 'POST data -> %s' % self.request.POST
        user = self.request.user
        analyser = models.Analyser.objects.get(user = user)
        self.discussion = models.Discussion.objects.get(slug=self.kwargs['slug'])
        form.instance.discussion = self.discussion
        #form.instance.analyser = analyser
        self.contentForSearch = form.instance.context + ' '  + form.instance.content

        #form.instance.tertiary_tag = tertiary_tag
        alteration = models.DiscussionContentUpdate.objects.filter(discussion=self.discussion, context = form.instance.context, content = form.instance.content)
        if alteration:
            return render_to_response('discussion/discussionupdate_form.html', {'form':form, 'errors': ['you already have this correction for the discussion.']}, context_instance = RequestContext(self.request))
        
        return super(DiscussionContentUpdateCreateView, self).form_valid(form)


class DiscussionDeleteView(LoggedInMixin, DeleteView):
    model = models.Discussion
    template_name_suffix = '_delete_form'


    def get_success_url(self):
        return reverse('index')
        #return render_to_response('discussion/discussion_index.html', {'user': self.request.user})


    def get_context_data(self, **kwargs):
        context = super(DiscussionDeleteView, self).get_context_data(**kwargs)
        context['owner'] = self.object.analyser
        context['analyser'] = models.Analyser.objects.get(user = self.request.user)
        return context


    def form_valid(self, form):
        discussors = models.Discussor.objects.filter(discussion = self.object)
        discussors.delete
        return super(DiscussionDeleteView, self).form_valid(form)


    def get_context_data(self, **kwargs):
        context = super(DiscussionDeleteView, self).get_context_data(**kwargs)
        """
        try:
            context['user'] = self.request.user
        except:
            raise ValidationError('No User Found')
            #TODO : handle the exception and do whatever required -> redirect to login or tell he doesnt have permissions
            """
        context['user'] = self.request.user
        return context


class DiscussionDetailView(DetailView):
    model = models.Discussion


    def privateAuthorizationCheck(self):
        if self.request.user.is_authenticated():
        #check if discussion is private
            analyser = models.Analyser.objects.get(user=self.request.user)
            #if the discussion is private check wheather the current user is in the private discussion
            try:
                privateDiscussion = models.PrivateDiscussion.objects.get(discussion=self.object)
                if analyser not in privateDiscussion.analyser.all():
                    return 0 #HttpResponse('You are not allowed to view this discussion.')
                    #return HttpResponseRedirect('/discussion') 
                else:
                    return 1
            except models.PrivateDiscussion.DoesNotExist:
                return 0
                #return HttpResponse('You are not allowed to view this discussion.')
                #return HttpResponseRedirect('/discussion')
        else:
            return 2

    
    def views(self):
        #ipstore = middleware.getIpStoreInstance()

        if not self.request.session['no-ip']:
            #dataStore = self.request.session['dataStore']
            ip = self.request.session['ip-addr']
            if self.object.pk in IPDataStore.IpDataStore[ip]['views']:#IpDataStore
                pass
            else:
                self.object.views += 1
                self.object.save()
                IPDataStore.IpDataStore[ip]['views'].append(self.object.pk)
                if self.request.user.is_authenticated():

                    #Personalization part
                    user = self.request.user
                    analyser = models.Analyser.objects.get(user=user)
                    personalization = personalize.getPersonInstance()
                    personalization.setPersonalizeTag(user, self.object)
                    st_key, tt_key = personalization.getPersonalizeTag(user)
                    print personalization.TagIndex

                    #personalized discussions
                    viewstore = personalize.getViewStoreInstance()
                    viewstore.updateIndex(analyser.pk, self.object.pk)

    def get_context_data(self, **kwargs): 
        print self.request.session.session_key
        context = super(DiscussionDetailView, self).get_context_data(**kwargs)
        #self.request.session["present-discussion-id"] = self.object.id
        #self.request.session["present-discussion-slug"] = self.object.slug
        if self.object.privacy_status == models.Discussion.PRIVATE:
            auth = self.privateAuthorizationCheck()
            if auth == 2:
                context['unauthorized'] = True
                context['notLogged'] = True
                return context
            elif auth==0:
                context['unauthorized'] = True
                return context
            elif auth==1:
                pass
        user = self.request.user
        if not self.request.user.is_authenticated():
            from django.contrib.auth.models import AnonymousUser
            user = AnonymousUser()
            context['AnonymousUser'] = True
            self.views()
        else:
            analyser = models.Analyser.objects.get(user=user)
            form = forms.CreateNewDiscussorForm(objectid=self.object.id, analyser=analyser)
            Discussorformset = formset_factory(form, extra=1)
            formset = Discussorformset()
            self.views()
            context['AnonymousUser'] = False
            context['formset'] = form
            context['analyser'] = models.Analyser.objects.get(user = user)#, None)
            context['discussion'] = models.Discussion.objects.get(pk = self.object.pk)
        return context


##############################################################################################################################
#Discussor Views
class DiscussorCreateView(LoggedInMixin, CreateView):
    model = models.Discussor
    form_class = forms.CreateDiscussorForm
    #template_name = 'discussion/discussion_detail.html'
    contentForSearch = ''


    def __init__(self, *args, **kwargs):
        super(DiscussorCreateView, self).__init__(*args, **kwargs)
    #    self.discussion = models.Discussion.objects.get(slug = kwargs['slug'])


    def get_success_url(self):
        print self.contentForSearch
        search = searchViews.getIndexInstance()
        search.mainfunc(self.contentForSearch, self.object.discussion.pk)
        return reverse('discussion-detail', kwargs={'slug': self.kwargs['slug']})


    def form_valid(self, form):
        analyser = models.Analyser.objects.get(user = self.request.user)
        form.instance.analyser = analyser
        #discussion = models.Discussion.objects.get(id = self.request.session["present-discussion-id"])
        self.discussion = models.Discussion.objects.get(slug = self.kwargs['slug'])
        form.instance.discussion = self.discussion

        #check for form re-submnission or user posting the same reply
        discussor = models.Discussor.objects.filter(analyser = analyser, discussion = self.discussion, content = form.instance.content, context = form.instance.context)
        if discussor:
            return render_to_response('discussion/discussor_form.html', {'form':form, 'errors': ['you have already submitted this data.']}, context_instance = RequestContext(self.request))
            #return reverse('discussion-detail', kwargs={'slug': self.request.session["present-discussion-slug"]})
        
        #create discussion timeline and discussion reply objects
        models.DiscussionTimeLine.objects.create(discussion=self.discussion, analyser=analyser)

        try:
            discussionreply = models.DiscussionReply.objects.get(discussion=self.discussion, analyser=analyser)
        except models.DiscussionReply.DoesNotExist:
            models.DiscussionReply.objects.create(discussion=self.discussion, analyser=analyser)

        self.object = form.save(commit=False)  # Not saved to database.
        #self.object.user = self.request.user
        self.object.save()  # Saved.
        tags=[]
        tag_names = form.instance.ter_tag.split()
        for tag_name in tag_names:
            tag, dummy = models.TertiaryTag.objects.get_or_create(tertiary_tag=tag_name)
            self.object.tertiary_tag.add(tag)

        self.contentForSearch = form.instance.context + ' '  + form.instance.content

        #upadate the number of replies by the analyser
        analyser.no_replied += 1
        analyser.save()

        return super(DiscussorCreateView, self).form_valid(form)


    """
    def get_context_data(self, **kwargs):
        context = super(DiscussorCreateView, self).get_context_data(**kwargs)
        #self.request.session["present-discussion-id"] = self.object.id
        #self.request.session["present-discussion-slug"] = self.object.slug
        user = self.request.user

        self.discussion = models.Discussion.objects.get(slug = self.kwargs['slug'])
        analyser = models.Analyser.objects.get(user=user)
        form = forms.CreateNewDiscussorForm(objectid=self.discussion.id, analyser=analyser)
        Discussorformset = formset_factory(form, extra=1)
        formset = Discussorformset()
        context['formset'] = form
        context['analyser'] = models.Analyser.objects.get(user = user)#, None)
        context['discussion'] = models.Discussion.objects.get(pk = self.discussion.pk)
        context['object'] = self.discussion
        return context"""


class DiscussorUpdateView(LoggedInMixin, UpdateView):
    model = models.Discussor
    fields = ['reply_to', 'context', 'content']
    template_name_suffix = '_update_form'


    def get_success_url(self):
        return reverse('discussor-update', kwargs={'slug': self.kwargs['slug']}) #TODO : Alter the kwargs field


    def get_context_data(self, **kwargs):
        context = super(DiscussionUpdateView, self).get_context_data(**kwargs)
        user = self.request.user
        context['analyser'] = models.Analyser.objects.get(user = user)#, None)
        context['owner'] = self.object
        return context


    def form_valid(self, form):
        content = self.object.content
        form.instance.content = content + form.instance.content
        return super(DiscussorUpdateView, self).form_valid(form)


###############################################################################################################################
#Tag Views
#TODO: Create a ajax request and response after the frontend is done. Query tags entered by the user and if not present
# Create those tags.
"""
class SecondaryTagCreateView(CreateView):
    model = models.SecondaryTag
    template_name_suffix = '_ST_create_form'

    def get_queryset(self):
        return models.SecondaryTag.objects.filter(category)
"""


def GetSecondaryCategory(request, category):
    if request.method == 'GET':
    #if request.is_ajax():
        tags = []
        if category == '1':
            actualCategory = models.Category.objects.get(category_name = 'ABSTRACT')
        elif category == '2':
            actualCategory = models.Category.objects.get(category_name = 'EXPERIENCE')
        elif category == '3':
            actualCategory = models.Category.objects.get(category_name = 'IDEA')
        elif category == '4':
            actualCategory = models.Category.objects.get(category_name = 'OFFTOPIC')
            #return JsonResponse({'tags':'<option value="empty">empty</option>'})

        obj = models.SecondaryTag.objects.filter(category=actualCategory)
        if obj:
            for tag in obj:
                obj_id = models.SecondaryTag.objects.get(category=actualCategory, secondary_tag=tag.secondary_tag)
                tags.append('<option value="'+str(obj_id.pk)+'">'+tag.secondary_tag+'</option>')
            data = {'tags':tags}
    return JsonResponse(data)


def api_discover(request):
    return render(request, 'discussion/api_discover.html')


def GetTertiaryTag(request, query=''):
    if request.method == 'GET':
        if query == '':
            return JsonResponse({'tertiary_tag':[]})
        queryset =  models.TertiaryTag.objects.filter(tertiary_tag__istartswith = query)
        tags = []
        for query in queryset:
            tags.append('<li>'+query.tertiary_tag+'</li>')

        data = {'tertiary_tag':tags}
        return JsonResponse(data)


def SetUpvoteDiscussion(request, slug=''):
    if request.method == 'GET':

        try:
            discussion =  models.Discussion.objects.get(slug = slug)
        except models.Discussion.DoesNotExist:
            print "Error retrieving the discussion for slug -> %s" % slug

        if request.user.is_authenticated():
            try:
                upvote = models.discussionUpvote.objects.get(discussion=discussion, analyser=models.Analyser.objects.get(user=request.user))
                discussion.upvotes -= 1
                discussion.save()
                owner = models.Analyser.objects.get(user=discussion.analyser.user)
                owner.total_upvotes -= 1
                owner.save()
                upvote.delete()
                data = {'upvotes':discussion.upvotes}
                return JsonResponse(data)

            except models.discussionUpvote.DoesNotExist:
                models.discussionUpvote.objects.create(discussion = discussion, analyser=models.Analyser.objects.get(user=request.user))
                discussion.upvotes += 1
                discussion.save()
                owner = models.Analyser.objects.get(user=discussion.analyser.user)
                owner.total_upvotes += 1
                owner.save()
                data = {'upvotes':discussion.upvotes}
                return JsonResponse(data)

def SetUpvoteDiscussionReply(request, slug=''):
    if request.method == 'GET':
        try:
            print "Retrieved the discussor for slug -> %s" % slug
            discussor =  models.Discussor.objects.get(slug = slug)
        except models.Discussor.DoesNotExist:
            print "Error retrieving the discussor for slug -> %s" % slug

        if request.user.is_authenticated():
            try:
                upvote = models.discussionReplyUpvote.objects.get(discussionReply=discussor, analyser=models.Analyser.objects.get(user=request.user))
                discussor.upvotes -= 1
                discussor.save()
                #TODO:For now lets not increse user's upvote by one for upvoting his reply
                #owner = models.Analyser.objects.get(user=discussor.analyser.user)
                #owner.total_upvotes -= 1
                #owner.save()
                upvote.delete()
                data = {'upvotes':discussor.upvotes}
                return JsonResponse(data)

            except models.discussionReplyUpvote.DoesNotExist:
                models.discussionReplyUpvote.objects.create(discussionReply = discussor, analyser=models.Analyser.objects.get(user=request.user))
                discussor.upvotes += 1
                discussor.save()
                #TODO:For now lets not increse user's upvote by one for upvoting his reply
                #owner = models.Analyser.objects.get(user=discussor.analyser.user)
                #owner.total_upvotes += 1
                #owner.save()
                data = {'upvotes':discussor.upvotes}
                return JsonResponse(data)


isNotification = False


def testNotif(request):
    global isNotification
    isNotification = True


def NotificationManager(request):
    global isNotification
    while not isNotification:
        time.sleep(10)
        #time.sleep(1)

    #get all notification and show the ones with updated==FALSE
    global isNotification
    isNotification = False
    return JsonResponse({'notification':'Yaay! you have a notification.'})