import sys
sys.path.insert(0,".")
from Algorithms import *
from Training import *
import unittest
import pandas as pd
import numpy as np

class TestFW(unittest.TestCase):
    testData = [['-', '-', 'A', '-'],
                ['B', 'B', 'B', 'B'],
                ['C', 'C', 'C', 'C'],
                ['-', '-', '-', 'A'],
                ['-', '-', 'B', '-'],
                ['-', 'C', 'C', '-'],
                ['A', 'A', 'A', 'A'],
                ['B', 'B', '-', '-'],
                ['-', '-', 'C', '-']]
    
    testData = [['B']*22,['C']*22,['A']*22]

    TrainTest = Trainer.Trainer(testData, 0.5)
    TrainTest.make_model()

    test_model = {}
    test_model["key"] = TrainTest.model
    
    
    def test_shorter_q(self):
        FW = Bestmatch.Bestmatch(self.__class__.test_model, "BCA")
        print(FW.get_probs())


if __name__ == '__main__':
    unittest.main()