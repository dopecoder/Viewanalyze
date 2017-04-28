    def getMainIndex(self, docID, MainIndex):
        DOCID = docID
        i=0

        for key, value in self.UniqueKeywordDict.items():
            DOCPRESENCE = 0
            print key 
            if key in MainIndex:
                print "IF BEING EXECUTED"
                temp = MainIndex[key]
                for index, each in enumerate(temp):
                    if each[0] == DOCID:
                        DOCPRESENCE = 1
                        for val in value:
                            if val in each[1]:
                                print "Value %s already there for DocID %s" % (val, DOCID)
                                print temp
                            elif val not in each[1]:
                                print "Appending value to existing document"
                                MainIndex[key][index][1].append(val)
                                print temp

                print MainIndex

            else:
                print "ELSE BEING EXECUTED"
                DOCPRESENCE=2
                print i
                MainIndex.update({key:[[DOCID,value]]})
                i = i+1

            if key in MainIndex and DOCPRESENCE == 0:
                print "ENDIF BEING EXECUTED"
                temp = MainIndex[key]
                temp.append([DOCID, value])
                MainIndex[key] = temp
        
        return MainIndex



    def getMainIndex(self, docID, MainIndex):
        DOCID = docID

        for key, value in self.UniqueKeywordDict.items():
            DOCPRESENCE = 0
            if key not in MainIndex:
                print 'IF BEING EXECUTED'
                DOCPRESENCE = 1
                MainIndex.update({key:[[DOCID,value]]})
            else:
                print 'ELSE BEING EXECUTED'
                temp = MainIndex[key]
                for index, each in enumerate(temp):
                    if each[0] == DOCID:
                        DOCPRESENCE = 2
                        if index in each[1]:
                            print "Value %s already there for DocID %s" % (val, DOCID)
                        else:
                            MainIndex[key][index][1].append(val)
                print MainIndex

            if key in MainIndex and DOCPRESENCE == 0:
                print "ENDIF EXECUTING -> NEW DOC FOR A PRESENT KEYWORD"
                temp = MainIndex[key]
                temp.append([DOCID, value])
                MainIndex[key] = temp

        return MainIndex



def appendToMainIndex(docID, INDEX):

    for k, v in UniqueKeywordDict.items():

        if k in INDEX:
            for each in INDEX:
                for term in each:
                    if term[0] == docID:
                        
