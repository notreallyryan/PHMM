import sys
sys.path.insert(0,".")
from Model import *
import unittest
import pandas as pd
import numpy as np

class TestModel(unittest.TestCase):

    def test_End_Node(self):
        TN = End.End()
        self.assertEqual(TN.return_type(), 'E')
    
    def test_Start_Node_return(self):
        TN = Start.Start()
        self.assertEqual(TN.return_type(), 'S') #test type return
    
    def test_Connections_Destination(self):
        TN = Start.Start()
        C1 = End.End()
        C2 = End.End()
        C3 = End.End()

        TN.set_Del(C1)
        TN.set_Insert(C2)
        TN.set_Match(C3)

        transitions = pd.DataFrame(data = {'p': np.ones(3), 't': [C1, C2, C3]})
        self.assertTrue(TN.return_connections().equals(transitions))

    def test_Connections_probabilities(self):
        TN = Start.Start()
        C1 = End.End()
        C2 = End.End()
        C3 = End.End()

        TN.set_Del(C1)
        TN.set_Insert(C2)
        TN.set_Match(C3)

        transitions = pd.DataFrame(data = {'p': np.log([2/8, 3/8, 3/8]), 't': [C1, C2, C3]})
        TN.write_connections([1, -1, 0, 0, 1])
        self.assertTrue(TN.return_connections().equals(transitions))

    def test_Del_Emissions(self):
        TN = Del.Del()
        emissions = pd.DataFrame(data = {'s':['-'], 'p': 1})
        self.assertTrue(TN.return_state().equals(emissions))
        self.assertEqual(TN.return_type(), 'D')

    def test_Amino_Acids(self):
        TN = Match.Match()
        additions = ['A', 'B', 'C', 'D', 'E', 'F']
        results = [2,1,1,2,2,1,2,1,1,1,1,1,1,2,1,1,1,1,1,1,2,1]
        results = pd.DataFrame(data = {'p': results})
        results = np.log(results['p'].div(28))
        TN.write_state(additions)
        self.assertTrue(TN.return_state()['p'].equals(results))

if __name__ == '__main__':
    unittest.main()