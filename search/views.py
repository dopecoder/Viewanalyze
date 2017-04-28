from django.shortcuts import render
from .models import SearchData
from discussion.models import Analyser
from nltk.stem.porter import PorterStemmer
from exceptions import IOError
from collections import defaultdict
import math
from discussion.models import Discussion
from django.views.generic.base import View
from . import forms


"""
STRUCTURE OF THE INDEX : 

keywordList = ['keyword1', 'keyword2', 'keyword3'........]
UniqueKeywordList = ['uniquekeyword1', 'uniquekeyword2', 'uniquekeyword3',.......]
UniqueKeywordDict = {'uniquekeyword1':['pos1', 'pos2', 'pos3',......],.......}
DOCINSTANCE = DiscussinObject.pk or DiscussorObject.pk
MainIndex = {'keyword':[['docID1',['pos1','pos2',.....]],['docID2',['pos1','pos2',.....]],['docID3',['pos1','pos2',.....]],.......]}
"""


#porterstemmer object used for word stemming
stemmer = PorterStemmer()


class SearchIndexBuilder:

    def __init__(self):
        self.INDEX_FILE_NAME = 'SearchIndexFile'
        self.KeywordList = []
        self.UniqueKeywordList = []
        self.UniqueKeywordDict = {}
        self.Index = {}
        self.titleIndexFile = {}
        self.tf=defaultdict(list)     #term frequencies of terms in documents
        self.df=defaultdict(int)      #document frequencies of terms in the corpus
        self.idf = {}
        self.numDocuments=0
        self.norm = 0
        self.i = 0
        
        try:
                self.readIndex()
                self.i +=1
                print "Read request executed! Its the %sth time! wat the FuCk!!" % str(self.i)
        except IOError:
                print "There was problem with reading the index"
                

    def setKeywordList(self, content):
        self.KeywordList = ''.join(e for e in content.lower() if e.isalnum() or e.isspace()).split()
        self.KeywordList = [stemmer.stem(word) for word in self.KeywordList]
        

    def setUniqueKeywordList(self):
        for keyword in self.KeywordList:
            if keyword not in self.UniqueKeywordList:
                self.UniqueKeywordList.append(keyword)
                

    def setUniqueKeywordDict(self):
        for keyword in self.UniqueKeywordList:
            for index, anotherkey in enumerate(self.KeywordList):
                if keyword == anotherkey:
                    if keyword in self.UniqueKeywordDict:
                        temp = self.UniqueKeywordDict[keyword]
                        temp.append(index)
                        self.UniqueKeywordDict[keyword] = temp
                    else:
                        self.UniqueKeywordDict.update({keyword:[index]})

        #normalize the document vector
        self.norm=0
        for term, posting in self.UniqueKeywordDict.iteritems():
            self.norm+=len(posting)**2
        self.norm=math.sqrt(self.norm)
            
        #calculate the tf and df weights
        #for term, posting in self.UniqueKeywordDict.iteritems():
        #    self.tf[term].append('%.4f' % (len(posting)/norm))
        #    self.df[term]+=1


    def getMainIndex(self, docID):
        DOCID = docID

        for key, value in self.UniqueKeywordDict.items():
            DOCPRESENCE = 0
            if key not in self.Index:
                print 'IF BEING EXECUTED'
                DOCPRESENCE = 1
                self.Index.update({key:[[DOCID,value]]})
            else:
                print 'ELSE BEING EXECUTED'
                #temp = self.Index[key]
                for index, each in enumerate(self.Index[key]):
                    if each[0] == DOCID:
                        DOCPRESENCE = 2
                        for anotherIndex, val in enumerate(value):
                            anotherIndex += each[1][-1] 
                            if val in each[1]:
                                print "Value %s already there for DocID %s" % (val, DOCID)
                            else:
                                print "End Else being executed" 
                                tempvalues = self.Index[key][index][1]
                                tempvalues.append(val)
                                self.Index[key][index][1]=tempvalues

            if key in self.Index and DOCPRESENCE == 0:
                print "ENDIF EXECUTING -> NEW DOC FOR A PRESENT KEYWORD"
                temp = self.Index[key]
                temp.append([DOCID, value])
                self.Index[key] = temp


            #calculate and update the tf and df values
            self.tf[key].append('%.4f' % (len(value)/self.norm))
            #update the document frequency only if the document is different
            if DOCPRESENCE == 0 or DOCPRESENCE == 1:
                self.df[key]+=1


    def writeIndexToFile(self):
        '''write the index to the file'''
        #write main inverted index
        f=open(self.INDEX_FILE_NAME, 'w')
        #first line is the number of documents
        print >>f, self.numDocuments
        self.numDocuments=int(self.numDocuments)
        for term in self.Index.iterkeys():
            postinglist=[]
            for p in self.Index[term]:
                docID=p[0]
                positions=p[1]
                postinglist.append(':'.join([str(docID) ,','.join(map(str,positions))]))
            #print data
            postingData=';'.join(postinglist)
            tfData=','.join(map(str,self.tf[term]))
            dfData = str(self.df[term])
            idfData='%.4f' % (self.numDocuments/self.df[term])
            print >> f, '|'.join((term, postingData, tfData, dfData, idfData))
        f.close()
        
        #write title index
        #f=open(self.titleIndexFile,'w')
        #for pageid, title in self.titleIndex.iteritems():
        #    print >> f, pageid, title
        #f.close()


    def readIndex(self):
        #read main index
        f=open(self.INDEX_FILE_NAME, 'r');
        #first read the number of documents
        try:
            self.numDocuments=int(f.readline().rstrip())
        except:
            print("The file is either empty or there was problem reading it.")

        for line in f:
            line=line.rstrip()
            term, postings, tf, df, idf = line.split('|')    #term='termID', postings='docID1:pos1,pos2;docID2:pos1,pos2'
            postings=postings.split(';')        #postings=['docId1:pos1,pos2','docID2:pos1,pos2']
            postings=[x.split(':') for x in postings] #postings=[['docId1', 'pos1,pos2'], ['docID2', 'pos1,pos2']]
            postings=[ [int(x[0]), map(int, x[1].split(','))] for x in postings ]   #final postings list  
            self.Index[term]=postings
            #read term frequencies
            tf=tf.split(',')
            self.tf[term]=map(float, tf)
            #read term frequencies
            self.df[term]=int(df)
            #read inverse document frequency
            self.idf[term]=float(idf)
        f.close()
        
        #read title index
        #f=open(self.titleIndexFile, 'r')
        #for line in f:
        #    pageid, title = line.rstrip().split(' ', 1)
        #    self.titleIndex[int(pageid)]=title
        #f.close()


    def mainfunc(self, content, docID):
        self.KeywordList = []
        self.UniqueKeywordList = []
        self.UniqueKeywordDict = {}
        self.norm = 0

        self.setKeywordList(content)
        self.setUniqueKeywordList()
        self.setUniqueKeywordDict()
        
        self.numDocuments+=1
        self.getMainIndex(docID)
        self.writeIndexToFile()


