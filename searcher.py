import math

from configuration import ConfigClass
from indexer import Indexer
from parser_module import Parse
from ranker import Ranker
import utils
from gensim.models import LsiModel
from gensim.models import LdaModel
from gensim.corpora import Dictionary
from gensim import similarities
import time
from nltk.corpus import wordnet
import numpy as np
from scipy import spatial

from stemmer import Stemmer


class Searcher:

    def __init__(self, inverted_index,Docment_info=None,persondic={},stemmer=False):
        """
        :param inverted_index: dictionary of inverted index
        """
        self.parser = Parse(persondic)
        self.ranker = Ranker()
        config = ConfigClass()
        self.indexer = Indexer(config)
        self.inverted_index = inverted_index
        self.Docment_info=Docment_info
        posting_name = utils.load_obj("postingNames")
        self.posting_name = sorted(posting_name)
        self.stemmerbool=stemmer
        self.stemmer = Stemmer()
        #self.termPlacement = {}


    def relevant_docs_from_posting(self, query):

        """
                This function loads the posting list and count the amount of relevant documents per term.
                :param query: query
                :return: dictionary of relevant documents.
                """
        queryexsp = []
        for word in query:
            if (self.stemmerbool):
                wname = self.stemmer.stem_term(word)
            else:
                wname = word
            queryexsp += [(wname, 1)]
            for syn in wordnet.synsets(word):
                w = wordnet.synsets(word)[0]
                for l in syn.lemmas():
                    if(self.stemmerbool):
                        lname=self.stemmer.stem_term(l.name())
                    else:
                        lname=l.name()
                    if l.name()==word or l.name().lower()==word or wname==lname:
                      queryexsp+=[(lname,1)]
                    else:
                        w2 = wordnet.synsets(l.name())[0]
                        score=w.wup_similarity(w2)
                        if(score!=None and score>0.5):
                            if(len(l.name().replace("_"," ").replace("-"," ").split())==1):
                                queryexsp.append((lname, score*0.9))
            #queryexsp = [t for t in queryexsp if t[1] != None]



        queryexsp = set(queryexsp)
        queryexsp = sorted(queryexsp, reverse=True, key=lambda item: item[0])
        print(queryexsp)
        posting_name = self.posting_name
        posting_name += ["number.json"]
        #sort_query = sorted(query)
        relevant_docs = {}
        tfidfdic={}
        i, t = 0, 0
        # listForName = list(tempdict.keys())
        while t < len(queryexsp):
            i = self.binarySearch(queryexsp[t][0],posting_name,i)
            tempdic = self.indexer.getJson(posting_name[i])
            if(tempdic.get(queryexsp[t][0])):
                for tweet in tempdic[queryexsp[t][0]].items():
                    if (tfidfdic.get(tweet[0])):
                        tfidfdic[tweet[0]][t] = ((tweet[1]) * math.log2(10000000 / self.inverted_index[queryexsp[t][0]][0]))*queryexsp[t][1]
                    else:
                        tfidfdic[tweet[0]] = [0] * len(queryexsp)
                        tfidfdic[tweet[0]][t] = ((tweet[1]) * math.log2(10000000 / self.inverted_index[queryexsp[t][0]][0]))*queryexsp[t][1]
            t+=1

        dq=[1]*len(queryexsp)
        dq=np.array(dq)
        dq=np.transpose(dq)
        A=np.array(list(tfidfdic.values()))
        tweets=list(tfidfdic.keys())
        cos_sim = np.dot(A, dq) / (np.linalg.norm(dq) * np.linalg.norm(A))
        #cos_sim=1 - spatial.distance.cosine(A, dq)
        tweetcos=zip(tweets,cos_sim)
        tweetcos=set(tweetcos)
        relevant_docs=sorted(tweetcos, reverse=True,key=lambda item:item[1])
        return relevant_docs
        '''for i in range(30):
            print(tweetcos[i])
            print(tweetcos[len(tweetcos)-i-1])'''


    def buildLsiModleimp(self):
        posting_name = self.posting_name
        posting_name += ["number.json"] +["persona.json"]
        i, t = 0, 0
        for term in self.inverted_index.keys():
            if(self.inverted_index[term][0]>7):
                self.termPlacement[term] = i
                i += 1
        tfidfdic = {}
        # listForName = list(tempdict.keys())
        while t < len(posting_name):
            # i = self.binarySearch(listiInvInx[t], posting_name, 0)
            tempdic = self.indexer.getJson(posting_name[t])
            for term in tempdic.keys():
                if(self.termPlacement.get(term)):
                    for tweet in tempdic[term].items():
                        if (tfidfdic.get(tweet[0])):
                            tfidfdic[tweet[0]][t] = (tweet[1] / self.Docment_info[tweet[0]][0]) * math.log2(1000 / self.inverted_index[term][0])
                        else:
                            tfidfdic[tweet[0]] = [0] * len(self.termPlacement)
                            tfidfdic[tweet[0]][t] = (tweet[1] / self.Docment_info[tweet[0]][0]) * math.log2(1000 / self.inverted_index[term][0])
            print(t)
            t += 1


        A = list(tfidfdic.values())
        print(len(A), ",", len(A[0]))
        print(len(self.termPlacement))
        return self.ranker.rank_relevant_doc(A)
    def buildLsiModle(self):
        posting_name=self.posting_name
        posting_name+=["number.json"]
        i, t = 0, 0
        # tempdict = {k: v for k, v in sorted(self.Docment_info.items(), key=lambda item: item[0])}
        tfidfdic = {}
        # listForName = list(tempdict.keys())
        while t < len(posting_name):
            #i = self.binarySearch(listiInvInx[t], posting_name, 0)
            tempdic = self.indexer.getJson(posting_name[t])
            for term in tempdic.keys():
                self.termPlacement[term]=i
                i += 1
                for tweet in tempdic[term].items():
                    if (tfidfdic.get(tweet[0])):
                        tfidfdic[tweet[0]][t] = (tweet[1] / self.Docment_info[tweet[0]][0]) * math.log2(1000 / self.inverted_index[term][0])
                    else:
                        tfidfdic[tweet[0]] = [0] * len(self.inverted_index)
                        tfidfdic[tweet[0]][t] = (tweet[1] / self.Docment_info[tweet[0]][0]) * math.log2(1000 / self.inverted_index[term][0])
            print(t)
            t+=1
        '''ip=0
        print(i)
        for term in self.inverted_index.keys():
            if not self.termPlacement.get(term):
                ip+=1
                print (term,"  ",ip)'''

        A = list(tfidfdic.values())
        print(len(A),",",len(A[0]))
        print(len(self.termPlacement))
        return self.ranker.rank_relevant_doc(A)
        #print(U)
        #print(S)
        #print(V)

    def binarySearch(self, term, posting_name, i):
        j = len(posting_name) - 1
        while j >= i:
            k = (j + i) // 2
            text = posting_name[k].replace(".json", "").split('-')
            if (term >= text[0] and term <= text[1]):
                return k
            else:
                if (term < text[0] and term < text[1]):
                    j = k - 1
                if (term > text[1]):
                    i = k + 1
        return False



