from cluster import Cluster

test_collection = Cluster("database", "test", False)
test_collection.insert_one({"_id": 3, "value": 3})