IndexSearch = SearchIndexBuilder()

def getIndexInstance():
    global IndexSearch
    if IndexSearch:
        print "IF INDEX EXECUTED"
        return IndexSearch
    else:
        print "ELSE INDEX EXECUTED"
        IndexSearch = SearchIndexBuilder()
        return IndexSearch


###############################################################################################################################
#SEARCH QUERY
###############################################################################################################################


class SearchQueryBuilder:

    def __init__(self):
        self.documentIntersection = []
        self.posIntersectionSet = []
        self.termSet = []
        self.presentDocs = []
        self.Priority_1 = []
        self.Priority_2 = []
        self.Priority_3 = []
        self.Set = []
        self.docScores = []
        self.rankedDocs = []

        self.Index = {}
        self.tf = {}      #term frequencies
        self.idf = {}    #inverse document frequencies

        self.search = getIndexInstance()
        self.Index = self.search.Index
        self.tf = self.search.tf
        self.idf = self.search.idf


    def getTermPresence(self, search_term, index):
        count = 0
        for word in search_term:
            if word in index:
                count = count+1

        print "SEARCH_TERM -> %s, %s" % (len(search_term),count)
        #if len(search_term) > 0:#== count:
        if count > 0:
            return True
        else:
            return False


    def getIndexTerm(self, search_term, index):
        #make sure the function is called only after the getTermPresence is True
        terms = []
        for word in search_term:
            if word in index:
                terms.append(index[word])
        print "Terms -> %s" % terms
        return terms


    def priorityDecider(self, search_term, index):

        if self.getTermPresence(search_term=search_term, index=index):
            for term in search_term:
                for val in index[term]:
                    self.documentIntersection.append(val[0])
                    self.termSet.append(val)
            return ['priority-1', 'priority-2', 'priority-3']
        else:
            return ['priority-2', 'priority-3']


    def getDocIntersection(self, IntersectionList):
        docs = []
        for index, term in enumerate(IntersectionList):
            for secondaryindex, secondterm in enumerate(term):
                y = []
                y.append(secondterm[0])
            docs.append(y)

        print "docs -> %s" % docs
        if docs:
            intersection = docs[0]
            for each in docs:
                intersection = set(intersection).intersection(each)
        return list(intersection)


    def getPosIntersection(self, docID, terms):
        for ID in docID:
            for term in terms:
                for actualTerm in term:
                    if ID == actualTerm[0]:
                        self.posIntersectionSet.append(actualTerm[1])

            print "DOCID -> %s" % (docID)        
            print "posIntersectionSet -> %s" % (self.posIntersectionSet)

            intersection = self.posIntersectionSet[0]

            print "intersection -> %s" % intersection
            
            for index, pos in enumerate(self.posIntersectionSet):
                if index > 0:
                    for secondIndex, val in enumerate(pos):
                        #Set[secondIndex] = pos[secondIndex] - index
                        self.Set.append(pos[secondIndex]-index)

                    print "Set -> %s" % self.Set
                    intersection = set(intersection).intersection(self.Set)
                else:
                    intersection = set(intersection).intersection(intersection)
                self.Set = []

            if intersection:
                if ID not in self.presentDocs:
                    print "Pos intersection -> %s" % intersection
                    self.presentDocs.append(ID)
        
        #read title index
        #f=open(self.titleIndexFile, 'r')
        #for line in f:
        #    pageid, title = line.rstrip().split(' ', 1)
        #    self.titleIndex[int(pageid)]=title
        #f.close()


    def getSearchStopTerm(self, search_term_list):
        p2_Search_term = []
        from nltk.corpus import stopwords
        stops = set(stopwords.words('english'))
        for word in search_term_list:
            if word not in stops:
                if word not in p2_Search_term:
                    p2_Search_term.append(word)
        return p2_Search_term  


    def getStemmedSearchTerm(self, search_term_list): 
        search_term_list = [stemmer.stem(word) for word in search_term_list]
        return search_term_list     


    def getSearchTerm(self, search_term):
        search_term = ''.join(word for word in search_term.lower() if word.isalnum() or word.isspace()).split()
        return search_term


    def dotProduct(self, vec1, vec2):
        if len(vec1)!=len(vec2):
            return 0
        return sum([ int(x)*int(y) for x,y in zip(vec1,vec2) ])
            
        
    def rankDocuments(self, terms, docs):
        #term at a time evaluation
        docVectors=defaultdict(lambda: [0]*len(terms))
        queryVector=[0]*len(terms)
        for termIndex, term in enumerate(terms):
            if term not in self.Index:
                continue

            if termIndex not in queryVector:
                continue

            queryVector[termIndex]=self.idf[term]
            
            for docIndex, (doc, postings) in enumerate(self.Index[term]):
                if doc in docs:###Need to replace the docs here
                    docVectors[doc][termIndex]=self.tf[term][docIndex]
                    
        #calculate the score of each doc
        docScores=[ [self.dotProduct(curDocVec, queryVector), doc] for doc, curDocVec in docVectors.iteritems() ]
        docScores.sort(reverse=True)
        resultDocs=[x[1] for x in docScores][:10]
        #print document titles instead if document id's
        #resultDocs=[ self.titleIndex[x] for x in resultDocs ]
        print 'resultDocs -> %s' % resultDocs
        return resultDocs



    def priority_1_set(self, search_term, index):
        searchTerm = self.getSearchTerm(search_term)
        searchTermStemmed = self.getStemmedSearchTerm(searchTerm)
        print "SearchTerm -> %s" % searchTermStemmed
        if self.getTermPresence(searchTermStemmed, index):
            Terms = self.getIndexTerm(searchTermStemmed, index)
            docIntersection = self.getDocIntersection(Terms)
            print "docIntersection -> %s" % docIntersection
            #Terms = self.getIndexTerm(searchTermStemmed, index)
            #print Terms
            self.getPosIntersection(docIntersection, Terms)

        if self.presentDocs:
            print self.presentDocs
            self.Priority_1.extend(self.presentDocs)


    def priority_2_set(self, search_term, index):
        searchTerm = self.getSearchTerm(search_term)

        if len(searchTerm) > 1:
            searchTermStop = self.getSearchStopTerm(searchTerm)
            searchTermStopStemmed = self.getStemmedSearchTerm(searchTermStop)
        else:
            searchTermStopStemmed = self.getStemmedSearchTerm(searchTerm)

        print "StopTerm -> %s" % searchTermStopStemmed
        if self.getTermPresence(searchTermStopStemmed, index):
            TermsStop = self.getIndexTerm(searchTermStopStemmed, index)
            docIntersectionStop = self.getDocIntersection(TermsStop)

            if docIntersectionStop:
                self.Priority_2.extend(docIntersectionStop) #we have the main terms in a single documents


    def priority_3_set(self, search_term, index):
        #priority 3
        #we need to get the terms of each word in different variable
        termsPro3 = [] #Holding the terms of all the Non-stop words
        searchTerm = self.getSearchTerm(search_term)
        print "---------PRIORITY_3_TEST---------"
        print "SEARCH-TERM -> %s" % searchTerm

        if len(searchTerm) > 1:
            print "LEN > 1"
            searchTermStop = self.getSearchStopTerm(searchTerm)
            print "SEARCH-TERM-STOP -> %s" % searchTermStop
            searchTermStopStemmed = self.getStemmedSearchTerm(searchTermStop)
            print "SEARCH-TERM-STOP-STEMMED -> %s" % searchTermStopStemmed
        else:
            print "LEN !> 1"
            searchTermStopStemmed = self.getStemmedSearchTerm(searchTerm)
            print "SEARCH-TERM-STOP-STEMMED -> %s" % searchTermStopStemmed

        if self.getTermPresence(searchTermStopStemmed, index):
            for word in searchTermStopStemmed:
                term = self.getIndexTerm([word], index)
                print "TERM -> %s" % term
                y = []
                for each in term:
                    y.append(each[0][0])
                    print "y -> %s" % y
                termsPro3.append(y)    

            if termsPro3:
                self.Priority_3.extend(termsPro3)


    def mainfunc(self, search_term):
        #TODO: need to include the ReplyIndex also to the querysystem

        self.Priority_1 = []
        self.Priority_2 = []
        self.Priority_3 = []
        self.documentIntersection = []
        self.posIntersectionSet = []
        self.termSet = []
        self.presentDocs = []
        self.Set = []
        self.Terms = []
        self.docScores = []
        self.rankedDocs = []

        
        self.priority_1_set(search_term, self.Index)
        self.priority_2_set(search_term, self.Index)
        self.priority_3_set(search_term, self.Index)

        print "Priority_1 -> %s" % self.Priority_1
        print "Priority_2 -> %s" % self.Priority_2
        print "Priority_3 -> %s" % self.Priority_3

        documentCollection = []
        if self.Priority_1:
            for docs in self.Priority_1:
                if docs not in documentCollection:
                    documentCollection.append(docs)
        if self.Priority_2:
            for docs in self.Priority_2:
                if docs not in documentCollection:
                    documentCollection.append(docs)
        if self.Priority_3:
            for docs in self.Priority_3:
                if docs not in documentCollection:
                    documentCollection.extend(docs)

        print "documentCollection -> %s" % documentCollection

        rankedDocs = []
        if documentCollection:
            searchTerm = self.getSearchTerm(search_term)
            stemmedTerm = self.getStemmedSearchTerm(searchTerm)
            rankedDocs = self.rankDocuments(stemmedTerm, documentCollection)

        #print "rankedDocs in ascending order -> %s" % rankedDocs
        if rankedDocs:
            return rankedDocs
        else:
            return None