'''posting = utils.load_obj("posting")
        relevant_docs = {}
        for term in query:
            try: # an example of checks that you have to do
                posting_doc = posting[term]
                for doc_tuple in posting_doc:
                    doc = doc_tuple[0]
                    if doc not in relevant_docs.keys():
                        relevant_docs[doc] = 1
                    else:
                        relevant_docs[doc] += 1
            except:
                print('term {} not found in posting'.format(term))
        return relevant_docs'''

'''start_time = time.time()
        dictionary= Dictionary.load('dictionary'+str(100000))
        listforcorp=utils.load_obj('tweetlist'+str(100000))
        tweet2doc = utils.load_obj("tweet2doc")
        for i in range(200000,10000000,100000):
            dictionary.merge_with(Dictionary.load('dictionary'+str(i)))
            listforcorp+=utils.load_obj('tweetlist'+str(i))
        corp=[]
        count=0
        for row in listforcorp:
          #  print(row," ",tweet2doc[count])
            count+=1
            corp+=[dictionary.doc2bow(row)]
        print("--- %s seconds ---" % (time.time() - start_time))
        lsi=LsiModel(corp,id2word=dictionary)
        lsi.save("LSIon10milon")
        print("--- %s seconds ---" % (time.time() - start_time))
        tweet2doc=utils.load_obj("tweet2doc")
        vec_bow = dictionary.doc2bow(query)
        vec_lsi = lsi[vec_bow]
        index = similarities.MatrixSimilarity(lsi[corp])
        index.save("LSIsimon10milon")
        sims = index[vec_lsi]
        #print(list(enumerate(sims)))
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        count=0
        for doc_position, doc_score in sims:
            print(doc_score, tweet2doc[doc_position])
            if(count==20):
                break
            count+=1
        print("--- %s seconds ---" % (time.time() - start_time))'''







