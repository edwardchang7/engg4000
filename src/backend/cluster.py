from pymongo import MongoClient
from src.backend.models.rhythmic_pattern_model import RhythmicPatternModel


class Cluster:
    database = None
    collection = None
    database_name = None
    collection_name = None
    is_admin = None

    def __new__(self, new_database_name: str, new_collection_name: str, new_is_admin: bool):
        """
        This method is automatically called when a Cluster object is created. It flexibly selects and returns the
        singleton MongoDB instance depending on the database and collection names provided.

        :param new_database_name: The name of the database to work with.
        :param new_collection_name: The name of the collection to work with.
        :param new_is_admin: A flag used to access the cluster as admin (True) or as a regular developer (False).
        :return: The collection where documents can be accessed or stored.
        """
        if (self.database is None or self.database_name != new_database_name or
                self.collection_name != new_collection_name or self.is_admin != new_is_admin):
            database_user_name = "dev1"
            database_password = "dev1"

            if new_is_admin:
                database_user_name = "admin1"
                database_password = "admin1"

            cluster = MongoClient(
                f"mongodb+srv://{database_user_name}:{database_password}@cluster.yyiqn.mongodb.net"
                f"/myFirstDatabase?retryWrites=true&w=majority"
            )

            self.database = cluster[new_database_name]
            self.collection = self.database[new_collection_name]
            self.database_name = new_database_name
            self.collection_name = new_collection_name
            self.is_admin = new_is_admin

        return self

    def insert_model(self, model) -> bool:
        """
        This method inserts the provided model into the database. This method will return true if the provided
        model was successfully inserted into the database. Otherwise, this method will return false.

        :param model: The model to insert into the database.
        :return A boolean that is True if the provided model was successfully inserted into the database. Returns
            False if the provided model failed to be inserted into the database.
        """
        # Make sure that the database is connected before trying to insert the provided model
        if (self.database is None or self.database_name is None or
                self.collection_name is None or self.is_admin is None):
            return False

        insert_action = self.collection.insert_one(model.__dict__)
        return insert_action.acknowledged
