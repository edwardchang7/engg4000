import unittest

from src.backend import cluster
from src.backend.models import rhythmic_pattern_model
from src.backend.models import tonal_pattern_model
from src.backend.Collections.Rhythmic_Pattern import Rhythmic_Pattern


class TestCluster(unittest.TestCase):
    def test_cluster_new_method(self):
        """
        Creates a new cluster instance and assert that its connection to the database was successful.
        """
        # start with no cluster instance
        cluster_instance = None
        self.assertIsNone(cluster_instance)

        # create a cluster instance and assert that it has been connected successfully
        database_name = "database"
        collection_name = "test"
        is_admin_value = False
        cluster_instance = cluster.Cluster(database_name, collection_name, is_admin_value)
        self.assertIsNotNone(cluster_instance)
        self.assertEqual(cluster_instance.database_name, database_name)
        self.assertEqual(cluster_instance.collection_name, collection_name)
        self.assertEqual(cluster_instance.is_admin, is_admin_value)

        # assert successful connection to cluster by performing actions
        example_data = {"_id": 0, "value": 0}
        collection_instance = cluster_instance.collection
        document = collection_instance.find_one({"_id": 0})

        if document is not None:
            collection_instance.delete_one(example_data)

        insert_action = collection_instance.insert_one(example_data)
        self.assertTrue(insert_action.acknowledged)

    def test_cluster_recreate(self):
        """
        Creates a new cluster instance and asserts that it replaces an already existing cluster instance. Therefore,
        this would also test that the cluster instance is singleton.
        """
        # create a cluster instance
        old_database_name = "database"
        old_collection_name = "test"
        old_is_admin_value = False
        old_cluster_instance = cluster.Cluster(old_database_name, old_collection_name, old_is_admin_value)
        self.assertIsNotNone(old_cluster_instance)
        self.assertEqual(old_cluster_instance.database_name, old_database_name)
        self.assertEqual(old_cluster_instance.collection_name, old_collection_name)
        self.assertEqual(old_cluster_instance.is_admin, old_is_admin_value)

        # replace the existing cluster instance with a new cluster instance
        new_database_name = "database_0"
        new_collection_name = "test_0"
        new_is_admin_value = False
        new_cluster_instance = cluster.Cluster(new_database_name, new_collection_name, new_is_admin_value)
        self.assertIsNotNone(new_cluster_instance)
        self.assertEqual(new_cluster_instance.database_name, new_database_name)
        self.assertEqual(new_cluster_instance.collection_name, new_collection_name)
        self.assertEqual(new_cluster_instance.is_admin, new_is_admin_value)

        # assert successful connection to the new cluster by performing actions with it
        example_data = {"_id": 0, "test_value": 0}
        collection_instance = new_cluster_instance.collection
        document = collection_instance.find_one({"_id": 0})

        if document is not None:
            collection_instance.delete_one(example_data)

        insert_action = collection_instance.insert_one(example_data)
        self.assertTrue(insert_action.acknowledged)

    def test_insert_rhythmic_pattern_model(self):
        """
        This test case tests that our rhythmic pattern models can be stored in the database successfully.
        """
        # instantiate test case variables
        example_collection_name = "Baby Shark"
        example_pattern = "[['[111]'], ['[111]'], ['[111]'], ['[111]']]"
        example_num_of_beats_value = 1
        example_frequency_value = 1
        example_length_value = 1
        example_is_v1_value = True

        # create a cluster instance and assert that it has been connected successfully
        database_name = "database"
        collection_name = example_collection_name
        is_admin_value = False
        cluster_instance = cluster.Cluster(database_name, collection_name, is_admin_value)
        self.assertIsNotNone(cluster_instance)
        self.assertEqual(cluster_instance.database_name, database_name)
        self.assertEqual(cluster_instance.collection_name, collection_name)
        self.assertEqual(cluster_instance.is_admin, is_admin_value)

        # Assert that our rhythmic pattern model can be stored in the database successfully
        rp = Rhythmic_Pattern(example_pattern, example_frequency_value, example_is_v1_value)
        list_of_rp = [rp, rp, rp, rp,  rp]
        rp_model = rhythmic_pattern_model.RhythmicPatternModel(example_collection_name, list_of_rp)        
        insert_rp_model_result = cluster_instance.insert_rhythmic_pattern_model(cluster_instance, rp_model)
        self.assertTrue(insert_rp_model_result)
