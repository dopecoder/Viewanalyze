from django.shortcuts import render
from django.http import HttpResponse
from discussion.models import Analyser
from django.views.generic.edit import CreateView
from . import models
from search import views as Search
from discussion.models import Discussion
from collections import OrderedDict
from operator import itemgetter

# Create your views here.

class DiscussionViewStore:
    #{analyser.pk:{discussion.pk:no_of_views, discussion.pk:no_of_views}}
    #{analuser.pk:[[discussion.pk, no_of_views], [discussion.pk, no_of_views], []]}
    ViewIndex={}


    def __init__(self):
        if self.ViewIndex == {}:
            try:
                self.readIndex()
            except:
                print("Error reading the file.")


    def updateIndex(self, analyserPk, discussionId):
        if analyserPk in self.ViewIndex:
            if discussionId in self.ViewIndex[analyserPk]:
                self.ViewIndex[analyserPk][discussionId] += 1
            else:
                self.ViewIndex[analyserPk].update({discussionId:1})
        else:
            self.ViewIndex.update({analyserPk:{discussionId:1}})

        self.writeToFile()


    def writeToFile(self):
        f=open('ViewData', 'w')

        for pk, views in self.ViewIndex.iteritems():
            analyserPk = str(pk)
            viewsPk = ''

            for a, b in views.iteritems():
                viewsPk = viewsPk + str(a)+':'+str(b)
                viewsPk = viewsPk +','

            #viewsPk = ','.join(view for view in views)
            
            print >> f, '|'.join((analyserPk, viewsPk[:-1]))
        f.close()


    def readIndex(self):
        f=open('ViewData', 'r');
        tags = self.ViewIndex
        for line in f:
            line=line.rstrip()
            analyserPk, viewsPk = line.split('|')    #term='termID', postings='docID1:pos1,pos2;docID2:pos1,pos2'
            views=viewsPk.split(',')        #postings=['docId1:pos1,pos2','docID2:pos1,pos2']

            tags.update({int(analyserPk):{}})
            #st=['12=34', '13=35']
            for kv in views:
                value = kv.split(':')
                tags[int(analyserPk)].update({int(value[0]):int(value[1])})
        
        f.close()

    
    def getDiscussionPk(self, analyserPk):
        x = []
        key=0
        val=0
        #d = OrderedDict(sorted(self.ViewIndex[analyserPk].items(), key=itemgetter(1)))
        #print 'OrderedDict -> %s' % d

        temp = self.ViewIndex[analyserPk].copy()
        actual = []
        temporary = []
        for x in xrange(0, len(temp)):
            count=0
            for k, v in temp.iteritems():
                if count == 0:
                    key=k
                    val=v
                else:
                    if v > val:
                        val = v
                        key = k
                count+=1
            actual.append(key)
            del temp[key]

        #for k,v in self.ViewIndex[analyserPk].iteritems():
        #    x.append(k)
        return actual


    def getUniqueQuerySet(self, queryset):
        views = []
        for view in queryset:
            if view not in views:
                views.append(view)
        return views


    def getPersonalizedQuerySet(self, analyserPk, viewSet):
        #viewSet = self.getDiscussionPk(analyserPk)
        print 'viewSet -> %s' % viewSet
        query = Search.getQueryInstance()
        views = []
        uniqueFirstView = []
        for view in viewSet:
            print 'view %d' % view
            try:
                discussion = Discussion.objects.get(pk=int(view))
                querySet = query.mainfunc(discussion.title)
                if querySet:
                    views.extend(querySet)
            except Discussion.DoesNotExist:
                pass

        uniqueViews = self.getUniqueQuerySet(views)

        #the already viewed discussions are omitted in the uniqueFirstView, which is returned actually to the user
        #the uniqueViews is unused after this point.

        discussions = Discussion.objects.filter(analyser = Analyser.objects.get(pk=analyserPk))
        discussionsPks = []
        for discussion in discussions:
            discussionsPks.append(discussion.pk)

        print "USERS OWN DISCUSSION PKS -> %s" % discussionsPks

        print "USERS VIEWINDEX PKS -> %s" % self.ViewIndex[analyserPk]

        print "USERS UNIQUEVIEWS PKS -> %s" % uniqueViews

        for discussion in uniqueViews:
            if discussion not in self.ViewIndex[analyserPk]: #excluding the common ones and including only the unique ones form the list
                if discussion not in discussionsPks: #excluding the user's own discussions
                    uniqueFirstView.append(discussion)

        print "uniqueViews -> %s" % uniqueViews
        print "uniqueFirstView -> %s" % uniqueFirstView

        if uniqueFirstView == []:
            return (uniqueViews[:5], 1) #returning the 1 flag to check that uniqueFirstView was not returned.
        else:
            # noinspection PyArgumentList
            uniqueFirstView.extend(uniqueViews[0:5])
            return uniqueFirstView, 0  #returning the 0 flag to check that uniqueFirstView was returned.


    def getDiscussion(self, queryPk):
        #if len(queryPk) == 1:
        #    try:
        #        return Discussion.objects.get(pk=queryPk)
        #    except Discussion.DoesNotExist:
        #        print "DISCUSSION OBJECT DOES NOT EXIST FOR PK -> %s" % queryPk
        #        return []

        clauses = ' '.join(['WHEN id=%s THEN %s' % (pk, i) for i, pk in enumerate(queryPk)])
        ordering = 'CASE %s END' % clauses
        queryset = Discussion.objects.filter(pk__in=queryPk).extra(select={'ordering': ordering}, order_by=('ordering',))
        return queryset