#IndexSearch = SearchIndexBuilder()
QuerySearch = SearchQueryBuilder()

"""
def getIndexInstance():
    global IndexSearch
    if IndexSearch:
        print "ID INDEX EXECUTED"
        return IndexSearch
    else:
        print "ELSE INDEX EXECUTED"
        IndexSearch = SearchIndexBuilder()
        return IndexSearch"""

def getQueryInstance():
    global QuerySearch
    if QuerySearch:
        print "IF QUERY EXECUTED"
        return QuerySearch
    else:
        print "ELSE QUERY EXECUTED"
        QuerySearch = SearchQueryBuilder()
        return QuerySearch


##################################################################################################################
#Search Ranking
##################################################################################################################
"""
class DocRank:

    def dotProduct(self, vec1, vec2):
        if len(vec1)!=len(vec2):
            return 0
        return sum([ x*y for x,y in zip(vec1,vec2) ])
            
        
    def rankDocuments(self, terms, docs):
        #term at a time evaluation
        docVectors=defaultdict(lambda: [0]*len(terms))
        queryVector=[0]*len(terms)
        for termIndex, term in enumerate(terms):
            if term not in self.index:###Need to replace with the index
                continue
            
            queryVector[termIndex]=self.idf[term]
            
            for docIndex, (doc, postings) in enumerate(self.index[term]):###Need to replace with the index
                if doc in docs:###Need to replace the docs here
                    docVectors[doc][termIndex]=self.tf[term][docIndex]
                    
        #calculate the score of each doc
        docScores=[ [self.dotProduct(curDocVec, queryVector), doc] for doc, curDocVec in docVectors.iteritems() ]
        docScores.sort(reverse=True)
        resultDocs=[x[1] for x in docScores][:10]
        #print document titles instead if document id's
        resultDocs=[ self.titleIndex[x] for x in resultDocs ]
        print '\n'.join(resultDocs), '\n'"""

