from numpy import array
from numpy import diag
from numpy import dot
from scipy.linalg import svd

class Ranker:
    def __init__(self):
        pass

    @staticmethod
    def rank_relevant_doc(relevant_doc):
        """
        This function provides rank for each relevant document and sorts them by their scores.
        The current score considers solely the number of terms shared by the tweet (full_text) and query.
        :param relevant_doc: dictionary of documents that contains at least one term from the query.
        :return: sorted list of documents by score
        """

        A=array(relevant_doc)
        U,S,V= svd(A)
        X=(S >30).sum()
        print("ss:",X)
        Ut=U[0:,0:X]
        print("ut:_____\n",Ut,"\n")
        St = S[0:X]
        print("st:_____\n", St, "\n")
        Vt=(V[0:,0:X]).transpose()
        print("vt:_____\n", Vt, "\n")
        return Ut, St, Vt

        return sorted(relevant_doc.items(), key=lambda item: item[1], reverse=True)

    @staticmethod
    def retrieve_top_k(sorted_relevant_doc, k=1):
        """
        return a list of top K tweets based on their ranking from highest to lowest
        :param sorted_relevant_doc: list of all candidates docs.
        :param k: Number of top document to return
        :return: list of relevant document
        """
        return sorted_relevant_doc[:k]
