import json
import math
import time

class Indexer:

    def __init__(self, config):
        self.inverted_idx = {}
        self.DocmentInfo={}
        self.postingDict = {}
        self.postingDictNum={}
        self.config = config
        self.numofdocment=0
        self.postingNames=[]
        self.firstposting=True
        #self.postCount = 0
        #self.maxTermInPost = 100
        #self.currnetRowInPost = 0
    ''' filename="posting" + str(self.postCount) + ".json"
        with open(filename, "w+") as f:
            data = {'terms': {}}
            json.dump(data, f)'''

    def replace_line(self,file_name, line_num, tweet_id ,f):
        lines = open(file_name, 'r').readlines()
        text=lines[line_num]
        textlist=text.split(',')
        text=textlist[0]
        bol=True
        for i in range(1,len(textlist)):
            if(int(textlist[i].split(" ")[0])>int(tweet_id)):
                text += ","+ tweet_id +" " +f
                bol=False
            text+=","+textlist[i].replace("\n","")
        if bol:
            text += "," + tweet_id + " " + f
        text+="\n"
        lines[line_num]=text
        out = open(file_name, 'w')
        out.writelines(lines)
        out.close()
    def fun1(self):
        tempdict = {k: v for k, v in sorted(self.postingDict.items(), key=lambda item: item[0])}
        sqrtofterm = math.ceil(len(tempdict) ** 0.5)
        listForName = list(tempdict.items())
        for i in range(0, len(tempdict), sqrtofterm):
            tempp=sqrtofterm + i-1
            if(tempp>=len(tempdict)):
                tempp=-1
            d1 = dict(listForName[i:tempp])
            filename = listForName[i][0] + "-" + listForName[tempp][0] + ".json"
            self.postingNames.append(filename)
            self.postingGenrate(filename, d1)

    def fun2(self):
        tempdict = {k: v for k, v in sorted(self.postingDict.items(), key=lambda item: item[0])}
        listForName = list(tempdict.keys())
        name=0
        i=0
        while i<len(listForName):
            if(name<len(self.postingNames)):
                text=self.postingNames[name].replace(".json","").split('_')
            if(listForName[i]<text[0]):
                firstname=listForName[i]
                tempdic = {}
                tempdic[listForName[i]] = tempdict[listForName[i]]
                print(i , " " , len(listForName))
                i+=1
                while i<len(listForName) and listForName[i]<text[0]:
                    tempdic[listForName[i]]=tempdict[listForName[i]]
                    i+=1
                    print(i , " " , len(listForName)," 1")
                filename=firstname+"-"+listForName[i-1]+".json"
                self.postingNames.insert(name,filename)
                self.postingGenrate(filename,tempdic)
                name+=1
            elif(listForName[i]>text[0] and listForName[i]<text[1]):
                print(i , " " , len(listForName))
                olddic=self.getJson(self.postingNames[name])
                while i<len(listForName) and listForName[i]<text[1]:
                    if olddic.get(listForName[i]):
                        self.appendDic(olddic,tempdict,listForName[i])#olddic[listForName[i]].append(tempdict[listForName[i]])
                    else:
                        olddic[listForName[i]]=tempdict[listForName[i]]
                    i+=1
                    print(i , " " , len(listForName)," 2")
                self.postingGenrate(self.postingNames[name],olddic)
                name+=1
            elif(name>len(self.postingNames)):
                print(i , " " , len(listForName)," 3")
                sqrtofterm = math.ceil(len(tempdict) ** 0.5)
                while i<len(listForName):
                    t=i
                    d1={}
                    for j in range(sqrtofterm):
                        if(i==len(listForName)):
                            break
                        d1[listForName[i]]=tempdict[listForName[i]]
                        i+=1
                    filename = listForName[t][0] + "-" + listForName[i-1][0] + ".json"
                    self.postingNames.append(filename)
                    self.postingGenrate(filename, d1)
            else:
                name+=1
        olddic = self.getJson("number.json")
        for key in self.postingDictNum.keys():
            if olddic.get(key):
                self.appendDic(olddic,self.postingDictNum,key)
            else:
                olddic[key] = self.postingDictNum[key]
        self.postingGenrate("number.json", olddic)

    def appendDic(self,dic1,dic2,term):
        dic1[term].update(dic2[term])

    def getJson(self,filename):
        with open(filename, "r+") as f:
            tempdic=json.load(f)
        return tempdic
    def postingGenrate(self,filename, dic):
        with open(filename, "w+") as f:
            json.dump(dic, f, indent=4, sort_keys=True)


    def add_new_doc(self, document):
        """
        This function perform indexing process for a document object.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param document: a document need to be indexed.
        :return: -
        """

        document_dictionary = document.term_doc_dictionary
        # Go over each term in the doc
        self.numofdocment += 1
        for term in document_dictionary.keys():
            uniWordCount=0
            if(document_dictionary[term]==1):
                uniWordCount+=1
            try:

                # Update inverted index and posting
                if term not in self.inverted_idx.keys():
                    self.inverted_idx[term] = [1,document_dictionary[term]]
                    if (term.replace('.',"").replace(',',"").replace(" ","").replace("/","")).isnumeric():
                        self.postingDictNum[term]={}
                        self.postingDictNum[term][document.tweet_id] = document_dictionary[term]
                    else:
                        self.postingDict[term]={}
                        self.postingDict[term][document.tweet_id] = document_dictionary[term]



                else:
                    self.inverted_idx[term][0] += 1
                    self.inverted_idx[term][1] += document_dictionary[term]
                    if self.postingDict.get(term):
                        if (term.replace('.', "").replace(',', "").replace(" ", "").replace("/","")).isnumeric():
                            self.postingDictNum[term][document.tweet_id]=document_dictionary[term]
                        else:
                            self.postingDict[term][document.tweet_id]=document_dictionary[term]
                    else:
                        if (term.replace('.', "").replace(',', "").replace(" ", "").replace("/","")).isnumeric():
                            self.postingDictNum[term] = {}
                            self.postingDictNum[term][document.tweet_id] = document_dictionary[term]
                        else:
                            self.postingDict[term] = {}
                            self.postingDict[term][document.tweet_id] = document_dictionary[term]


                    #self.replace_line(filename,self.postingDict[term][0][0],document.tweet_id,str(document_dictionary[term]))


            except:
                print('problem with the following key {}'.format(term[0]))
        self.DocmentInfo[document.tweet_id]=[document.infoForDoc]+[document.doc_length]+[len(document_dictionary)]
        if (self.numofdocment == 1000):
            start_time = time.time()
            if(self.firstposting):
                self.fun1()
                self.postingGenrate("number.json",self.postingDictNum)
                self.firstposting=False
            else:
                self.fun2()
            print("--- %s seconds ---" % (time.time() - start_time))
            self.numofdocment = 0
            self.postingDict={}
            self.postingDictNum={}

