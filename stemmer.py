from nltk import LancasterStemmer
from nltk.stem import snowball


class Stemmer:
    def __init__(self):
        self.stemmer = snowball.SnowballStemmer("english")

    def stem_term(self, token):
        """
        This function stem a token
        :param token: string of a token
        :return: stemmed token
        """
        tempstmeeing = []
        lancaster = LancasterStemmer()
        for w in token:
            if (lancaster.stem(w) not in tempstmeeing):
                tempstmeeing += [lancaster.stem(w)]
        return tempstmeeing
        #return self.stemmer.stem(token)
