class DataBase:
    """
    Stores all the models that are currently in use.

    Accepts requests to add, delete, or access the models.
    """
    def __init__(self):
        self.__database = dict()



    def add_model(self, model, model_name):
        """
        Adds the model to the database under a given model name. Assumes name has not yet been used.

        Keyword arguments:
        model -- an ordered list containing all the nodes in the model
        model_name - a string key to store the model under.
        """
        self.__database[model_name] = model



    def delete_model(self, model_name):
        """
        Deletes the model stored under a given model name. Assumes the name is valid.

        Keyword arguments:
        model_name: a string containing the name of a model to delete.
        """
        del self.__database[model_name]



    def get_model(self, model_name):
        """
        Returns access to the model stored under a given name. Assumes there is a model stored under the given name
        """
        return self.__database[model_name]
    


    def get_all(self):
        """
        Returns all of the models stored in the DataBase
        """
        return self.__database



    def check_name(self, model_name):
        """
        Checks if the name is currently being used. Should be run before using any other function. 
        """
        if model_name in self.__database: return True
        else: return False

    

    def clear_data(self):
        """
        Deletes all stored data.
        """
        self.__database.clear()