import os
import pandas as pd
import glob2

class ReadFile:
    def __init__(self, corpus_path):
        self.corpus_path = corpus_path

    def read_file(self):
        """
        This function is reading a parquet file contains several tweets
        The file location is given as a string as an input to this function.
        :param file_name: string - indicates the path to the file we wish to read.
        :return: a dataframe contains tweets.
        """
        allfiles = glob2.glob(self.corpus_path+"/*/*/*.parquet") +glob2.glob(self.corpus_path+"/*/*.parquet")+glob2.glob(self.corpus_path+"/*.parquet")
        #full_path = os.path.join(self.corpus_path)
        df=[]

        df = [(pd.read_parquet(allfiles[0], engine="pyarrow")).values.tolist()]
        return df
