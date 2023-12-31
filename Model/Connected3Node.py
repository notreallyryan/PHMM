from .Node import Node
import numpy as np
import pandas as pd

class Connected3Node(Node):
    """
    Accounts for the Transition probabilities of all nodes. 
    
    Every node will connect to three other nodes: an Insert, a Delete, and a Match

    Only exception is the Last set of Nodes, which will only connect to an Insert and the End Node.
    """

    def __init__(self, type):
        """
        Initiates the Object. Stores the probabilities and locations in a pandas dataframe (for practice)
        """
        super().__init__(type)
        self.transitions = pd.DataFrame(data = {'p': np.ones(3), 't': [None]*3})
        self.transitions_count = 3 #for division later to get fractions


    """
    Sets up the destination nodes
    """
    def set_Match(self, match):
        self.transitions.at[2, 't'] = match
    
    def set_Insert(self, insert):
        self.transitions.at[1, 't'] = insert

    def set_Del(self, delete):
        self.transitions.at[0, 't'] = delete


    def return_connections(self):
        """
        returns dataframe of the transition states pairs stored in the node
        """
        return self.transitions
    


    def write_connections(self, connections):
        """
        Updates the transition matrix given a list of the transitions from the hidden state

        Keyword arguments:
        connections -- an integer list of all transitions observed from the hidden state:
        where "-1" implies a transition to a deletion state, "0" a transition to a matching state, 
        and "1" implies a transition to an insertion state
        """
        for c in connections:
    
            if c < 0: #deletion
                self.transitions.at[0,'p'] += 1
            elif c > 0: #insertion
                self.transitions.at[1,'p'] += 1
            elif c == 0: #match
                self.transitions.at[2,'p'] += 1

            self.transitions_count +=1


        """
        If no End Node has been set, assume that current object is in last set of Nodes.
        """
        if self.transitions.at[0,'t'] == None: 
            self.transitions.at[0,'p'] = 0
            self.transitions_count -= 1

        self.transitions['p'] = self.transitions['p'].div(self.transitions_count)
    