##################################################################################################################
#Searching
##################################################################################################################

class Search(View):

    def get(self, request):
        searchForm = forms.SearchForm()
        return render(request, 'search/search_form.html', {'form':searchForm})

    def post(self, request):
        form = forms.SearchForm(request.POST)

        if form.is_valid():
            cleanedForm = form.cleaned_data

            if self.request.user.is_authenticated():
                analyser = Analyser.objects.get(user=self.request.user)
                try:
                    searchdata = SearchData.objects.get(analyser=analyser, search_term=cleanedForm.get('search_field'))
                except SearchData.DoesNotExist:
                    searchdata = SearchData.objects.create(analyser=analyser, search_term=cleanedForm.get('search_field'))


            query = getQueryInstance()
            queryList = query.mainfunc(cleanedForm.get('search_field')) 

            print 'queryset -> %s' % queryList
            if queryList:
                discussionList = [] #= Discussion.objects.in_bulk(queryList)
                #print discussionList
                for query in queryList:
                    try:
                        discussionList.append(Discussion.objects.get(pk=query))
                    except Discussion.DoesNotExist:
                        pass

                form = forms.SearchForm()
                return render(request, 'search/search_form.html', {'form':form, 'discussions':discussionList, 'search_term': cleanedForm.get('search_field')})
            else:
                form = forms.SearchForm()
                return render(request, 'search/search_form.html', {'form':form, 'noResult':True})
        
        else:
            form = forms.SearchForm()
            return render(request, 'search/search_form.html', {'form':form})