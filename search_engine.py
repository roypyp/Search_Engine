import time

from reader import ReadFile
from configuration import ConfigClass
from parser_module import Parse
from indexer import Indexer
from searcher import Searcher
import json

import os
import utils

def run_engine():
    """

    :return:
    """
    number_of_documents = 0

    config = ConfigClass()
    r = ReadFile(corpus_path=config.get__corpusPath())
    p = Parse()
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
            if number_of_documents<=10000:
                print(number_of_documents)
            elif number_of_documents==1000000:
                print("--- %s seconds ---" % (time.time() - start_time))
            elif number_of_documents == 140205:
                print(number_of_documents)
            indexer.add_new_doc(parsed_document)
    print('Finished parsing and indexing. Starting to export files')

    utils.save_obj(indexer.inverted_idx, "inverted_idx")
    utils.save_obj(indexer.DocmentInfo, "Docment_info")
    utils.save_obj(indexer.postingNames, "postingNames")
    utils.save_obj(indexer.postingDict, "posting")


def load_index():
    print('Load inverted index')
    inverted_index = utils.load_obj("inverted_idx")
    return inverted_index

def doc_info():
    print('DocmentInfo index')
    Docment_info = utils.load_obj("Docment_info")
    return Docment_info

def search_and_rank_query(query, inverted_index, k,Docment_info=None):
    p = Parse()
    query_as_list = p.parse_sentence(query)
    searcher = Searcher(inverted_index,Docment_info)
    relevant_docs = searcher.relevant_docs_from_posting(query_as_list)
    ranked_docs = searcher.ranker.rank_relevant_doc(relevant_docs)
    return searcher.ranker.retrieve_top_k(ranked_docs, k)


def main():
    start_time = time.time()
    print("--- %s seconds ---" % (time.time() - start_time))
    run_engine()
    print("--- %s seconds ---" % (time.time() - start_time))
    query = input("Please enter a query: ")
    k = int(input("Please enter number of docs to retrieve: "))
    inverted_index = load_index()
    Docment_info= doc_info()
    for doc_tuple in search_and_rank_query(query, inverted_index, k,Docment_info):
        print('tweet id: {}, score (unique common words with query): {}'.format(doc_tuple[0], doc_tuple[1]))
