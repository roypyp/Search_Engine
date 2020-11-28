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

def wordSpertor(word):
    word=word.replace("/","")
    word = word.replace(",", "")
    if(len(word)<2):
        return False
    templist = [word]
    if "_" in word:
        word = word.replace("#", "")
        templist += word.split("_")
        templist=[x for x in templist if x]
    else:
        word = word.replace("#", "")
        if(word[0].isupper()):
            templist += re.findall('([A-Z][a-z]+)', word)
        else:
            templist += re.findall('([a-z]+)', word)
        for w in range(1,len(templist)):
            word=word.replace(templist[w],"")
        if len(word)!=0:
            templist+=[word]
    templist=[x.lower() for x in templist]


    return templist

def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')
'''def deEmojify(text):
    regrex_pattern = re.compile(pattern="[" \
        u"\U0001F600-\U0001F64F" \
        u"\U0001F300-\U0001F5FF" \
        u"\U0001F680-\U0001F6FF" \
        u"\U0001F1E0-\U0001F1FF" \
        "]+", flags=re.UNICODE)
    return regrex_pattern.sub(r'', text)'''

class Parse:

    def __init__(self,prsondic,stmmer=False):
        self.stop_words = stopwords.words('english')
        self.secondStop_word =['rt','i','p','etc','oh','im','also']
        #,'0','1','2','3','4','5','6','7','8','9'
        self.stop_words=self.stop_words+self.secondStop_word
        self.personadic =prsondic
        self.positiondic={}
        self.stmmer=stmmer
        self.stemmer= Stemmer()
        self.doc2bowcount=0
        self.tweetcount=0
        self.tweet2doc={}
        self.tweetlist=[]
        self.dictionary=[]

    def parse_sentence(self, text,tweetId=""):
        """
        This function tokenize, remove stop words and apply lower case for every word within the text
        :param text:
        :return:
        """
        nonBreakSpace = u'\xa0'
        text = text.replace(nonBreakSpace, ' ')
        #text_prsona = get_continuous_chunks(text)
        text=deEmojify(text)
     #   print(self.stop_words)
        ''' temptextlist=text.split(' ')
        for i in range(len(temptextlist)):
            if(self.positiondic.get(temptextlist[i])):
                self.positiondic[temptextlist[i]].append(i)
            else:
                self.positiondic[temptextlist[i]]=[i]'''

        '''text_tokens = word_tokenize(text)
        text_tokens_without_stopwords = [w.lower() for w in text_tokens if w not in self.stop_words]
        return text_tokens_without_stopwords'''

        return_parse=[]
        #text='RT @revathitweets: Will we 55.get any answers? #TelanganaCovidTruth #WhereIsKCR https://t.co/i8IdrIKp2B https://www.instagram.com/p/CD7fAPWs3WM/?igshid=o9kf0ugp1l8x'
        #text = 'RT #b.o.b. #matchedset… https://instagram.com/p/CCadwNjDKai/?igshid=1tfptbed95bln/… 5/5/2020 8/7/20'
        char_to_remove=['.',',','…','\n','?','/',' ','=']
        '''for char in char_to_remove:
            text=text.replace(char,'')'''
        numricset=['thousand','million','billion']
        webBuzzWord=["http","https","www"]
        text=re.sub('\.\.+', '.', text)
        text = re.sub('\_\_+', '_', text)
        text=text.replace('\r','')

        text = text.replace('\\', '')
        text_tokens = re.split("[ \-!?:=\n()$&`^\+\"'%;~*\|“…”{}\[\]‘]+",text)
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
            elif (text_tokens[word]==",,,"):
                word+=1
            elif(text_tokens[word].lower() in self.stop_words):
                word += 1
            elif (text_tokens[word][0]=='_' or text_tokens[word][0]==','):
                text_tokens[word]=text_tokens[word][1:]
            elif (text_tokens[word][0]).isupper():
                tempprona=text_tokens[word]
                temp = re.sub("[,_/.’#'\"]+", '', text_tokens[word])
                #return_parse+=[temp]
                word+=1
                while word < lenTokens and text_tokens[word]!="" and (text_tokens[word][0]).isupper():
                    temp = re.sub("[ _,/.’#'\"]+", '', text_tokens[word])
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
                    if(self.personadic.get(text)):
                        if(self.personadic[text]>1):
                            return_parse +=[text]
                        if(len(text.split(" "))>1):
                            for txt in text.split(" "):
                                if(self.personadic.get(txt)):
                                    txt = re.sub("[,_/.’#'\"]+", '', txt)
                                    return_parse +=[txt]
                                else:
                                    if(txt.lower() not in self.stop_words):
                                        txt = re.sub("[,/_.’#'\"]+", '', txt)
                                        return_parse += [txt.lower()]
                    else:
                        for txt in text.split(" "):
                            if(self.personadic.get(txt)):
                                txt = re.sub("[,/.’#'\"]+", '', txt)
                                return_parse +=[txt]
                            else:
                                if (txt.lower() not in self.stop_words):
                                    txt = re.sub("[,/.’#'\"]+", '', txt)
                                    return_parse += [txt.lower()]
                ''' if(self.personadic.get(text)):
                        if(self.personadic[text][2].get(tweetId)):
                            self.personadic[text][2][tweetId] += 1
                            self.personadic[text][1]+=1
                        else:
                            self.personadic[text][2][tweetId] = 1
                            self.personadic[text][0] += 1
                            self.personadic[text][1] += 1
                    else:
                        tempdic = {}
                        tempdic[tweetId] = 1
                        self.personadic[text] =[1,1,tempdic]'''

            elif re.match(r'^\d{1,2}\.\d{1,2}\.\d{2,4}$',text_tokens[word]) or re.match(r'^\d{1,2}\/\d{1,2}\/\d{2,4}$',text_tokens[word]):
                temp=text_tokens[word]
                if('.' in text_tokens[word]):
                    temp=text_tokens[word].replace('.','/')
                return_parse += [temp]
                word += 1
            elif text_tokens[word][0]=='#':

                if len(text_tokens[word])!=1:
                    if text_tokens[word].count('#') != 1:
                        temp=text_tokens[word].replace('#', '')
                        if temp!="":
                            return_parse += [temp]
                    else:
                        temp = re.sub("[ \-./:=\n()\"'~*\|“…”{}\[\]]+", '', text_tokens[word])
                        spertor=wordSpertor(temp)
                        if(spertor!=False):
                            return_parse+=wordSpertor(temp)
                word += 1
            elif text_tokens[word] in webBuzzWord and lenTokens>word+1:
                if(text_tokens[word] not in ['http','https']):
                    return_parse+=[text_tokens[word]]
                tempUrl=text_tokens[word+1].split('/')
                tempUrl=[x for x in tempUrl if x]
                if len(tempUrl)==0:
                    word += 2
                    continue
                if 'www' in tempUrl[0]:
                    tempw = tempUrl[0].split('.')
                    if(len(tempw)>2):
                        return_parse += [tempw[0]]
                        return_parse += [tempw[1]+'.' + tempw[2]]
                        for i in range(1,len(tempUrl)):
                            if(len(tempUrl[i])>2):
                                return_parse +=[tempUrl[i]]
                    else:
                        return_parse += [tempw[0]]
                        if(len(tempw)==2):
                            return_parse += [tempw[1]]
                else:
                    return_parse += [tempUrl[0]]
                    for i in range(1,len(tempUrl)):
                        if (len(tempUrl[i]) > 2):
                            return_parse +=[tempUrl[i]]

                word += 2
            elif (text_tokens[word].replace('.','').isnumeric()) and word+1<lenTokens and (text_tokens[word+1]=='percent' or text_tokens[word+1]=='percentage'):
                return_parse += [text_tokens[word]+'%']
                word += 2
            elif text_tokens[word].isdigit() and lenTokens>word+1 and text_tokens[word + 1].replace("/", "").isdigit() and text_tokens[word + 1].count("/") == 1:
                return_parse += [text_tokens[word] + " " + text_tokens[word + 1]]
                word += 2
            elif (text_tokens[word].replace("/", "").isdigit() and text_tokens[word].count("/") == 1):
                return_parse += [text_tokens[word]]
                word += 1
            elif (text_tokens[word].replace('.','').isnumeric()) and word+1<lenTokens and (text_tokens[word+1].lower() in numricset ):
                temp=text_tokens[word+1].lower();
                if('.' not in(text_tokens[word].replace(",",""))):
                    num=int(text_tokens[word].replace(",", ""))
                else:
                    num=float(text_tokens[word].replace(",",""))
                    num = round(num, 3)
                if(temp=='billion'):
                    return_parse += [ str(num) + 'B']
                elif(temp=='million'):
                    return_parse += [ str(num)  + 'M']
                else:
                    return_parse += [ str(num)  + 'K']
                word += 2
            elif (text_tokens[word].replace(",","").replace('.','').isdigit() and text_tokens[word].count(".")<=1):
                temp = float(text_tokens[word].replace(",",""))
                if temp>=1000000000:
                    if(temp%1000000000==0):
                        temp= int(temp/1000000000)
                    else:
                        temp=temp/1000000000
                        temp = round(temp, 3)
                    return_parse += [str(temp) + 'B']
                elif temp>=1000000:
                    if (temp % 1000000 == 0):
                        temp = int(temp / 1000000)
                    else:
                        temp = temp / 1000000
                        temp = round(temp, 3)
                    return_parse += [str(temp) + 'M']
                elif temp>=1000:
                    if (temp % 1000 == 0):
                        temp = int(temp / 1000)
                    else:
                        temp = temp / 1000
                        temp = round(temp, 3)
                    return_parse += [str(temp) + 'K']
                else:
                    if (temp % 1 == 0):
                        temp = int(temp / 1)
                    else:
                        temp = temp / 1
                        temp = round(temp, 3)
                    return_parse += [ str(temp) ]
                word += 1

            else:
                temp=re.sub("[,/.’#/'\"]+",'',text_tokens[word])
                if(temp!=""):
                    return_parse+=[temp]
                word += 1
        #return_parse = [w for w in return_parse if w.lower() not in self.stop_words]
        if(self.stmmer):
            return_parse = self.stemmer.stem_terms(return_parse)
        return return_parse

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
        tokenized_text = [x for x in tokenized_text if x]
        strtemp = ""
        '''for i in range(len(tokenized_text)):
            if ((tokenized_text[i][0]).isupper()):
                if (strtemp == ""):
                    strtemp = tokenized_text[i]
                else:
                    strtemp += " " + tokenized_text[i]
            else:
                if (strtemp != ""):
                    if (self.personadic.get(strtemp)):
                        if(tweet_id not in self.personadic[strtemp]):
                            self.personadic[strtemp].append(tweet_id)
                    else:
                        self.personadic[strtemp] = [tweet_id]
                    strtemp = ""
        if (self.personadic.get(strtemp)):
            if (tweet_id not in self.personadic[strtemp]):
                self.personadic[strtemp].append(tweet_id)
        else:
            self.personadic[strtemp] = [tweet_id]'''


        doc_length = len(tokenized_text)  # after text operations.
        ''' if self.doc2bowcount==0:
            self.dictionary = Dictionary([tokenized_text])
        else:
            self.dictionary.add_documents([tokenized_text])

        self.tweet2doc[self.tweetcount]=tweet_id
        self.tweetcount+=1
        self.tweetlist+=[tokenized_text]
        self.doc2bowcount+=1
        if(self.doc2bowcount==100000):
            self.dictionary.save('dictionary'+str(self.tweetcount))
            utils.save_obj(self.tweetlist,'tweetlist'+str(self.tweetcount))
            self.tweetlist=[]
            self.doc2bowcount=0'''

        maxFrecinDoc= 0
        docWordCount=0
        for term in tokenized_text:
            if(len(term)<2):
                continue
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1
            if(maxFrecinDoc<term_dict[term]):
                maxFrecinDoc= term_dict[term]
        infoForDoc = maxFrecinDoc
        document = Document(tweet_id, tweet_date, full_text, url, retweet_text, retweet_url, quote_text,
                            quote_url, term_dict, doc_length, infoForDoc)

        return document


