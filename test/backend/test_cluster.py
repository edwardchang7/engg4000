import unittest

from src.backend.cluster import Cluster
from src.backend.collections.rhythmic_pattern import Rhythmic_Pattern
from src.backend.collections.tonal_pattern import TonalPattern
from src.backend.models.rhythmic_pattern_model import RhythmicPatternModel
from src.backend.models.tonal_pattern_model import TonalPatternModel

from typing import Final


class TestCluster(unittest.TestCase):
    FIRST_TEST_DATABASE: Final[str] = "TEST_DATABASE_1"
    FIRST_TEST_COLLECTION: Final[str] = "TEST COLLECTION 1"
    SECOND_TEST_DATABASE: Final[str] = "TEST_DATABASE_2"
    SECOND_TEST_COLLECTION: Final[str] = "TEST COLLECTION 2"
    RHYTHMIC_PATTERN_TEST_COLLECTION: Final[str] = "RHYTHMIC PATTERN TEST COLLECTION"
    TONAL_PATTERN_TEST_COLLECTION: Final[str] = "TONAL PATTERN TEST COLLECTION"

    def test_cluster_new_method(self):
        """
        Creates a new cluster instance and assert that its connection to the database was successful.
        """
        # Start with no cluster instance
        cluster_instance = None
        self.assertIsNone(cluster_instance)

        # Create a cluster instance and assert that it has been connected successfully
        cluster_instance = Cluster(self.FIRST_TEST_DATABASE, self.FIRST_TEST_COLLECTION, False)
        self.assertIsNotNone(cluster_instance)
        self.assertEqual(cluster_instance.database_name, self.FIRST_TEST_DATABASE)
        self.assertEqual(cluster_instance.collection_name, self.FIRST_TEST_COLLECTION)
        self.assertFalse(cluster_instance.is_admin)

        # Assert successful connection to cluster by performing actions
        example_data = {"_id": 0, "value": 0}
        document = cluster_instance.collection.find_one({"_id": 0})

        if document is not None:
            cluster_instance.collection.delete_one(example_data)

        insert_action = cluster_instance.collection.insert_one(example_data)
        self.assertTrue(insert_action.acknowledged)

    def test_cluster_recreate(self):
        """
        Creates a new cluster instance and asserts that it replaces an already existing cluster instance. Therefore,
        this would also test that the cluster instance is singleton.
        """
        # Create a cluster instance
        cluster_instance = Cluster(self.FIRST_TEST_DATABASE, self.FIRST_TEST_COLLECTION, False)
        self.assertIsNotNone(cluster_instance)
        self.assertEqual(cluster_instance.database_name, self.FIRST_TEST_DATABASE)
        self.assertEqual(cluster_instance.collection_name, self.FIRST_TEST_COLLECTION)
        self.assertFalse(cluster_instance.is_admin)

        # Replace the old cluster instance with a new cluster instance
        cluster_instance = Cluster(self.SECOND_TEST_DATABASE, self.SECOND_TEST_COLLECTION, False)
        self.assertIsNotNone(cluster_instance)
        self.assertEqual(cluster_instance.database_name, self.SECOND_TEST_DATABASE)
        self.assertEqual(cluster_instance.collection_name, self.SECOND_TEST_COLLECTION)
        self.assertFalse(cluster_instance.is_admin)

        # Assert successful connection to the new cluster by performing actions with it
        example_data = {"_id": 0, "test_value": 0}
        document = cluster_instance.collection.find_one({"_id": 0})

        if document is not None:
            cluster_instance.collection.delete_one(example_data)

        insert_action = cluster_instance.collection.insert_one(example_data)
        self.assertTrue(insert_action.acknowledged)

    def test_insert_rhythmic_pattern_model(self):
        """
        This test case tests that our rhythmic pattern models can be stored in the database successfully.
        """
        # Instantiate test case variables
        test_rhythmic_pattern_song_name = self.RHYTHMIC_PATTERN_TEST_COLLECTION
        test_rhythmic_pattern_pattern = "[['[111]'], ['[111]'], ['[111]'], ['[111]']]"
        test_rhythmic_pattern_frequency = 1
        test_rhythmic_pattern_is_v1 = True

        # Create a cluster instance and assert that it has been connected successfully
        cluster_instance = Cluster(self.FIRST_TEST_DATABASE, test_rhythmic_pattern_song_name, False)
        self.assertIsNotNone(cluster_instance)
        self.assertEqual(cluster_instance.database_name, self.FIRST_TEST_DATABASE)
        self.assertEqual(cluster_instance.collection_name, test_rhythmic_pattern_song_name)
        self.assertFalse(cluster_instance.is_admin)

        # Create a rhythmic pattern model that is used to insert rhythmic patterns into the database
        test_rhythmic_pattern = Rhythmic_Pattern(
            test_rhythmic_pattern_pattern, test_rhythmic_pattern_frequency, test_rhythmic_pattern_is_v1
        )
        test_list_of_rhythmic_patterns = [test_rhythmic_pattern, test_rhythmic_pattern, test_rhythmic_pattern]
        test_rhythmic_pattern_model = RhythmicPatternModel(
            test_rhythmic_pattern_song_name, test_list_of_rhythmic_patterns
        )

        # Assert that our rhythmic pattern model can be stored in the database successfully
        insert_rp_model_result = cluster_instance.insert_rhythmic_pattern_model(
            cluster_instance, test_rhythmic_pattern_model
        )
        self.assertTrue(insert_rp_model_result)

    def test_insert_tonal_pattern_model(self):
        # Instantiate test case variables
        test_tonal_pattern_song_name = self.TONAL_PATTERN_TEST_COLLECTION
        test_tonal_pattern_pattern = [['[111]'], ['[111]'], ['[111]'], ['[111]']]
        test_rhythmic_pattern_priority_value = 1
        test_rhythmic_pattern_num_of_notes = 1

        # Create a cluster instance and assert that it has been connected successfully
        cluster_instance = Cluster(self.FIRST_TEST_DATABASE, test_tonal_pattern_song_name, False)
        self.assertIsNotNone(cluster_instance)
        self.assertEqual(cluster_instance.database_name, self.FIRST_TEST_DATABASE)
        self.assertEqual(cluster_instance.collection_name, test_tonal_pattern_song_name)
        self.assertFalse(cluster_instance.is_admin)

        # Create a tonal pattern model that is used to insert tonal patterns into the database
        test_tonal_pattern = TonalPattern(
            test_tonal_pattern_pattern, test_rhythmic_pattern_priority_value, test_rhythmic_pattern_num_of_notes
        )
        test_list_of_tonal_patterns = [test_tonal_pattern, test_tonal_pattern, test_tonal_pattern]
        test_tonal_pattern_model = TonalPatternModel(test_tonal_pattern_song_name, test_list_of_tonal_patterns)

        # Assert that our tonal pattern model can be stored in the database successfully
        insert_tp_model_result = cluster_instance.insert_tonal_pattern_model(cluster_instance, test_tonal_pattern_model)
        self.assertTrue(insert_tp_model_result)
