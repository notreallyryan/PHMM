"""
Takes care of training the transition aspects of the profile HMM model

It is not in charge of determining if a given index is a key feature or not.
"""
import sys
sys.path.insert(0,".")
from Model import *

class Transitions:

    def __init__(self, model) -> None:
        """
        Updates which nodes to change

        Keyword arguments:
        model -- a list containing the nodes to update the transition probability for in DIM order
        """
        self.model = model

    def update_model(self, model):
        self.model = model



    def transition(self, fro, between, to):
        """
        The function that will be called by the other classes

        Keyword arguments:
        fro --  a numerical list detailing the states of the current key feature
        between - a numerical list detailing the states between the two key features
        to -- a numerical list detailing the states of the next key feature
        """
        self.make_transitions(self.tally_transitions(fro, between, to))



    def tally_transitions(self, fro, between, to):
        """
        Observes and counts the transitions from different States.

        Returns the a list of the three transitions lists in the order D, I, M (Delete, Insert, Match)
        """
        D, I, M = [], [], []

        for i in range(0, len(fro)):
            #8 cases to account for: MM, MD, MID, MIM, DM, DD, DIM, DID
            #If transitioning to a match, apppend 0. If to an Insert, append 1. If to a Delete, append -1.

            #If starting at a Match
            if fro[i] == 0:
                if between[i] > 0:
                    M.append(1) #MI
                    for j in range(0, between[i]-1): I.append(1) #II
                    I.append(to[i]) #ID and IM and I to END
                else: M.append(to[i]) #MD and MM, also M to END

            #If starting at an insert
            elif fro[i] == -1:
                if between[i] > 0:
                    D.append(1) #DI
                    for j in range(0, between[i]-1): I.append(1) #II
                    I.append(to[i]) #ID and IM and I to END
                else:D.append(to[i]) #DD and DM also D to END

        return [D, I, M]
    


    def make_transitions(self, transitions):
        """
        Sends the transition tallies to the appropriate nodes. Assumes the lists are in the order D, I, M

        Keyword arguments:
        transitions --  a 2D array of the observed transitions, obtained from the tally_transitions function
        """
        currlen = len(self.model)
        if currlen == 2: #Only time there are two nodes to update is if there is only the start and insert node. 
            self.make_starting_transitions(transitions)
            return

        D, I, M = transitions[0], transitions[1], transitions[2]

        self.model[1].write_connections(I)
        self.model[2].write_connections(M)
        self.model[0].write_connections(D)



    def make_starting_transitions(self, transitions):
        """
        Function that takes care of special case of start.
        """
        I, M = transitions[1], transitions[2]

        self.model[0].write_connections(M)
        self.model[1].write_connections(I)
    


