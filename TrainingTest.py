import sys
sys.path.append("Training")
from Training import *
sys.path.append("Model")
from Model import *
import unittest
import pandas as pd
import numpy as np

class TestModel(unittest.TestCase):

    
    def test_Transitions(self):
        S = Start.Start()
        I0 = Insert.Insert()
        D1 = Del.Del()
        I1 = Insert.Insert()
        M1 = Match.Match()
        D2 = Del.Del()
        I2 = Insert.Insert()
        M2 = Match.Match()
        E = End.End()

        S.set_Insert(I0)
        S.set_Del(D1)
        S.set_Match(M1)

        I0.set_Insert(I0)
        I0.set_Match(M1)
        I0.set_Del(D1)

        for x in [D1, M1]:
            x.set_Insert(I1)
            x.set_Match(M2)
            x.set_Del(D2)

        I1.set_Insert(I1)
        I1.set_Match(M2)
        I1.set_Del(D2)

        for x in [D2, M2, I2]:
            x.set_Insert(I2)
            x.set_Match(E)

        testModel = [S, I0]
        TestTran = Transitions.Transitions(testModel)
        a = [0,0,0,0,0]
        b = [1,0,1,0,2]
        c = [0,0,-1,-1,0]
        TestTran.transition(a,b,c)
        S_t = pd.DataFrame(data = {'p': np.log([2/8, 4/8, 2/8]), 't': [D1, I0, M1]})
        I0_t = pd.DataFrame(data = {'p': np.log([2/7, 2/7, 3/7]), 't': [D1, I0, M1]})
        self.assertTrue(S.return_connections().equals(S_t))
        self.assertTrue(I0.return_connections().equals(I0_t))

        testModel = [D1, I1, M1]

        TestTran.update_model(testModel)
        a = [0,0,0,0,0,-1,-1,-1,-1,-1]
        b = [0,0,1,1,2,0,0,1,1,2]
        c = [0, -1, 0, -1, 0, -1, 0, -1, 0, -1]
        TestTran.transition(a,b,c)
        DM_t = pd.DataFrame(data = {'p': np.log([2/8, 4/8, 2/8]), 't': [D2, I1, M2]})
        I_t = pd.DataFrame(data = {'p': np.log([4/11, 3/11, 4/11]), 't': [D2, I1, M2]})
        self.assertTrue(D1.return_connections().equals(DM_t))
        self.assertTrue(I1.return_connections().equals(I_t))
        self.assertTrue(M1.return_connections().equals(DM_t))

        testModel = [D2, I2, M2]
        TestTran.update_model(testModel)
        a = [0, 0, -1, -1, -1]
        b = [0, 1, 0, 1, 2]
        c = [0,0,0,0,0]
        TestTran.transition(a,b,c)
        D2_t = pd.DataFrame(data = {'p': np.log([0/5, 3/5, 2/5]), 't': [None, I2, E]})
        I2_t = pd.DataFrame(data = {'p': np.log([0/6, 2/6, 4/6]), 't': [None, I2, E]})
        M2_t = pd.DataFrame(data = {'p': np.log([0/4, 2/4, 2/4]), 't': [None, I2, E]})
        self.assertTrue(D2.return_connections().equals(D2_t))
        self.assertTrue(I2.return_connections().equals(I2_t))
        self.assertTrue(M2.return_connections().equals(M2_t))
    
    def test_Emissions(self):
        S = Start.Start()
        I0 = Insert.Insert()
        D1 = Del.Del()
        I1 = Insert.Insert()
        M1 = Match.Match()
        E = End.End()

        S.set_Insert(I0)
        S.set_Del(D1)
        S.set_Match(M1)

        I0.set_Insert(I0)
        I0.set_Match(M1)
        I0.set_Del(D1)

        for x in [D1, M1, I1]:
            x.set_Insert(I1)
            x.set_Match(E)
      
        testModel = [S, I0]
        TestEmit = Emissions.Emissions(testModel)
        a = [[0, 0, 0],
             ['A','B','C'],
             ['-', 'B', '-'],
             ['-', 'B', 'C']]
        TestEmit.emission(a)
        I0_e = pd.DataFrame(data = {'p': np.log([2/28, 1/28, 1/28, 1/28, 3/28, 1/28, 1/28, 1/28, 1/28, 1/28, 1/28, 1/28, 1/28, 1/28, 1/28, 1/28, 1/28, 1/28, 1/28, 1/28, 4/28, 1/28]), 
                                    's': ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V', 'B', 'Z']})
        self.assertTrue(I0.return_state().equals(I0_e))

        testModel = [I1, M1]
        TestEmit.update_model(testModel)
        a = [['A','B','C'],
             ['-', 'B', '-'],
             ['-', 'B', 'C']]
        
        TestEmit.emission(a)
        M1_e = pd.DataFrame(data = {'p': np.log([2/25, 1/25, 1/25, 1/25, 2/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25, 2/25, 1/25]), 
                                    's': ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V', 'B', 'Z']})
        I1_e = pd.DataFrame(data = {'p': np.log([1/25, 1/25, 1/25, 1/25, 2/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25, 3/25, 1/25]), 
                                    's': ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V', 'B', 'Z']})

        self.assertTrue(I1.return_state().equals(I1_e))
        self.assertTrue(M1.return_state().equals(M1_e))

    
    def test_Trainer(self):
        testData = [['-', '-', 'A', '-'],
                    ['B', 'B', 'B', 'B'],
                    ['C', 'C', 'C', '-'],
                    ['-', '-', '-', 'A'],
                    ['-', '-', 'B', '-'],
                    ['-', 'C', 'C', '-'],
                    ['A', 'A', '-', 'A'],
                    ['B', 'B', '-', '-'],
                    ['-', '-', 'C', '-']]

        TrainTest = Trainer.Trainer(testData, 0.5)
        TrainTest.make_model()
        testobject = TrainTest.model

        S = pd.DataFrame(data = {'p': np.log([1/7, 2/7, 4/7])})
        I0 = pd.DataFrame(data = {'p': np.log([1/4, 1/4, 2/4])}) 
        D1 = pd.DataFrame(data = {'p': np.log([1/3, 1/3, 1/3])})
        I1 = pd.DataFrame(data = {'p': np.log([1/3, 1/3, 1/3])})
        M1 = pd.DataFrame(data = {'p': np.log([2/7, 1/7, 4/7])})
        D2 = pd.DataFrame(data = {'p': np.log([1/4, 2/4, 1/4])})
        I2 = pd.DataFrame(data = {'p': np.log([2/5, 1/5, 2/5])})
        M2 = pd.DataFrame(data = {'p': np.log([1/3, 1/3, 1/3])})
        D3 = pd.DataFrame(data = {'p': np.log([1/5, 1/5, 3/5])})
        I3 = pd.DataFrame(data = {'p': np.log([1/3, 1/3, 1/3])})
        M3 = pd.DataFrame(data = {'p': np.log([2/5, 1/5, 2/5])})
        D4 = pd.DataFrame(data = {'p': np.log([2/4, 1/4, 1/4])})
        I4 = pd.DataFrame(data = {'p': np.log([1/3, 1/3, 1/3])})
        M4 = pd.DataFrame(data = {'p': np.log([2/6, 1/6, 3/6])})
        D5 = pd.DataFrame(data = {'p': np.log([0, 2/4, 2/4])})
        I5 = pd.DataFrame(data = {'p': np.log([0, 1/3, 2/3])})
        M5 = pd.DataFrame(data = {'p': np.log([0, 1/4, 3/4])}) 

        correct_transitions = [S, I0, D1, I1, M1, D2, I2, M2, D3, I3, M3, D4, I4, M4, D5, I5, M5]

        for i in range(len(correct_transitions)):
            self.assertTrue(testobject[i].return_connections()['p'].equals(correct_transitions[i]['p']))

        I0 = pd.DataFrame(data = {'p': np.log([2/23, 1/23, 1/23, 1/23, 1/23, 1/23, 1/23, 1/23, 1/23, 1/23, 1/23,
                                               1/23, 1/23, 1/23, 1/23, 1/23, 1/23, 1/23, 1/23, 1/23, 1/23, 1/23 ])})
        I1 = pd.DataFrame(data = {'p': np.log([1/22] * 22)})
        M1 = pd.DataFrame(data = {'p': np.log([1/26, 1/26, 1/26, 1/26, 1/26, 1/26, 1/26, 1/26, 1/26, 1/26, 1/26,
                                               1/26, 1/26, 1/26, 1/26, 1/26, 1/26, 1/26, 1/26, 1/26, 5/26, 1/26])})
        I2 = pd.DataFrame(data = {'p': np.log([2/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24,
                                               1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 2/24, 1/24])})
        M2 = pd.DataFrame(data = {'p': np.log([1/25, 1/25, 1/25, 1/25, 4/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25,
                                               1/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25])})
        I3 = pd.DataFrame(data = {'p': np.log([1/22] * 22)})
        M3 = pd.DataFrame(data = {'p': np.log([1/24, 1/24, 1/24, 1/24, 3/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24,
                                               1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24])})
        I4 = pd.DataFrame(data = {'p': np.log([1/22] * 22)})
        M4 = pd.DataFrame(data = {'p': np.log([4/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25,
                                               1/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25, 1/25])})
        I5 = pd.DataFrame(data = {'p': np.log([1/23, 1/23, 1/23, 1/23, 2/23, 1/23, 1/23, 1/23, 1/23, 1/23, 1/23,
                                               1/23, 1/23, 1/23, 1/23, 1/23, 1/23, 1/23, 1/23, 1/23, 1/23, 1/23 ])})
        M5 = pd.DataFrame(data = {'p': np.log([1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24,
                                               1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 3/24, 1/24])})
        
        correct_emissions = [I0, I1, M1, I2, M2, I3, M3, I4, M4, I5, M5]
        positions = [1, 3, 4, 6, 7, 9, 10, 12, 13]
        for i in range(len(positions)):
            self.assertTrue(testobject[positions[i]].return_state()['p'].equals(correct_emissions[i]['p']))


if __name__ == '__main__':
    unittest.main()

