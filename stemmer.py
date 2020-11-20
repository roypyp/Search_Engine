from nltk import PorterStemmer
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
        Porter = PorterStemmer()
        tempstmeeing=[Porter.stem(tokens) for tokens in token]
        return tempstmeeing
        #return self.stemmer.stem(token)
