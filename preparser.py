from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import LancasterStemmer
from document import Document
import re
from stemmer import Stemmer
from gensim.corpora import Dictionary
import utils


from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree

def get_continuous_chunks(text):
    chunked = ne_chunk(pos_tag(word_tokenize(text)))
    continuous_chunk = []
    current_chunk = []
    for i in chunked:
         if type(i) == Tree:
                 current_chunk.append(" ".join([token for token, pos in i.leaves()]))
         if current_chunk:
                 named_entity = " ".join(current_chunk)
                 if named_entity not in continuous_chunk:
                         continuous_chunk.append(named_entity)
                         current_chunk = []
         else:
                 continue
    return continuous_chunk



def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')


class Preparse:

    def __init__(self,stmmer=False):
        self.stop_words = stopwords.words('english')
        self.secondStop_word =['rt','i','p','etc','oh','im','also']
        #,'0','1','2','3','4','5','6','7','8','9'
        self.stop_words=self.stop_words+self.secondStop_word
        self.personadic ={}
        self.terms={}


    def parse_sentence(self, text,tweetId=""):
        """
        This function tokenize, remove stop words and apply lower case for every word within the text
        :param text:
        :return:
        """
        nonBreakSpace = u'\xa0'
        text = text.replace(nonBreakSpace, ' ')
        if ('1280975647146496009' == tweetId):
            print(text)
            print(tweetId)
        text=deEmojify(text)

        return_parse=[]
        ifprsona={}
        text=re.sub('\.\.+', '.', text)
        text=text.replace('\r','')
        text_tokens = re.split("[ \-!?:=\n()$&^\+\"';~*\|“…”{}\[\]‘]+",text)
        #text_tokens= self.stemmer.stem_term(text_tokens)

        word = 0
        lenTokens=len(text_tokens)
        while word < lenTokens:
            if (text_tokens[word].count('.') == 1):
                split = text_tokens[word].split('.')
                if (split[0].replace(',',"").isnumeric() and not (split[1].isnumeric())) or\
                        ((not split[0].isnumeric() and  (split[1].replace(',',"").isnumeric()))) or\
                        ((not (split[1].isnumeric())) and not (split[1].isnumeric())):
                    text_tokens[word]=split[0]
                    text_tokens.insert(word+1,split[1])
            if (text_tokens[word].count('/') == 1):
                split = text_tokens[word].split('/')
                if ((not (split[1].isnumeric())) and not (split[1].isnumeric())):
                    text_tokens[word]=split[0]
                    text_tokens.insert(word+1,split[1])
            if(len(text_tokens[word].replace("#",""))<2 and not text_tokens[word].isnumeric()):
                word+=1

            elif(text_tokens[word].lower() in self.stop_words):
                word += 1

            elif (text_tokens[word][0]).isupper():
                tempprona=text_tokens[word]
                temp = re.sub("[,/.’#'\"]+", '', text_tokens[word])
                #return_parse+=[temp]
                word+=1
                while word < lenTokens and text_tokens[word]!="" and (text_tokens[word][0]).isupper():
                    temp = re.sub("[ ,/.’#'\"]+", '', text_tokens[word])
                    #return_parse += [temp]
                    tempprona+=" " +text_tokens[word]
                    word+=1
                for text in tempprona.split(","):
                    if len(text) < 1:
                        continue
                    if(text[0]==" "):
                        text=text[1:]
                    if len(text) < 2:
                        continue
                    if(text.isnumeric()):
                        continue
                    if(not self.terms.get(text.lower())):
                        if(self.personadic.get(text)):
                            if(not ifprsona.get(text)):
                                self.personadic[text] += 1
                                ifprsona[text] = True
                        else:
                            self.personadic[text] =1
                            ifprsona[text]=True
            else:
                self.terms[text_tokens[word]]=True
                tempp=text_tokens[word][0].upper()+text_tokens[word][1:]
                if(self.personadic.get(tempp)):
                    self.personadic.pop(tempp)
                word+=1




    def parse_doc(self, doc_as_list):
        """
        This function takes a tweet document as list and break it into different fields
        :param doc_as_list: list re-preseting the tweet.
        :return: Document object with corresponding fields.
        """

        tweet_id = doc_as_list[0]
        tweet_date = doc_as_list[1]
        full_text = doc_as_list[2]
        url = doc_as_list[3]
        retweet_text = doc_as_list[4]
        retweet_url = doc_as_list[5]
        quote_text = doc_as_list[6]
        quote_url = doc_as_list[7]
        term_dict = {}
        tokenized_text = self.parse_sentence(full_text,tweet_id)



'''re.match(r'^\d{2}\.\d{2}\.\d{4}$',text_tokens[word]) or re.match(r'^\d{2}\.\d{2}\.\d{2}$',text_tokens[word]) or\
                    re.match(r'^\d{1}\.\d{2}\.\d{4}$',text_tokens[word]) or re.match(r'^\d{1}\.\d{2}\.\d{2}$',text_tokens[word]) or\
                    re.match(r'^\d{2}\.\d{1}\.\d{4}$',text_tokens[word]) or re.match(r'^\d{2}\.\d{1}\.\d{2}$',text_tokens[word]) or\
                    re.match(r'^\d{2}\/\d{2}\/\d{4}$',text_tokens[word]) or re.match(r'^\d{2}\/\d{2}\/\d{2}$', text_tokens[word]) or\
                    re.match(r'^\d{1}\/\d{2}\/\d{4}$',text_tokens[word]) or re.match(r'^\d{1}\/\d{2}\/\d{2}$', text_tokens[word]) or\
                    re.match(r'^\d{2}\/\d{1}\/\d{4}$',text_tokens[word]) or re.match(r'^\d{2}\/\d{1}\/\d{2}$', text_tokens[word]) or\
                    re.match(r'^\d{1}\.\d{1}\.\d{4}$',text_tokens[word]) or re.match(r'^\d{1}\.\d{1}\.\d{2}$',text_tokens[word]) or\
                    re.match(r'^\d{1}\/\d{1}\/\d{4}$',text_tokens[word]) or re.match(r'^\d{1}\/\d{1}\/\d{2}$',text_tokens[word]):'''