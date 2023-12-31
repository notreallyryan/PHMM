from .Connected3Node import Connected3Node
import pandas as pd
import numpy as np

class AAnode(Connected3Node):
    """
    Accounts for the emission probabilities in Insert and Match Nodes.

    Has a probability for each of the 20 amino acids, and the 2 extra uncertain characters B and Z.
    Stores lagrangian smoothed probabilities and characters in a pandas dataframe,
    """

    def __init__(self, type):
        """
        Initates the Node.

        Stores probabilities and characters in a pandas dataframe. Employs Lagrangian Smoothing
        """
        super().__init__(type)
        Amino_acids = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V', 'B', 'Z']
        self.State_count = 22 #for division later to create fractions
        self.emissions = pd.DataFrame(data = {'p': np.ones(22), 's': Amino_acids})



    def return_state(self):
        """
        returns dataframe of the emission states pairs stored in the node
        """
        return self.emissions
    


    def write_state(self, seen_states):
        """
        Updates the emission state matrix given a list of the seen states

        Keyword arguments:
        seen_states -- a list of the states oberved at this node. 
        Assumes that there are no states outside of the basic 20 amino acids and additional 2 special cases with standard Abbreviations in Caps.
        """
        
        #first update all values
        for AA in seen_states:
            self.emissions.loc[self.emissions.s == AA, 'p'] += 1
            self.State_count += 1
        
        #then make into natural logs of the fractions
        self.emissions['p'] = self.emissions['p'].div(self.State_count)