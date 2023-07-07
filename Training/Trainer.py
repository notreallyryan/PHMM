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
        tallies up number of matches and deletions in a key index

        returns an ordered list where 0 indicates a match, and -1 a deletion 
        """
        transitions = [0] * self.length
        for i in range(0, self.length):
            if column[i] == '-': transitions[i] = -1 
        return transitions
    


    def get_transitions_insert(self, column):
        """
        Counts the number of insertions in a non key index

        returns an ordred list where 1 indicates an insertion, and 0 otherwise.
        """
        transitions = [0] * self.length
        for i in range(0, self.length):
            if column[i] != '-': transitions[i] +=1
        return transitions
        


    def make_model(self):
        """
        The main model maker. Creates the model nodes and stores it in self.model.
        """

        #Starting phase
        index = 0 #keeps track of place in sequence
        start = Start.Start() #creates first two nodes
        insert = Insert.Insert()
        start.set_Insert(insert) #connects Start to Insert
        to_connect = [start, insert] #queue used for connecting later 

        #append the nodes to the model list.
        self.model.append(start)
        self.model.append(insert)

        #load the nodes to process into the transition and emission objects
        self.Trans.update_model([start, insert])
        self.Emit.update_model([start, insert])

        I_t = [0] * self.length #sets up the Transitions array counting number of inserts between start and the first key feature
        I_e = [[0] * self.length] #sets up the Emissions array where all emissions are stored. The zeros take care of the no emissons at the start node
        K_t1 = [0] * self.length #sets up the first "key feature" 
                                #in this case start is considered the first key feature, and every value at the position is considred a match
        
        #Loop that continues until a key point or the sequence end.
        while self.determine_key(self.data[index]) is False and index !=len(self.data):
            I_e.append(self.data[index]) #adds emissions to list
            I_t = [I_t[i]+ self.get_transitions_insert(self.data[index])[i] for i in range(len(I_t))] #adds to number of insertions each sequence in the family has before reaching the key feature
            index += 1
        
        #If didn't reach the end of the sequence, then set the key feature observation
        if index != len(self.data):
            K_t2 = self.get_transitions_key(self.data[index]) #record whether there is a match or deletion in each sequence at the key feature
            self.set_Next_Nodes(to_connect) #creates next nodes and connects the previous ones to them
        else: 
            K_t2 = [0] * self.length #At end, record that all sequences go to a match state (END)
            self.set_End(to_connect) #terminate

        #pass data to the transition and emission objects to process and finalize.
        self.Trans.transition(K_t1, I_t, K_t2)
        self.Emit.emission(I_e)

        #set previous key feature observations to current.
        K_t1 = K_t2

        #normal phase - will ignore if index is already out of sequence range. 
        while index != len(self.data):
            I_e = [self.data[index]]
            I_t = [0] * self.length
            index += 1 #because K_t1 was already set to K_t2

            #update which nodes are to be changed - previously put into model by set_next_Nodes function
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
        """
        Creates new nodes, and connects user given nodes to the new nodes. puts the new nodes back into the list for next iteration

        keyword arguments:
        to_connect --  a queue containing all the previous nodes to connect to the next nodes.
        """
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
        """
        Ends the model by capping it with an End Node. Connects to user given nodes.

        keyword arguments
        to_connect -- a queue containg the nodes to connect to the end node. 
        """
        E= End.End()
        self.model.append(E)
        while to_connect:
                node = to_connect.pop()
                node.set_Match(E)

        



    
