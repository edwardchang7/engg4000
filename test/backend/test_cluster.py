import unittest

from src.backend import cluster


class TestCluster(unittest.TestCase):
    def test_cluster_new_method(self):
        """
        Creates a new instance of cluster and asserts that its connection to the database was successful.
        """
        # start with no cluster instance
        cluster_instance = None
        self.assertIsNone(cluster_instance)

        # create a cluster instance and assert that it has been connected to the database
        database_name = "database"
        collection_name = "test"
        is_admin_value = False
        cluster_instance = cluster.Cluster(database_name, collection_name, is_admin_value)
        self.assertIsNotNone(cluster_instance)
        self.assertEqual(cluster_instance.database_name, database_name)
        self.assertEqual(cluster_instance.collection_name, collection_name)
        self.assertEqual(cluster_instance.is_admin, is_admin_value)

    def test_cluster_recreate(self):
        """
        Creates a new instance of cluster and asserts that it replaces an already existing cluster instance. This
        also tests that the cluster instance is singleton.
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

        # replace the cluster instance created with a new cluster instance
        new_database_name = "database_0"
        new_collection_name = "test_0"
        new_is_admin_value = False
        new_cluster_instance = cluster.Cluster(new_database_name, new_collection_name, new_is_admin_value)
        self.assertIsNotNone(new_cluster_instance)
        self.assertEqual(new_cluster_instance.database_name, new_database_name)
        self.assertEqual(new_cluster_instance.collection_name, new_collection_name)
        self.assertEqual(new_cluster_instance.is_admin, new_is_admin_value)
        