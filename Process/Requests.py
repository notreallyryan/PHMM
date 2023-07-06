"""
Handles all of the requests made by the user
"""
import sys
sys.path.insert(0,".")
from Storage import DataBase
from Algorithms import Bestmatch
from Training import Trainer

from os.path import dirname, abspath
from os import listdir
from os.path import isfile, join
import Reader

class Requests:

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

        d = dirname(dirname(abspath(__file__))) + "/FASTA"
        onlyfiles = [f for f in listdir(d) if isfile(join(d, f))]
        onlyfiles.remove('.DS_Store') #get rid of this idk why it's there

        for name in onlyfiles:
            address = d + "/" + name
            model = self.reader.read_Model_seqs(address)
            self.modelnames.append(name[:-6])
            Training = Trainer.Trainer(model, thresholds)
            Training.make_model()
            self.Database.add_model(Training.return_model(), self.modelnames[-1])



    def make_queries(self):
        """
        gets the queries from the current FASTA files stored in QUERIES
        """
        self.queries.clear()

        d = dirname(dirname(abspath(__file__))) + "/QUERIES"
        onlyfiles = [f for f in listdir(d) if isfile(join(d, f))]

        for name in onlyfiles:
            address = d + "/" + name
            sequence = self.reader.read_Queried_seqs(address)
            self.queries[name[:-6]] = sequence



    def return_most_likely(self, name):
        """
        for name 
        """
        Algorithm = Bestmatch.Bestmatch(self.Database.get_all(), self.queries[name])
        scores = Algorithm.get_probs()

        return(max(scores, key=scores.get))


def main():
    R = Requests()
    R.make_model(0.5)
    R.make_queries()
    print(R.return_most_likely("unknown1"))

if __name__ == "__main__":
    main()