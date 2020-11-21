import math

from configuration import ConfigClass
from indexer import Indexer
from parser_module import Parse
from ranker import Ranker
import utils


class Searcher:

    def __init__(self, inverted_index,Docment_info=None):
        """
        :param inverted_index: dictionary of inverted index
        """
        self.parser = Parse()
        self.ranker = Ranker()
        config = ConfigClass()
        self.indexer = Indexer(config)
        self.inverted_index = inverted_index
        self.Docment_info=Docment_info


    def relevant_docs_from_posting(self, query):
        self.buildLsiModle()
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


    def buildLsiModle(self):
        posting_name = utils.load_obj("postingNames")
        posting_name = sorted(posting_name)
        posting_name+=["number.json"]
        i, t = 0, 0
        # tempdict = {k: v for k, v in sorted(self.Docment_info.items(), key=lambda item: item[0])}
        tfidfdic = {}
        # listForName = list(tempdict.keys())
        while t < len(posting_name):
            #i = self.binarySearch(listiInvInx[t], posting_name, 0)
            tempdic = self.indexer.getJson(posting_name[t])
            for term in tempdic.keys():
                for tweet in tempdic[term].items():
                    if (tfidfdic.get(tweet[0])):
                        tfidfdic[tweet[0]][t] = (tweet[1] / self.Docment_info[tweet[0]][0]) * math.log2(1000 / self.inverted_index[term][0])
                    else:
                        tfidfdic[tweet[0]] = [0] * len(self.inverted_index)
                        tfidfdic[tweet[0]][t] = (tweet[1] / self.Docment_info[tweet[0]][0]) * math.log2(1000 / self.inverted_index[term][0])
            print(t)
            t+=1

        A = list(tfidfdic.values())
        #print(A)
        U, S, V = self.ranker.rank_relevant_doc(A)
        #print(U)
        #print(S)
        #print(V)
    def binarySearch(self,term, posting_name,i):
        j=len(posting_name)-1
        while j>=i:
            k = (j + i) // 2
            text = posting_name[k].replace(".json", "").split('-')
            if(term>text[0] and term<text[1]):
                return k
            else:
                if(term<text[0]):
                    j=k
                if(term>text[1]):
                    i=k
        return False