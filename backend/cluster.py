from pymongo import MongoClient


class Cluster:
    __database = None
    __collection = None
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
        if (self.__database is None or self.database_name != new_database_name or
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

            self.__database = cluster[new_database_name]
            self.__collection = self.__database[new_collection_name]
            self.database_name = new_database_name
            self.collection_name = new_collection_name
            self.is_admin = new_is_admin

        return self.__collection
