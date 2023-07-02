from .Connected3Node import Connected3Node
import pandas as pd

class Del(Connected3Node):

    def __init__(self):
        super().__init__('D')
        self.emissions = pd.DataFrame(data = {'s':['-'], 'p': 1})



    def return_state(self):
        """
        returns dataframe of the emission states pairs stored in the node
        """
        return self.emissions