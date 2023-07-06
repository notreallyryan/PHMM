"""
Reads the FastA sequences stored in FASTA folder.
"""
from pathlib import Path
import re

class Reader:

    def __init__(self) -> None:
        pass

    def read_Model_seqs(self, file_location):
        return self.__processdata(self.__readfile(file_location))
    
    
    def read_Queried_seqs(self, file_location):
        return self.__readfile(file_location)[0]


    def __readfile(self, file_location):
        f = open(file_location, 'r')
        lines = f.readlines()
        hre = re.compile('>(\S+)')
        lre = re.compile('^(\S+)$')
         
        sequences = []
        id = -1

        for line in lines:
            outh = hre.search(line)
            if outh: 
                id += 1
            else:
                outl = lre.search(line)
                if outl == None: continue #deletes any nasty blanks >:(
                elif len(sequences) != id: sequences[id] += outl.group(1)
                else: sequences.append(outl.group(1))
        
        return sequences



    def __processdata(self, sequences):
        processed = []
        for index in range(len(sequences[1])):
            temp = []
            for seq in sequences:
                temp.append(seq[index])
            processed.append(temp)
        return processed



def main():
    test = Reader()
    print(test.read_Model_seqs("/Users/ryan/PHMM/FASTA/test.fasta"))
    print(test.read_Queried_seqs("/Users/ryan/PHMM/FASTA/test.fasta"))

if __name__ == "__main__":
    main()