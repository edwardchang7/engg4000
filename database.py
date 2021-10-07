from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://dev1:dev1@cluster.yyiqn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = cluster["database"]
collection = database["test"]

collection.insert_one({"_id": 2, "value": 2})
