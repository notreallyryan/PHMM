"""
Handles all of the requests made by the user
"""
import sys
sys.path.insert(0,".")
from Storage import DataBase
from Algorithms import Bestmatch
from Training import Trainer
from Process import Reader

from os.path import dirname, abspath
from os import listdir
from os.path import isfile, join


class Requests:
    """
    Handles the main requests that can be inputted by a user.
    """

    def __init__(self) -> None:
        self.Database = DataBase.DataBase()
        self.modelnames = []
        self.queries = {}
        self.reader = Reader.Reader()



    def make_model(self, thresholds):
        """
        makes the model from the current .fasta files in FASTA using the thresholds given
        """
        self.Database.clear_data()

        d = dirname(dirname(abspath(__file__))) + "/_FASTA"
        onlyfiles = [f for f in listdir(d) if isfile(join(d, f))]
        if '.DS_Store' in onlyfiles: onlyfiles.remove('.DS_Store') #get rid of this idk why it's there

        for name in onlyfiles:
            address = d + "/" + name
            model = self.reader.read_Model_seqs(address) #read file
            self.modelnames.append(name[:-6]) #use file name minus .fasta as the model name
            Training = Trainer.Trainer(model, thresholds) #train model
            Training.make_model()
            self.Database.add_model(Training.return_model(), self.modelnames[-1]) #add model to database under file name



    def make_queries(self):
        """
        gets the queries from the current FASTA files stored in QUERIES
        """
        self.queries.clear()

        d = dirname(dirname(abspath(__file__))) + "/_QUERIES"
        onlyfiles = [f for f in listdir(d) if isfile(join(d, f))]
        if '.DS_Store' in onlyfiles: onlyfiles.remove('.DS_Store')

        for name in onlyfiles:
            address = d + "/" + name
            sequence = self.reader.read_Queried_seqs(address) #read file
            self.queries[name[:-6]] = sequence 



    def return_loaded_models(self):
        return self.modelnames
    


    def return_loaded_queries(self):
        return self.queries.keys()



    def return_most_likely(self, name):
        """
        returns the model that would be most likely to generate the sequence under the user given name

        Keyword arguments:
        name -- a string containing the name of a sequence stored in _Queries.
        """
        Algorithm = Bestmatch.Bestmatch(self.Database.get_all(), self.queries[name])
        scores = Algorithm.get_probs()

        return(max(scores, key=scores.get))