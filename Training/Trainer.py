"""
Main Trainer function for the profile HMM model.

Does all of the organization, and passes on the requests to various objects.
"""
import sys
sys.path.insert(0,".")
from Model import *
from Training import Transitions
from Training import Emissions


class Trainer:
    
    def __init__(self, data, threshold):
        """
        Initiates the object.

        Keyword arguments:
        data -- a 2D array containing the training data, where each column contains the ordered obervations at that index across all FASTA sequences
        threshold -- a fraction that determines if an index is a key feature or not. The fraction of observed amino acid states over total observations
            must exceed this threshold to be considered a key feature 
        """
        self.data = data
        self.threshold = threshold
        self.length = len(data[0])
        self.model = []
        self.Trans = Transitions.Transitions(self.model)
        self.Emit = Emissions.Emissions(self.model)

    def return_model(self):
        return self.model

    def determine_key(self, column):
        """
        Returns true if an index is a key, and false otherwise.

        Keyword arguments:
        column -- the observed states at the index.
        """
        blanks = 0
        for i in column:
            if i == '-': blanks += 1

        if (len(column) - blanks)/len(column) < self.threshold: return False
        else: return True

    def get_transitions_key(self, column):
        """
        
        """
        transitions = [0] * self.length
        for i in range(0, self.length):
            if column[i] == '-': transitions[i] = -1
        return transitions
    
    def get_transitions_insert(self, column):
        transitions = [0] * self.length
        for i in range(0, self.length):
            if column[i] != '-': transitions[i] +=1
        return transitions
        

    def make_model(self):

        #Starting phase
        index = 0
        start = Start.Start()
        insert = Insert.Insert()
        start.set_Insert(insert) #connects Start to Insert
        to_connect = [start, insert] #queue used for connecting later
        self.model.append(start)
        self.model.append(insert)
        self.Trans.update_model([start, insert])
        self.Emit.update_model([start, insert])

        I_t = [0] * self.length
        I_e = [[0]* self.length]
        K_t1 = [0] * self.length
        
        while self.determine_key(self.data[index]) is False and index !=len(self.data):
            I_e.append(self.data[index])
            I_t = [I_t[i]+ self.get_transitions_insert(self.data[index])[i] for i in range(len(I_t))]
            index += 1
        
        if index != len(self.data):
            K_t2 = self.get_transitions_key(self.data[index])
            self.set_Next_Nodes(to_connect)
        else: 
            K_t2 = [0] * self.length
            self.set_End(to_connect)

        self.Trans.transition(K_t1, I_t, K_t2)
        self.Emit.emission(I_e)
        K_t1 = K_t2

        #normal phase
        while index != len(self.data):
            I_e = [self.data[index]]
            I_t = [0] * self.length
            index += 1 #because K_t1 was already set to K_t2

            #update which nodes are to be changed
            D = self.model[-3]
            I = self.model[-2]
            M = self.model[-1]
            self.Trans.update_model([D, I, M])
            self.Emit.update_model([I, M])

            #get data arrays
            while index !=len(self.data) and self.determine_key(self.data[index]) is False:
                I_e.append(self.data[index])
                I_t = [I_t[i]+ self.get_transitions_insert(self.data[index])[i] for i in range(len(I_t))]
                index += 1

            #make transition changes
            if index != len(self.data):
                K_t2 = self.get_transitions_key(self.data[index])
                self.set_Next_Nodes(to_connect)
            else: 
                K_t2 = [0] * self.length
                self.set_End(to_connect)

            #send data arrays to transmission and emission editors
            self.Trans.transition(K_t1, I_t, K_t2)
            self.Emit.emission(I_e)

            #update K_t1
            K_t1 = K_t2

    

    def set_Next_Nodes(self, to_connect):
        M = Match.Match()
        I = Insert.Insert()
        D = Del.Del()
        
        I.set_Insert(I)
        M.set_Insert(I)
        D.set_Insert(I)

        while to_connect:
            node = to_connect.pop()
            node.set_Match(M)
            node.set_Del(D)

        to_connect.append(M)
        to_connect.append(I)
        to_connect.append(D)
        self.model.append(D)
        self.model.append(I)
        self.model.append(M)
    


    def set_End(self, to_connect):
        E= End.End()
        self.model.append(E)
        while to_connect:
                node = to_connect.pop()
                node.set_Match(E)

        



    
