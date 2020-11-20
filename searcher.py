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
        self.indexer = Indexer()
        self.inverted_index = inverted_index
        self.Docment_info=Docment_info

    def relevant_docs_from_posting(self, query):
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

        posting_name = utils.load_obj("postingNames")
        sort_query = sorted(query)
        i,j=0,0
        tempdict = {k: v for k, v in sorted(self.Docment_info.items(), key=lambda item: item[0])}
        listForName = list(tempdict.keys())
        while i<len(query) and j<len(posting_name):
            text = self.postingNames[j].replace(".json", "").split('_')
            if(sort_query[i]>text[0] and sort_query[i]<text[1]):
                dict=self.indexer.getJson(posting_name[j])

