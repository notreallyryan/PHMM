"""
Reads the FastA sequences stored in FASTA folder.
"""
from pathlib import Path
import sys, re

class Reader:

    def __init__(self) -> None:
        pass



    def read_File(self, filename):
        root = Path(__file__).parents[1]
        pathstr = "FASTA/" + filename
        self.__my_path = root / pathstr
        self.__readfile()
        return self.__processdata()



    def __readfile(self):
        f = open(self.__my_path, 'r')
        lines = f.readlines()
        hre = re.compile('>(\S+)')
        lre = re.compile('^(\S+)$')
         
        self.__sequences = []
        id = -1

        for line in lines:
            outh = hre.search(line)
            if outh: 
                id += 1
            else:
                outl = lre.search(line)
                if outl == None: continue #deletes any nasty blanks >:(
                elif len(self.__sequences) != id: self.__sequences[id] += outl.group(1)
                else: self.__sequences.append(outl.group(1))



    def __processdata(self):
        processed = []
        for index in range(len(self.__sequences[1])):
            temp = []
            for seq in self.__sequences:
                temp.append(seq[index])
            processed.append(temp)
        return processed



def main():
    test = Reader()
    print(test.read_File("test.fasta"))

if __name__ == "__main__":
    main()