#class instantiation
viewstore = DiscussionViewStore()

#instance getter
def getViewStoreInstance():
    global viewstore
    if viewstore:
        print "IF EXECUTED IN PERSONALIZATION"
        print DiscussionViewStore.ViewIndex
        return viewstore
    else:
        print "ELSE EXECUTED IN PERSONALIZATION"
        viewstore = DiscussionViewStore()
        return viewstore


class Personalization:
    TagIndex = {}

    def __init__(self):
        i = 1
        if self.TagIndex == {}:
            try:
                self.readFromFile()
                print "this is the %sth time" % i
                i=i+1
            except:
                print("Error reading from the file.")

    #{'analyser.pk':{'st':[[tag1.pk,count], [tag2.pk, count]]}, {'tt':[[tag1.pk, count], [tag2.pk, count]]}}
    #tags = {analyser.pk:{'st':{tag.pk:3,tag.pk:6,tag.pk:8},'tt':{tag.pk:3,tag.pk:5,tag.pk:7}}}


    def setPersonalizeTag(self, user, discussion):
        #return HttpResponse('Still working on it!')
        analyser = Analyser.objects.get(user=user)
        if analyser.pk in self.TagIndex:
            for tags in discussion.secondary_tag.all():
                if tags.pk in self.TagIndex[analyser.pk]['st']:
                    self.TagIndex[analyser.pk]['st'][tags.pk] += 1;
                else:
                    self.TagIndex[analyser.pk]['st'].update({tags.pk:1})

            for tags in discussion.tertiary_tag.all():
                if tags.pk in self.TagIndex[analyser.pk]['tt']:
                    self.TagIndex[analyser.pk]['tt'][tags.pk] += 1;
                else:
                    self.TagIndex[analyser.pk]['tt'].update({tags.pk:1})

        else:
            self.TagIndex.update({analyser.pk:{'st':{},'tt':{}}})
            for tags in discussion.secondary_tag.all():
                self.TagIndex[analyser.pk]['st'].update({tags.pk:1})
            for tags in discussion.tertiary_tag.all():
                self.TagIndex[analyser.pk]['tt'].update({tags.pk:1})

        self.writeToFile()
        print 'TagIndex -> %s' % self.TagIndex


    def getPersonalizeTag(self, user):
        analyser = Analyser.objects.get(user=user)
        if analyser.pk in self.TagIndex:
            key=0
            val=0
            count=0

            data = self.TagIndex[analyser.pk]['st']
            d = OrderedDict(sorted(data.items(), key=itemgetter(0)))
            print 'st -> %s' % d

            data = self.TagIndex[analyser.pk]['tt']
            d = OrderedDict(sorted(data.items(), key=itemgetter(0)))
            print 'tt -> %s' % d

            for k, v in self.TagIndex[analyser.pk]['st'].iteritems():
                if count == 0:
                    key=k
                    val=v
                else:
                    if v > val:
                        val = v
                        key = k
                count+=1
            print 'st key -> %s' % key
            print 'st val -> %s' % val

            st_key = key

            count=0
            for k, v in self.TagIndex[analyser.pk]['tt'].iteritems():
                if count == 0:
                    key=k
                    val=v
                else:
                    if v > val:
                        val = v
                        key = k
                count+=1
            print 'tt key -> %s' % key
            print 'tt val -> %s' % val

            return st_key, key


    def writeToFile(self):

        #first seperately write the st and tt to the variables and at the end add it to the file
        #write main inverted index
        f=open('PersonalizationData', 'w')

        for pk, alltags in self.TagIndex.iteritems():
            #st tt and analyser
            analyserPK = str(pk)
            stTags = ''
            ttTags = ''
            for tagtype, tags in alltags.iteritems():
                #we the above loop runs two times
                for k, v in tags.iteritems():
                    if tagtype == 'st':
                        stTags += str(k)+'='+str(v)
                        stTags += ';'
                    elif tagtype == 'tt': 
                        ttTags += str(k)+'='+str(v)
                        ttTags += ';'

            print >> f, '|'.join((analyserPK, stTags[:-1], ttTags[:-1]))
        f.close()


    def readFromFile(self):
        #read main index
        f=open('PersonalizationData', 'r');
        #first read the number of documents
        #self.numDocuments=int(f.readline().rstrip())
        tags = self.TagIndex
        for line in f:
            line=line.rstrip()
            analyserPK, st, tt = line.split('|')    #term='termID', postings='docID1:pos1,pos2;docID2:pos1,pos2'
            st=st.split(';')        #postings=['docId1:pos1,pos2','docID2:pos1,pos2']
            tt=tt.split(';')

            tags.update({int(analyserPK):{'st':{},'tt':{}}})
            #st=['12=34', '13=35']
            for kv in st:
                value = kv.split('=')
                tags[int(analyserPK)]['st'].update({int(value[0]):int(value[1])})

            for kv in tt:
                value = kv.split('=')
                if analyserPK == '56':
                    print value
                tags[int(analyserPK)]['tt'].update({int(value[0]):int(value[1])})

            #postings=[x.split(':') for x in postings] #postings=[['docId1', 'pos1,pos2'], ['docID2', 'pos1,pos2']]
            #postings=[ [int(x[0]), map(int, x[1].split(','))] for x in postings ]   #final postings list  
            #self.Index[term]=postings
            #read term frequencies
            #tf=tf.split(',')
            #self.tf[term]=map(float, tf)
            #read term frequencies
            #self.df[term]=int(df)
            #read inverse document frequency
            #self.idf[term]=float(idf)
        f.close()

        """
        tags.update({int(analyserPK):{'st':{},'tt':{}}})
        #st=['12=34', '13=35']
        for kv in st:
            value = kv.split('=')
            tags[int(analyserPK)]['st'].update({int(value[0]):int(value[1])})

        for kv in tt:
            value = kv.split('=')
            tags[int(analyserPK)]['tt'].update({int(value[0]):int(value[1])})
        """

    #file save pattern:
    #analyser.pk|st:56=12;34=12;33=1;34=31|tt:21=6;34=14|

#class instantiation
personalization = Personalization()

#instance getter
def getPersonInstance():
    global personalization
    if personalization:
        print "IF EXECUTED"
        return personalization
    else:
        print "ELSE EXECUTED"
        personalization = SearchQueryBuilder()
        return personalization


#class PersonalizationCreateView(CreateView):
#    model = models.VisitedTags

#Create a method to analyse the visited pk's of the user and search the main keywords in the search index 
#and return the important discussions to the user.

def getPersonalizedQuerySet(user):
    pass
    #go through every discussion pk and append the title, content and filter the stopwords, -> stem it
    #get related discussions.

    #not too recent nor too old
    #main preference to no_of_replys and upvotes and activity -> weightage

    #step 1 : go through index and find all the replated discussions for each view
    #step 2 : rank the final pk list
    #step 3 : return the queryset   

def getRelatedDiscussion(pk):
    pass