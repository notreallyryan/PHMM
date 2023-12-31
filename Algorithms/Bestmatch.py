"""
Finds the best match for a given sequence from the families stored in a given database object.
"""

class Bestmatch:
    """
    Main class for the Forwards Algorithm, finds the model that is most likely to produce a given sequence.
    """

    def __init__(self, database, sequence) -> None:
        """
        Initiator for the Bestmatch object

        keyword arguments:
        database -- the database object containing the families to compare to.
        sequence -- a string containing the amino acid sequence to be compared to the families
        """

        self.__database = database
        self.__sequence = sequence
        self.__scores = dict()

        for key in database.keys():
            self.__scores[key] = 0
    


    def get_probs(self):
        """
        Returns a dict with model names as the key and the model score as the value.
        """
        for key in self.__scores.keys():
            self.__scores[key] = self.__Forwards(self.__database[key])
        
        return self.__scores




    def __Forwards(self, model):
        """
        Finds the probability that the sequence matches a given family. Returns a float value.

        Key arguments:
        model = the model from the database to compare to.
        """

        #preparing initial values
        D =  [0] * (len(self.__sequence)+1)
        I =  [0] * (len(self.__sequence)+1)
        M =  [0] * (len(self.__sequence)+1)
        M[0] = 1 #Since Start is considered a "match" the chance of starting at a match is 100%

        ST = model[0].return_connections() #Start Transition Probabilities
        IT = model[1].return_connections() #Insertion Transition Probabilities
        IE = model[1].return_state() #Insertion Emission probabilities

        #update initial Insertion probabilities as they rely on probability of previous amino acid being at same insert node
        I[1] = IE.at[IE.index[IE.s == self.__sequence[0]][0], 'p'] * ST.at[1, 'p']

        for x in range(2, len(self.__sequence)+1):
            I[x] = IE.at[IE.index[IE['s'] == self.__sequence[x-1]][0], 'p'] * I[x-1] * IT.at[1, 'p']
        
        #set the "score" of the model
        temp = I[-1]
        return self.__Forward_Recursive(D,I,M,ST,IT,ST,temp)



    def __Forward_Recursive(self, D, I, M, D_prev, I_prev, M_prev, temp):
        """
        helper Loop function for Forward algorithm (not recursion to avoid stack variables). Seperated for testing purposes

        keyword arguments
        D, I, M -- the previous values found by the Forward Recursive algorithms. for 1<= i <= len(self.__sequence), 
                represents the probability that self._sequence[i-1] would be at the previous Del, insert, or Match node.

        D_prev, I_prev, M_prev --  pandas dataframes of the previous transition probabliites from the Del, Insert, and Match nodes

        temp --  current probability that the sequence fits the model
        """

        #initial set up
        old_D = D
        old_I = I
        old_M = M
        prev_D_t = D_prev
        prev_I_t = I_prev
        prev_M_t = M_prev
        value = temp

        #repeat until End Node is reached. 
        #(since prev_M was computed in last iteration, if E appears as a transition node it means we are about to compute it)
        while(prev_M_t.at[2, 't'].return_type() != 'E'):
            D_node = prev_M_t.at[0, 't'] #get current Deletion Node
            M_node = prev_M_t.at[2, 't'] #Get current matching Node

            D_node_t = D_node.return_connections() #Get Deletion Node transitions

            M_node_t = M_node.return_connections() #get Matching Node transitions
            M_node_e = M_node.return_state() #Get Matching Node Emissions

            #prepares new arrays
            new_D = [0]* len(old_D)
            new_M = [0]* len(old_M)
            new_I = [0]* len(old_I)
            
            #do the math.
            for x in range(1, len(new_D)):
                new_D[x] = ((old_D[x]*prev_D_t.at[0, 'p'] + old_M[x-1]*prev_M_t.at[0, 'p']
                             + old_I[x-1]*prev_I_t.at[0, 'p']))

                new_M[x] = (M_node_e.at[M_node_e.index[M_node_e.s == self.__sequence[x-1]][0], 'p'] *
                            (old_D[x]*prev_D_t.at[2, 'p'] + old_M[x-1]*prev_M_t.at[2, 'p']
                             + old_I[x-1]*prev_I_t.at[2, 'p']))
                
            #initiate Insertion Node and get transition and emission probabilities    
            I_node = D_node_t.at[1, 't']
            I_node_t = I_node.return_connections()
            I_node_e = I_node.return_state()

            #Since the Forward Algorithm Insert Values depend on the current Match and Deletion values, need to compute this afterwards
            for x in range(1, len(new_I)):
                new_I[x] = (I_node_e.at[I_node_e.index[I_node_e.s ==  self.__sequence[x-1]][0] , 'p'] *
                            (new_D[x]*D_node_t.at[1, 'p'] + new_M[x-1]*M_node_t.at[1, 'p']
                             + new_I[x-1]*I_node_t.at[1, 'p']))
                
            #update the score
            value = new_I[-1] + new_M[-1] + new_D[-1]
            
            #update the variables with the ones computed in the loop
            old_D = new_D
            old_I = new_I
            old_M = new_M
            prev_D_t = D_node_t
            prev_I_t = I_node_t
            prev_M_t = M_node_t

        return value





