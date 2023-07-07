class Node:
    """
    Base Node Object. Only sets up the type variable. 
    """

    def __init__(self, type) -> None:
        """
        Initiator.
        Keyword argument:
        type -- a char (SMIDE) that represents the type of Node created (Start, Match, Insert, Del, or End)
        """
        self.type = type

    def return_type(self):
        return self.type