from abc import ABC, abstractmethod

from mongo import MongoDatabaseHandler


class StorageAbstract(ABC):

    @abstractmethod
    def store(self, data, *args):
        pass



class MongoDataBase(StorageAbstract):
    def __init__(self):
        self.mongo = MongoDatabaseHandler()

    def store(self, data, collection,  *args):
        collection = getattr(self.mongo.database, collection)
        if len(data) > 1 and isinstance(data, list):
            collection.insert_many(data) 
        else:
            collection.insert_one(data)


    def load(self):
        return self.mongo.database.jobs_links.find()