'''Ut, St, Vt=self.buildLsiModleimp()
        i, t = 0, 0
        s=[]
        qvec=np.array([0]*len(self.termPlacement))
        while t < len(query):
            if(self.termPlacement.get(query[t])):
                qvec[self.termPlacement[query[t]]]=1
                print(self.termPlacement[query[t]],", ",qvec[self.termPlacement[query[t]]])
                s+=[self.termPlacement[query[t]]]
            t+=1
        #qvec=np.transpose(qvec)

        print(qvec.shape)
        print(Ut.shape)
        St = np.linalg.inv(St)
        print(St.shape)
        print(St)
        dq=np.matmul(qvec,Ut)
        num=qvec[s[0]]*Ut[s[0],0]+qvec[s[1]]*Ut[s[1],0]
        print(num,"=",qvec[s[0]],"*",Ut[s[0],0],"+",qvec[s[1]],"*",Ut[s[1],0])
        print(dq)
        dq=np.matmul(dq,St)
        print(dq)
        print(Vt.shape)

        cos_sim = np.dot(Vt, dq) / (np.linalg.norm(dq) * np.linalg.norm(Vt))
        print(cos_sim)
        print(cos_sim.shape)'''


"""
        This function loads the posting list and count the amount of relevant documents per term.
        :param query: query
        :return: dictionary of relevant documents.
        """
'''posting = utils.load_obj("posting")
        relevant_docs = {}
        for term in query:
            try: # an example of checks that you have to do
                posting_doc = posting[term]
                for doc_tuple in posting_doc:
                    doc = doc_tuple[0]
                    if doc not in relevant_docs.keys():
                        relevant_docs[doc] = 1
                    else:
                        relevant_docs[doc] += 1
            except:
                print('term {} not found in posting'.format(term))
        return relevant_docs'''

'''posting_name = utils.load_obj("postingNames")
        posting_name=sorted(posting_name)
        sort_query = sorted(query)
        i,t=0,0
        #tempdict = {k: v for k, v in sorted(self.Docment_info.items(), key=lambda item: item[0])}
        tfidfdic={}
        #listForName = list(tempdict.keys())
        while t<len(query):
            i = self.binarySearch(sort_query[t],posting_name,i)
            if(i!=False):
                tempdic=self.indexer.getJson(posting_name[i])
                tempdic2=tempdic[sort_query[t]]
                templist=list(tempdic2.items())
                for tweet in templist:
                    if(tfidfdic.get(tweet)):
                        tfidfdic[tweet[0]][t]=(tweet[1]/self.Docment_info[tweet[0]][0])*math.log2(60000/self.inverted_index[sort_query[t]][0])
                    else:
                        tfidfdic[tweet[0]]=[0]*len(query)
                        tfidfdic[tweet[0]][t] = (tweet[1] / self.Docment_info[tweet[0]][0]) * math.log2(60000 / self.inverted_index[sort_query[t]][0])
            t+=1
        print(tfidfdic)
        A=[]
        for val in tfidfdic.values():
            A.append(val)
        print(A)
        U,S,V=self.ranker.rank_relevant_doc(A)
        print(U)
        print(S)
        print(V)'''
