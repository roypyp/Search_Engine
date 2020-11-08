from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import LancasterStemmer
from document import Document
import re


def fun1(word):
    templist = [word]
    if "_" in word:
        word = word.replace("#", "")
        templist += word.split("_")
        templist=[x for x in templist if x]
    else:
        word = word.replace("#", "")
        templist += re.findall('([A-Z][a-z]+)', word)
        for w in range(1,len(templist)):
            word=word.replace(templist[w],"")
        if len(word)!=0:
            templist+=[word]
    templist=[x.lower() for x in templist]

    return templist


class Parse:

    def __init__(self):
        self.stop_words = stopwords.words('english')
        #self.secondStop_word =[':',',','?','!','.',"'",'"',"of",'']
        #self.stop_words=self.stop_words+self.secondStop_word
        self.personadic ={}
        self.positiondic={}

    def parse_sentence(self, text):
        """
        This function tokenize, remove stop words and apply lower case for every word within the text
        :param text:
        :return:
        """
        #print(self.stop_words)
        temptextlist=text.split(' ')
        for i in range(len(temptextlist)):
            if(self.positiondic.get(temptextlist[i])):
                self.positiondic[temptextlist[i]].append(i)
            else:
                self.positiondic[temptextlist[i]]=[i]

        """text_tokens = word_tokenize(text)
        #text_tokens_without_stopwords = [w.lower() for w in text_tokens if w not in self.stop_words]
        return text_tokens_without_stopwords"""
        return_parse=[]
        #text='RT @revathitweets: Will we get any answers? #TelanganaCovidTruth #WhereIsKCR https://www.instagram.com/p/CD7fAPWs3WM/?igshid=o9kf0ugp1l8x  ½'
        text = 'RT 5 percent ½ 55.2165 @revathitweets: Will we, get. 1.05.2000 trouble troubling troubled'
        char_to_remove=['.',',','…','\n','?','/',' ','=']
        '''for char in char_to_remove:
            text=text.replace(char,'')'''
        numricset=['thousand','million','billion']
        text_tokens = re.split("[ \-!?:/=\n…]+",text)
        word = 0
        while word < len(text_tokens):
            if(text_tokens[word]==""):
                word+=1
            elif re.match(r'^\d{2}\.\d{2}\.\d{4}$',text_tokens[word]) or re.match(r'^\d{2}\.\d{2}\.\d{2}$',text_tokens[word] or \
                    re.match(r'^\d{2}\/\d{2}\/\d{4}$',text_tokens[word]) or  re.match(r'^\d{1}\.\d{2}\.\d{4}$',text_tokens[word]) or \
                    re.match(r'^\d{1}\.\d{2}\.\d{2}$',text_tokens[word]) or re.match(r'^\d{2}\.\d{1}\.\d{4}$',text_tokens[word]) or \
                    re.match(r'^\d{2}\.\d{1}\.\d{2}$',text_tokens[word]) ):
                return_parse += [text_tokens[word]]
                word += 1
            elif text_tokens[word][0]=='#':
                return_parse+=fun1(text_tokens[word])
                word += 1
            elif text_tokens[word]=='www':
                return_parse+=[text_tokens[word]]
                return_parse+= [text_tokens[word+1] + "." + text_tokens[word+2]]
                word += 3
            elif (text_tokens[word].replace('.','').isnumeric()) and word+1<len(text_tokens) and (text_tokens[word+1]=='percent' or text_tokens[word+1]=='percentage'):
                return_parse += [text_tokens[word]+'%']
                word += 2
            elif (text_tokens[word].replace('.','').isnumeric()) and word+1<len(text_tokens)and (text_tokens[word+1].lower() in numricset ):
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
            elif (text_tokens[word].replace(",","").replace('.','').isdigit()):

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
                temp=re.sub("[,.’]+",'',text_tokens[word])
                if(temp!=""):
                    return_parse+=[temp]
                word += 1
        text_tokens_without_stopwords = [w.lower() for w in return_parse if w not in self.stop_words]
        return text_tokens_without_stopwords

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
        tokenized_text = self.parse_sentence(full_text)
        strtemp = ""
        for i in range(len(tokenized_text)):
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
            self.personadic[strtemp] = [tweet_id]



        doc_length = len(tokenized_text)  # after text operations.

        tempstmeeing = []
        lancaster = LancasterStemmer()
        for w in tokenized_text:
            if (lancaster.stem(w) not in tempstmeeing):
                tempstmeeing += [lancaster.stem(w)]
        tokenized_text = tempstmeeing


        for term in tokenized_text:
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1


        document = Document(tweet_id, tweet_date, full_text, url, retweet_text, retweet_url, quote_text,
                            quote_url, term_dict, doc_length)
        return document
