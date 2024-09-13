from pymongo import MongoClient

def ingest_data_from_mongodb(uri, database):
    client = MongoClient(uri)
    db = client[database]
    
    data = {}
    for collection_name in db.list_collection_names():
        collection = db[collection_name]
        data[collection_name] = list(collection.find())
    
    client.close()
    return data
