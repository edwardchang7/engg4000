from cluster import Cluster

test_collection = Cluster("database", "test", False)
test_collection.insert_one({"_id": 2, "value": 2})
