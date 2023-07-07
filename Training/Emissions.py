import sys
sys.path.insert(0,".")
from Model import *

class Emissions:
    """
    Takes care of the emission aspect of the profile HMM model.

    It is not in charge of determining if a given index is a key feature or not.
    """

    
    def __init__(self, model) -> None:
        """
        Initiates the object

        Keyword arguments:
        model -- the list of nodes to updated
        """
        self.model = model
    
    def update_model(self,model):
        self.model = model
    

    def emission(self, emissions):
        """
        The function that will be called by other classes

        Keyword arguments:
        emissions --  a 2D array containing the emissions at each index between two states.
            Including the emissions at the starting key feature index, but not the ending key feature index.
        """
        if emissions: self.make_emissions(self.tally_emissions(emissions))
        


    def tally_emissions(self, emissions):
        """
        Observes and counts the emissions of different states.
        
        returns: a list of the two transition lists in the order "I, M" (Insert, Match)
        """

        M, I = [], []
        #get emissions for key node - the first list in the emissions list are the emission observed at the key feature
        for c in emissions[0]:
            if c != '-': M.append(c)
        
        #get possible emissions between key node and next key node. -- this is from all other lists in the provided list.
        if len(emissions) > 1:
            for index in range(1, len(emissions)):
                for c in emissions[index]:
                    if c != '-': I.append(c) 
        return [I, M]

    

    def make_emissions(self, emissions):
        """
        Sends the emission tallies to the appropriate nodes. Assumes the lists are in the order I, M

        Keyword arguments:
        emissions --  a 2D array of the observed emissions, obtained from the tally_emissions function
        """
        
        if emissions[1][0] == 0: #if the Key feature observations are all '0' indicates a Start Node, not a key feature
            self.make_starting_emissions(emissions)
            return

        I,M = emissions[0], emissions[1]
        self.model[0].write_state(I)
        self.model[1].write_state(M)
    


    def make_starting_emissions(self, emissions):
        """
        Function that takes care of special case of start.
        """
        I = emissions[0]
        self.model[1].write_state(I)
