

class Indexer:

    def __init__(self, config):
        self.inverted_idx = {}
        self.postingDict = {}
        self.config = config
        self.postCount = 0
        self.maxTermInPost = 20
        self.currnetRowInPost = 0

        open("posting" + str(self.postCount) + ".txt", "w+")

    def replace_line(self,file_name, line_num, tweet_id ,f):
        lines = open(file_name, 'r').readlines()
        text=lines[line_num]
        textlist=text.split(',')
        text=textlist[0]
        bol=True
        for i in range(1,len(textlist)):
            if(int(textlist[i].split(" ")[0])>int(tweet_id)):
                text+=","+ tweet_id +" " +f
                bol=False
            text+=","+textlist[i].replace("\n","")
        if bol:
            text += "," + tweet_id + " " + f
        text+="\n"
        lines[line_num]=text
        out = open(file_name, 'w')
        out.writelines(lines)
        out.close()


    def add_new_doc(self, document):
        """
        This function perform indexing process for a document object.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param document: a document need to be indexed.
        :return: -
        """

        document_dictionary = document.term_doc_dictionary
        # Go over each term in the doc
        for term in document_dictionary.keys():
            try:
                # Update inverted index and posting
                if term not in self.inverted_idx.keys():
                    self.inverted_idx[term] = [1,document_dictionary[term]]
                    self.postingDict[term] = []

                    if self.currnetRowInPost >= self.maxTermInPost:
                        self.postCount += 1
                        self.currnetRowInPost = 0
                        open("posting" + str(self.postCount) + ".txt", "w+")
                    filename = "posting" + str(self.postCount) + ".txt"
                    self.postingDict[term].append((self.currnetRowInPost, filename))
                    # document.tweet_id, document_dictionary[term]
                    with open(filename, 'a') as f:
                        f.write(term + "," + document.tweet_id + " " + str(document_dictionary[term]) +"\n")
                    self.currnetRowInPost+=1

                else:
                    self.inverted_idx[term][0] += 1
                    self.inverted_idx[term][1] += document_dictionary[term]
                    filename = self.postingDict[term][0][1]
                    self.replace_line(filename,self.postingDict[term][0][0],document.tweet_id,str(document_dictionary[term]))


            except:
                print('problem with the following key {}'.format(term[0]))
