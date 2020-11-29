import time

from reader import ReadFile
from configuration import ConfigClass
from parser_module import Parse
from indexer import Indexer
from searcher import Searcher
from preparser import Preparse
import re
from operator import itemgetter
import matplotlib.pyplot as plt
from scipy import special
import numpy as np
import json

import os
import utils

def run_engine(steemr=False):
    """

    :return:
    """
    number_of_documents = 0

    config = ConfigClass()
    r = ReadFile(corpus_path=config.get__corpusPath())
    persondic=utils.load_obj("persona_dic")
    p = Parse(persondic,steemr)
    #pre=Preparse()
    indexer = Indexer(config)
    start_time = time.time()
    #file_name='covid19_07-08.snappy.parquet'
    print("--- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    # Iterate over every document in the file
    for i in range(r.maxlen):
        documents_list = r.read_file()
        for idx, document in enumerate(documents_list[0]):
            # parse the document
            parsed_document = p.parse_doc(document)
            number_of_documents += 1
            # index the document data
            '''filename = "posting" + str(0) + ".json"
            with open(filename, "w+") as f:
                json.dump(p.personadic, f, indent=4, sort_keys=True)'''

            #print(number_of_documents)
            if number_of_documents%100000==0:
                print("--- %s seconds ---" % (time.time() - start_time))
            elif number_of_documents == 100000:
                print(number_of_documents)
            indexer.add_new_doc(parsed_document)
            if(number_of_documents==100000*100):
                break
        if (number_of_documents == 100000*100):
            break
    if(indexer.numofdocment!=0):
        indexer.saveondisk()
    lenofindx = len(indexer.inverted_idx)
    print("num of terms:",lenofindx)
    print("num of numterms:", indexer.postnumcounter)
    sortindexser=sorted(list(indexer.inverted_idx.items()),key=lambda item:item[1][1])
    print(sortindexser[0:10])
    print('\n\n')
    print(sortindexser[lenofindx-10:])
    sortindexser=[]
    #indexer.add_Persona_Dic(p.personadic)

    frequency = {}




    frequency = {key: value[1] for key, value in list(indexer.inverted_idx.items())}

    # convert value of frequency to numpy array


    freqs = list(frequency.values())
    freqs.sort(reverse=True)
    epsilon = 10 ** (-6.0)
    # enumerate the ranks and frequencies
    rf = [((r + 1)*epsilon, f) for r, f in enumerate(freqs)]
    rs, fs = zip(*rf)

    plt.clf()
    plt.xscale('log')
    plt.yscale('log')
    plt.title('Zipf plot')
    plt.xlabel('rank')
    plt.ylabel('frequency')
    plt.plot(rs, fs, 'r-')
    plt.show()
    print('Finished parsing and indexing. Starting to export files')
    #utils.save_obj(pre.personadic,"persona_dic")
    utils.save_obj(indexer.inverted_idx, "inverted_idx")
    utils.save_obj(indexer.DocmentInfo, "Docment_info")
    utils.save_obj(indexer.postingNames, "postingNames")
    #utils.save_obj(indexer.postingDict, "posting")
    utils.save_obj(p.tweet2doc, "tweet2doc")

def load_index():
    print('Load inverted index')
    inverted_index = utils.load_obj("inverted_idx")
    return inverted_index

def doc_info():
    print('DocmentInfo index')
    Docment_info = utils.load_obj("Docment_info")
    return Docment_info

def search_and_rank_query(query, inverted_index, k,Docment_info=None,stemmer=False):
    persondic = utils.load_obj("persona_dic")
    p = Parse(persondic)
    query_as_list = p.parse_sentence(query)
    searcher = Searcher(inverted_index,Docment_info,persondic,stemmer)
    relevant_docs = searcher.relevant_docs_from_posting(query_as_list)
    ranked_docs = searcher.ranker.rank_relevant_doc(relevant_docs)
    return searcher.ranker.retrieve_top_k(ranked_docs, k)


def main():
    start_time = time.time()
    print("--- %s seconds ---" % (time.time() - start_time))
    run_engine(True)
    print("--- %s seconds ---" % (time.time() - start_time))
    query = "soaking up the sun in Spain may quarantine"#input("Please enter a query: ")
    k = 5#int(input("Please enter number of docs to retrieve: "))
    inverted_index = load_index()
    Docment_info= doc_info()
    start_time = time.time()
    for doc_tuple in search_and_rank_query(query, inverted_index, k,Docment_info,True):
        print('tweet id: {}, score (unique common words with query): {}'.format(doc_tuple[0], doc_tuple[1]))
    print("--- %s seconds ---" % (time.time() - start_time))