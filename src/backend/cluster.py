import certifi

from pymongo import MongoClient
from typing import Final

from src.backend.collections.rhythmic_pattern import RhythmicPattern
from src.backend.collections.tonal_pattern import TonalPattern
from src.backend.models.rhythmic_pattern_model import RhythmicPatternModel
from src.backend.models.tonal_pattern_model import TonalPatternModel


class Cluster:
    database = None
    collection = None
    database_name = None
    collection_name = None
    is_admin = None

    RHYTHMIC_PATTERN: Final = "rhythmic_pattern"
    TONAL_PATTERN: Final = "tonal_pattern"

    def __new__(cls, new_database_name: str, new_collection_name: str, new_is_admin: bool):
        """
        This method is automatically called when a Cluster object is created. It flexibly selects and returns the
        singleton MongoDB instance depending on the database and collection names provided.

        :param new_database_name: The name of the database to work with.
        :param new_collection_name: The name of the collection to work with.
        :param new_is_admin: A flag used to access the cluster as admin (True) or as a regular developer (False).
        :return: The collection where documents can be accessed or stored.
        """
        if (cls.database is None or cls.database_name != new_database_name or
                cls.collection_name != new_collection_name or cls.is_admin != new_is_admin):
            database_user_name = "dev1"
            database_password = "dev1"

            if new_is_admin:
                database_user_name = "admin1"
                database_password = "admin1"

            cluster = MongoClient(
                f"mongodb+srv://{database_user_name}:{database_password}@cluster.yyiqn.mongodb.net"
                f"/myFirstDatabase?retryWrites=true&w=majority",
                tlsCAFile=certifi.where()
            )

            cls.database = cluster[new_database_name]
            if new_collection_name is not None and new_collection_name != "":
                cls.collection = cls.database[new_collection_name]
            else:
                cls.collection = None
            cls.database_name = new_database_name
            cls.collection_name = new_collection_name
            cls.is_admin = new_is_admin

        return cls

    def insert_rhythmic_pattern_model(self, rhythmic_pattern_model: RhythmicPatternModel) -> bool:
        if not self._is_connected_to_database(self):
            return False

        if self.collection_name != rhythmic_pattern_model.collection_name:
            return False

        parsed_rhythmic_pattern_objects = []
        for i in range(len(rhythmic_pattern_model.rhythmic_pattern_objects)):
            parsed_rhythmic_pattern_objects.append(rhythmic_pattern_model.rhythmic_pattern_objects[i].__dict__)
        document_to_insert = {self.RHYTHMIC_PATTERN: parsed_rhythmic_pattern_objects}

        insert_action = self.collection.insert_one(document_to_insert)
        return insert_action.acknowledged

    def insert_tonal_pattern_model(self, tonal_pattern_model: TonalPatternModel) -> bool:
        if not self._is_connected_to_database(self):
            return False

        if self.collection_name != tonal_pattern_model.collection_name:
            return False

        parsed_tonal_pattern_objects = []
        for tonal_pattern in tonal_pattern_model.tonal_pattern_objects:
            parsed_tonal_pattern_objects.append(tonal_pattern.__dict__)
        document_to_insert = {self.TONAL_PATTERN: parsed_tonal_pattern_objects}

        insert_action = self.collection.insert_one(document_to_insert)
        return insert_action.acknowledged

    def query_rhythmic_patterns(self, song_name: str, length: int) -> list:
        # check connection to the database
        if not self._is_connected_to_database(self):
            return None

        # check that the database connection is set to the provided song name (collection)
        if self.collection_name != song_name:
            return None

        all_rhythmic_pattern_documents = self.collection.find({self.RHYTHMIC_PATTERN: {'$exists': True}})
        queried_rhythmic_patterns = []

        for rhythmic_pattern_document in all_rhythmic_pattern_documents:
            for rhythmic_pattern in rhythmic_pattern_document.get(self.RHYTHMIC_PATTERN):
                current_rhythmic_pattern_length: int = rhythmic_pattern.get('length')

                if (current_rhythmic_pattern_length is not None and
                        current_rhythmic_pattern_length == length):
                    queried_rhythmic_patterns.append(
                        RhythmicPattern(
                            rhythmic_pattern.get('pattern'),
                            rhythmic_pattern.get('frequency'),
                            rhythmic_pattern.get('is_v1')
                        )
                    )

        return queried_rhythmic_patterns

    def query_tonal_patterns(self, song_name: str, num_of_notes: int) -> list:
        # Check connection to the database
        if not self._is_connected_to_database(self):
            return None

        # Check that the database connection is set to the provided song name (collection)
        if self.collection_name != song_name:
            return None

        all_tonal_pattern_documents = self.collection.find({self.TONAL_PATTERN: {'$exists': True}})
        queried_tonal_patterns = []

        for tonal_pattern_document in all_tonal_pattern_documents:
            for tonal_pattern in tonal_pattern_document.get(self.RHYTHMIC_PATTERN):
                current_tonal_pattern_num_of_beats: int = tonal_pattern.get('num_of_notes')

                if (current_tonal_pattern_num_of_beats is not None and
                        current_tonal_pattern_num_of_beats == num_of_notes):
                    queried_tonal_patterns.append(
                        TonalPattern(
                            tonal_pattern.get('pattern'),
                            tonal_pattern.get('num_of_notes'),
                            tonal_pattern.get('priority')
                        )
                    )

        return queried_tonal_patterns

    def query_all_tonal_patterns(self, song_name: str) -> list:
        # Check connection to the database
        if not self._is_connected_to_database(self):
            return None

        # Check that the database connection is set to the provided song name (collection name)
        if self.collection_name != song_name:
            return None

        all_tonal_pattern_documents = self.collection.find({self.TONAL_PATTERN: {'$exists': True}})
        queried_tonal_patterns = []

        for tonal_pattern_document in all_tonal_pattern_documents:
            for tonal_pattern in tonal_pattern_document.get(self.TONAL_PATTERN):
                queried_tonal_patterns.append(
                    TonalPattern(
                        tonal_pattern.get('pattern'),
                        tonal_pattern.get('num_of_notes'),
                        tonal_pattern.get('priority')
                    )
                )

        return queried_tonal_patterns

    def get_collection_names(self) -> list:
        if self is None or self.database_name is None:
            return None

        return self.database.list_collection_names()

    def _is_connected_to_database(self) -> bool:
        connected = False

        if (self.database is not None and self.database_name is not None and
                self.collection_name is not None and self.is_admin is not None):
            connected = True

        return connected
